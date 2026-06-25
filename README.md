# ETF 신규 상장 텔레그램 알림 봇

KRX(한국거래소) 공개 API를 통해 ETF 신규 상장 정보를 수집하고, 텔레그램 봇으로 자동 알림을 전송하는 Python 스크립트입니다.

## 기능

- 매일 지정 시각에 KRX API에서 ETF 신규 상장 목록 자동 수집
- 신규 상장 ETF를 텔레그램으로 알림 전송
- SQLite DB로 중복 알림 방지
- 환경변수로 토큰, 스케줄, 알림 기준일 설정

## 프로젝트 구조

```
etf_alert/
├── main.py           # 진입점, APScheduler 스케줄러
├── krx_scraper.py    # KRX API ETF 신규 상장 수집
├── telegram_bot.py   # 텔레그램 메시지 전송
├── db.py             # SQLite 중복 알림 관리
├── config.py         # 환경변수 로드
├── requirements.txt
└── .env.example
```

## 시작하기

### 1. 텔레그램 봇 준비

1. 텔레그램에서 `@BotFather` 검색 → `/newbot` 명령어로 봇 생성 → **Bot Token** 발급
2. 생성한 봇과 채팅 시작
3. 아래 URL에서 **Chat ID** 확인
   ```
   https://api.telegram.org/bot<TOKEN>/getUpdates
   ```

### 2. 환경변수 설정

```bash
cp .env.example .env
```

`.env` 파일을 열어 아래 값을 입력합니다.

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
NEW_LISTING_DAYS=1
SCHEDULE_HOUR=9
SCHEDULE_MINUTE=0
DB_PATH=etf_alert.db
```

| 변수 | 설명 | 기본값 |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | BotFather에서 발급한 봇 토큰 | 필수 |
| `TELEGRAM_CHAT_ID` | 알림을 받을 채팅 ID | 필수 |
| `NEW_LISTING_DAYS` | 오늘로부터 며칠 이내 상장을 알림 대상으로 볼지 | `1` |
| `SCHEDULE_HOUR` | 매일 실행 시각 (시, KST) | `9` |
| `SCHEDULE_MINUTE` | 매일 실행 시각 (분, KST) | `0` |
| `DB_PATH` | SQLite DB 파일 경로 | `etf_alert.db` |

### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

### 4. 실행

```bash
# 즉시 실행 (테스트용)
python main.py --run-now

# 스케줄러 상시 실행 (매일 지정 시각 자동 실행)
python main.py
```

## 텔레그램 알림 예시

```
📢 ETF 신규 상장 알림

• KODEX AI반도체핵심장비 (123456)
  상장일: 2026-06-25  시장: KOSPI
  ISIN: KR7000000001

• TIGER 미국AI빅테크10 (234567)
  상장일: 2026-06-25  시장: KOSDAQ
  ISIN: KR7000000002
```

## 동작 흐름

```
매일 09:00 (KST)
    │
    ▼
KRX API에서 전체 ETF 목록 수집
    │
    ▼
오늘 신규 상장된 ETF 필터링
    │
    ▼
DB에서 이미 알림 보낸 ETF 제외
    │
    ├── 새로운 ETF 없음 → 종료
    │
    └── 새로운 ETF 있음 → 텔레그램 전송 → DB 기록
```

## 데이터 출처

- [KRX 정보데이터시스템](http://data.krx.co.kr) 공개 API (별도 API 키 불필요)
