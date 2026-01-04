import requests, random, os, urllib.parse
from bs4 import BeautifulSoup

def get_rfi_b1_link():
    # 가장 정확한 목록 페이지
    url = "https://francaisfacile.rfi.fr/fr/exercices/b1/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8' # 한글/프랑스어 깨짐 방지
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        links = []
        # 페이지 내의 모든 링크를 검사
        for a in soup.find_all('a', href=True):
            href = a['href']
            
            # 기사 링크의 특징: 특정 레벨(b1)이나 기사 카테고리가 포함되고 길이가 긴 것들
            if len(href) > 35 and ('/fr/' in href):
                # 상대 경로를 절대 경로로 변환
                if not href.startswith('http'):
                    full_url = "https://francaisfacile.rfi.fr" + href
                else:
                    full_url = href
                
                # 링크에 프랑스어 특수문자가 있으면 안전하게 인코딩 (깨짐 방지)
                safe_url = urllib.parse.quote(full_url, safe=':/?&=')
                links.append(safe_url)
        
        # 목록 페이지 자신이나 불필요한 페이지 제외
        final_links = [l for l in list(set(links)) if not l.endswith('/b1/') and 'exercices' in l]
        
        if final_links:
            return random.choice(final_links), "성공"
        else:
            return None, "기사 링크 추출 실패"

    except Exception as e:
        return None, str(e)

# 실행 및 전송
token = os.environ.get('TELEGRAM_TOKEN')
chat_id = os.environ.get('CHAT_ID')
link, status = get_rfi_b1_link()

if token and chat_id:
    if link:
        text = f"🇫🇷 오늘의 B1 프랑스어 연습 🇫🇷\n\n주소 깨짐 문제를 해결했습니다. 열공하세요!\n\n🔗 링크: {link}"
    else:
        text = f"⚠️ 봇 실행 알림\n원인: {status}"
    
    requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={'chat_id': chat_id, 'text': text})
