import requests, random, os
from bs4 import BeautifulSoup

def get_link():
    # 1. 레벨과 주제 리스트 설정
    levels = ['b1', 'b2']
    topics = [
        "soci%C3%A9t%C3%A9", "culture", "%C3%A9conomie", 
        "politique", "environnement", "sciences-sant%C3%A9"
    ]
    
    selected_level = random.choice(levels)
    selected_topic = random.choice(topics)
    
    # 2. 최종 카테고리 URL 구성
    # 예: https://francaisfacile.rfi.fr/fr/comprendre-actualité-français/b1/société/
    base_url = f"https://francaisfacile.rfi.fr/fr/comprendre-actualit%C3%A9-fran%C3%A7ais/{selected_level}/{selected_topic}/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(base_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        links = []
        # 해당 카테고리 페이지 내에서 연습문제 링크 추출
        for a in soup.find_all('a', href=True):
            href = a['href']
            # 실제 학습 콘텐츠는 보통 '/fr/exercices/' 경로를 포함함
            if '/fr/exercices/' in href and len(href) > 40:
                if not href.startswith('http'):
                    href = "https://francaisfacile.rfi.fr" + href
                links.append(href)
        
        if links:
            # 중복 제거 후 랜덤 하나 선택
            return random.choice(list(set(links))), selected_level, selected_topic
        return None, selected_level, selected_topic
        
    except Exception as e:
        print(f"Error: {e}")
        return None, None, None

# 텔레그램 전송 부분
token = os.environ.get('TELEGRAM_TOKEN')
chat_id = os.environ.get('CHAT_ID')
link, level, topic = get_link()

if link and token and chat_id:
    # URL 인코딩된 주제를 다시 읽기 편하게 변환
    display_topic = topic.replace("%C3%A9", "é").replace("%C3%A9", "é").replace("-", "/")
    
    text = (
        f"🇫🇷 오늘의 프랑스어 연습 도착!\n\n"
        f"📌 레벨: {level.upper()}\n"
        f"📂 주제: {display_topic.capitalize()}\n"
        f"🔗 링크: {link}\n\n"
        f"오늘의 30분을 응원합니다! Bonne chance!"
    )
    requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={'chat_id': chat_id, 'text': text})
else:
    print("조건에 맞는 링크를 찾지 못했습니다.")
