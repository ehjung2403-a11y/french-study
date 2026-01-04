import requests, random, os
from bs4 import BeautifulSoup

def get_rfi_b1_link():
    # B1 연습문제 목록 페이지
    url = "https://francaisfacile.rfi.fr/fr/comprendre-actualit%C3%A9-fran%C3%A7ais/b1/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return None, f"사이트 접속 실패 (Status: {response.status_code})"

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 기사 링크 추출 (보통 /fr/exercices/ 경로를 가집니다)
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            # 중복 방지 및 실제 기사 링크만 필터링
            if '/fr/exercices/' in href and len(href) > 40:
                if not href.startswith('http'):
                    href = "https://francaisfacile.rfi.fr" + href
                links.append(href)
        
        if links:
            return random.choice(list(set(links))), "성공"
        else:
            return None, "기사 링크를 찾지 못했습니다."

    except Exception as e:
        return None, str(e)

# 실행 및 전송
token = os.environ.get('TELEGRAM_TOKEN')
chat_id = os.environ.get('CHAT_ID')
link, status = get_rfi_b1_link()

if token and chat_id:
    if link:
        text = f"🇫🇷 오늘의 프랑스어 연습 (B1) 🇫🇷\n\n알림이 왔을 때 바로 시작해보세요!\n\n🔗 링크: {link}"
    else:
        text = f"⚠️ 봇 실행 알림\n원인: {status}\n나중에 다시 시도하거나 코드를 점검해주세요."
    
    requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={'chat_id': chat_id, 'text': text})
