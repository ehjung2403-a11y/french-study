import requests, random, os, urllib.parse
from bs4 import BeautifulSoup

def get_rfi_b1_link():
    # 타겟 페이지
    url = "https://francaisfacile.rfi.fr/fr/exercices/b1/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            return None, f"접속 실패 (코드: {response.status_code})"

        soup = BeautifulSoup(response.text, 'html.parser')
        
        links = []
        # 1. RFI 기사 카드(article)나 특정 클래스 내의 링크를 먼저 찾습니다.
        # RFI의 연습문제 기사들은 주로 m-item-list-article 클래스를 가집니다.
        articles = soup.find_all(['article', 'div'], class_=lambda x: x and 'article' in x)
        
        if not articles:
            # 클래스를 못 찾을 경우 모든 a 태그를 뒤집니다.
            articles = [soup]

        for container in articles:
            for a in container.find_all('a', href=True):
                href = a['href']
                # 기사 링크의 핵심 패턴: /fr/ 이 포함되고, b1이 아닌 특정 기사 제목이 길게 붙은 것
                if len(href) > 30 and '/fr/' in href and '/b1/' not in href:
                    if not href.startswith('http'):
                        full_url = "https://francaisfacile.rfi.fr" + href
                    else:
                        full_url = href
                    
                    # 프랑스어 특수문자 깨짐 방지 처리
                    safe_url = urllib.parse.quote(full_url, safe=':/?&=')
                    links.append(safe_url)
        
        # 중복 제거 및 필터링
        final_links = list(set(links))
        
        if final_links:
            return random.choice(final_links), "성공"
        else:
            return None, "기사 링크를 찾을 수 없음 (패턴 불일치)"

    except Exception as e:
        return None, f"에러 발생: {str(e)}"

# 실행 및 전송
token = os.environ.get('TELEGRAM_TOKEN')
chat_id = os.environ.get('CHAT_ID')
link, status = get_rfi_b1_link()

if token and chat_id:
    if link:
        text = f"🇫🇷 오늘의 B1 프랑스어 연습 🇫🇷\n\n링크 깨짐 및 추출 로직을 보완했습니다.\n\n🔗 링크: {link}"
    else:
        text = f"⚠️ 봇 실행 알림\n원인: {status}\n\n사용자께서 주신 링크 구조를 다시 확인중입니다."
    
    requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={'chat_id': chat_id, 'text': text})
