import requests, random, os
from bs4 import BeautifulSoup

def get_link():
    level = random.choice(['b1', 'b2'])
    url = f"https://francaisfacile.rfi.fr/fr/exercices/{level}/"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = ["https://francaisfacile.rfi.fr" + a['href'] for a in soup.find_all('a', href=True) if '/fr/exercices/' in a['href'] and len(a['href']) > 30]
        return random.choice(list(set(links))) if links else None
    except:
        return None

token = os.environ.get('TELEGRAM_TOKEN')
chat_id = os.environ.get('CHAT_ID')
link = get_link()

if link and token and chat_id:
    text = f"📢 오늘의 프랑스어 연습 🇫🇷\n{link}"
    api_url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(api_url, data={'chat_id': chat_id, 'text': text})
