"""KRX 공개 API를 통해 ETF 신규 상장 목록을 가져옵니다."""

import logging
from datetime import date, timedelta

import requests

from config import NEW_LISTING_DAYS

logger = logging.getLogger(__name__)

_KRX_URL = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"
_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020201",
}


def _fetch_etf_list() -> list[dict]:
    """KRX에서 전체 ETF 목록(ISIN, 종목코드, 종목명, 상장일)을 반환합니다."""
    params = {
        "bld": "dbms/MDC/STAT/standard/MDCSTAT04301",
        "locale": "ko_KR",
        "tboxisuCd_finder_secuprodisu1_0": "",
        "isuCd": "",
        "isuCd2": "",
        "codeNmisuCd_finder_secuprodisu1_0": "",
        "param1isuCd_finder_secuprodisu1_0": "ETF",
        "trdDd": date.today().strftime("%Y%m%d"),
        "share": "1",
        "money": "1",
        "csvxls_isNo": "false",
    }
    try:
        resp = requests.post(_KRX_URL, data=params, headers=_HEADERS, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        return data.get("OutBlock_1", [])
    except Exception as exc:
        logger.error("KRX API 호출 실패: %s", exc)
        return []


def get_new_listings() -> list[dict]:
    """오늘 기준 NEW_LISTING_DAYS 이내 신규 상장된 ETF 목록을 반환합니다."""
    cutoff = date.today() - timedelta(days=NEW_LISTING_DAYS - 1)
    etfs = _fetch_etf_list()
    new_etfs = []
    for etf in etfs:
        listing_str = etf.get("LIST_DD", "").replace("-", "").replace("/", "")
        if len(listing_str) != 8:
            continue
        try:
            listing_date = date(
                int(listing_str[:4]),
                int(listing_str[4:6]),
                int(listing_str[6:]),
            )
        except ValueError:
            continue
        if listing_date >= cutoff:
            new_etfs.append(
                {
                    "isin": etf.get("ISU_CD", ""),
                    "short_code": etf.get("ISU_SRT_CD", ""),
                    "name": etf.get("ISU_ABBRV", etf.get("ISU_NM", "")),
                    "listing_date": listing_date.isoformat(),
                    "market": etf.get("MKT_TP_NM", ""),
                }
            )
    logger.info("신규 상장 ETF %d건 발견 (기준일: %s 이후)", len(new_etfs), cutoff)
    return new_etfs
