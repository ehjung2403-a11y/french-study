name: French Bot
on:
  schedule:
    - cron: '0 20 * * *' # 세네갈 시간 저녁 8시 (UTC 20:00)
  workflow_dispatch: # 수동 실행 버튼

jobs:
  run-bot:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install
        run: pip install requests beautifulsoup4
      - name: Run
        env:
          TELEGRAM_TOKEN: ${{ secrets.TELEGRAM_TOKEN }}
          CHAT_ID: ${{ secrets.CHAT_ID }}
        run: python main.py
