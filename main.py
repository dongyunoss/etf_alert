"""ETF 신규 상장 알림 봇 진입점."""

import logging
import sys

from apscheduler.schedulers.blocking import BlockingScheduler

import db
from config import SCHEDULE_HOUR, SCHEDULE_MINUTE
from krx_scraper import get_new_listings
from telegram_bot import format_etf_message, send_message

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def job():
    logger.info("ETF 신규 상장 확인 시작")
    new_etfs = get_new_listings()

    unseen = [e for e in new_etfs if not db.is_notified(e["isin"])]
    if not unseen:
        logger.info("새로운 신규 상장 ETF 없음")
        return

    msg = format_etf_message(unseen)
    send_message(msg)

    for etf in unseen:
        db.mark_notified(etf["isin"], etf["short_code"], etf["name"], etf["listing_date"])

    logger.info("%d개 ETF 알림 전송 완료", len(unseen))


def job_no_db():
    """GitHub Actions용: DB 없이 오늘 신규 상장 ETF를 바로 전송."""
    logger.info("ETF 신규 상장 확인 시작 (DB 없음)")
    new_etfs = get_new_listings()
    if not new_etfs:
        logger.info("오늘 신규 상장 ETF 없음")
        return
    send_message(format_etf_message(new_etfs))
    logger.info("%d개 ETF 알림 전송 완료", len(new_etfs))


def main():
    # GitHub Actions: DB 없이 즉시 실행
    if "--run-now" in sys.argv:
        job_no_db()
        return

    db.init_db()

    scheduler = BlockingScheduler(timezone="Asia/Seoul")
    scheduler.add_job(
        job,
        trigger="cron",
        hour=SCHEDULE_HOUR,
        minute=SCHEDULE_MINUTE,
        id="etf_alert",
    )
    logger.info(
        "스케줄러 시작: 매일 %02d:%02d (KST) 실행", SCHEDULE_HOUR, SCHEDULE_MINUTE
    )
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("봇 종료")


if __name__ == "__main__":
    main()
