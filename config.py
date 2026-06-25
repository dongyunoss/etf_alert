import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# 며칠 이내 신규 상장 ETF를 알림 대상으로 볼지 (기본 1일)
NEW_LISTING_DAYS = int(os.getenv("NEW_LISTING_DAYS", "1"))

# 스케줄 실행 시각 (24h 기준, 기본 오전 9시)
SCHEDULE_HOUR = int(os.getenv("SCHEDULE_HOUR", "9"))
SCHEDULE_MINUTE = int(os.getenv("SCHEDULE_MINUTE", "0"))

DB_PATH = os.getenv("DB_PATH", "etf_alert.db")
