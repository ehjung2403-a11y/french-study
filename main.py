import requests
import os

# 텔레그램 정보 설정
token = os.environ.get('TELEGRAM_TOKEN')
chat_id = os.environ.get('CHAT_ID')

# 고정 링크 (B1 연습문제 목록 페이지)
exercise_url = "https://francaisfacile.rfi.fr/fr/exercices/b1/"

if token and chat_id:
    text = (
        "🔔 프랑스어 공부 리마인더 🇫🇷\n\n"
        "오늘의 30분, 프랑스어와 친해질 시간입니다!\n"
        "아래 링크에서 마음에 드는 주제를 골라 풀어보세요.\n\n"
        f"🔗 연습문제 목록: {exercise_url}"
    )
    
    # 메시지 전송
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={'chat_id': chat_id, 'text': text})
