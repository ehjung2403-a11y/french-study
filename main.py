import requests
import random
import os
from bs4 import BeautifulSoup

def get_rfi_b1_rss():
    # RFI에서 공식적으로 제공하는 연습문제 RSS 피드 주소입니다. (차단 안 됨)
    rss_url = "https://francaisfacile.rfi.fr/fr/exercices/b1/rss"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        response = requests.get(rss_url, headers=headers, timeout=20)
        # RSS는 XML 형식이므로 beautifulsoup으로 링크만 쏙 뽑아냅니다.
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        links = []
        for item in items:
            link = item.find('link').text.strip()
            if link:
                links.append(link)
        
        if links:
            # 가장 최신 기사 10개 중 하나를 랜덤으로 고릅니다.
            return random.choice(links[:10]), "성공"
        return None, "피드에서 링크를 찾지 못함"

    except Exception as e:
        return None, f"RSS 접속 에러: {str(e)}"

# 실행 및 전송
token = os.environ.get('TELEGRAM_TOKEN')
chat_id = os.environ.get('CHAT_ID')
link, status = get_rfi_b1_rss()

if token and chat_id:
    if link:
        # 텔레그램은 특수문자가 섞인 링크도 자동으로 잘 처리합니다.
        text = f"🇫🇷 오늘의 B1 프랑스어 연습 🇫🇷\n\n공식 피드를 통해 가져온 최신 기사입니다.\n\n🔗 링크: {link}"
    else:
        text = f"⚠️ 봇 실행 알림\n상태: {status}\n\nRSS 방식도 막혔다면 다른 사이트를 찾아보겠습니다."
    
    requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={'chat_id': chat_id, 'text': text})
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
