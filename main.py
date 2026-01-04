import requests, random, os, urllib.parse
from bs4 import BeautifulSoup

def get_rfi_b1_link():
    url = "https://francaisfacile.rfi.fr/fr/exercices/b1/"
    
    # 실제 브라우저처럼 보이게 하는 더 강력한 헤더
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://www.google.com/',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    try:
        # 세션을 사용하여 접속 (연속 접속처럼 보이게 함)
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=20)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            return None, f"차단됨 (Error {response.status_code})"

        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        
        # 기사 링크 추출 로직
        for a in soup.find_all('a', href=True):
            href = a['href']
            # b1 리스트가 아닌 실제 연습문제 주소 패턴
            if '/fr/' in href and len(href) > 40:
                if not href.startswith('http'):
                    full_url = "https://francaisfacile.rfi.fr" + href
                else:
                    full_url = href
                
                # 특수문자 안전 처리
                safe_url = urllib.parse.quote(full_url, safe=':/?&=')
                links.append(safe_url)
        
        final_links = list(set(links))
        if final_links:
            return random.choice(final_links), "성공"
        return None, "기사를 찾지 못함"

    except Exception as e:
        return None, f"에러: {str(e)}"

# 실행 및 전송
token = os.environ.get('TELEGRAM_TOKEN')
chat_id = os.environ.get('CHAT_ID')
link, status = get_rfi_b1_link()

if token and chat_id:
    if link:
        text = f"🇫🇷 오늘의 B1 프랑스어 연습 🇫🇷\n\n차단을 뚫고 기사를 가져왔습니다!\n\n🔗 링크: {link}"
    else:
        text = f"⚠️ 봇 실행 알림\n상태: {status}\n\n서버 차단이 강력하네요. 다시 우회 방법을 찾는 중입니다."
    
    requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={'chat_id': chat_id, 'text': text})
