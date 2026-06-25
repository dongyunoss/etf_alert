import logging

import requests

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

logger = logging.getLogger(__name__)

_API_BASE = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


def send_message(text: str):
    url = f"{_API_BASE}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        logger.info("텔레그램 메시지 전송 완료")
    except Exception as exc:
        logger.error("텔레그램 전송 실패: %s", exc)


def format_etf_message(etfs: list[dict]) -> str:
    lines = ["📢 <b>ETF 신규 상장 알림</b>\n"]
    for etf in etfs:
        lines.append(
            f"• <b>{etf['name']}</b> ({etf['short_code']})\n"
            f"  상장일: {etf['listing_date']}  시장: {etf.get('market', '-')}\n"
            f"  ISIN: <code>{etf['isin']}</code>"
        )
    lines.append(
        "\n🔗 <a href='https://n.news.naver.com/mnews/article/list/0001?sid=101'>KRX ETF 정보</a>"
    )
    return "\n".join(lines)
