# 🕷️ Naver Keyword Crawler API

Spring Boot와 Python을 연동하여 특정 키워드로 네이버에서 장소 정보를 크롤링하는 API입니다.

---

## 📦 프로젝트 구조

```
2025-NE-XT-BE/
├── crawler.py                 # Python 크롤러 (키워드 기반 장소 검색)
├── naver-crawler-api/
│   └── src/
│       └── main/
│           └── java/com/example/navercrawlerapi/
│               ├── NaverCrawlerApiApplication.java
│               └── controller/CrawlController.java
```

---

## 🚀 실행 방법

### 1. Python 환경 설정

#### 필요한 패키지 설치

```bash
pip install selenium webdriver-manager
```

### 2. Spring Boot 서버 실행

```bash
./gradlew bootRun
```

---

## 📡 API 호출 예시 (POST)

```
POST /api/crawl
Content-Type: application/json
```

**Request Body**
```json
{
  "keyword": "강남 맛집"
}
```

**Response Body (성공 시)**
```json
[
  {
    "name": "맛집이름",
    "address": "주소",
    "phone": "전화번호",
    ...
  },
  ...
]
```

> ⚠️ Python `crawler.py`는 Spring Boot 백엔드가 실행되는 동일 디렉토리 또는 절대 경로로 지정되어 있어야 합니다.

---

## 🧪 프론트엔드 테스트 예시

React 또는 Vue 등 프론트엔드에서:

```js
fetch("http://localhost:8080/api/crawl", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ keyword: "홍대 술집" })
})
.then(res => res.json())
.then(data => console.log(data));
```

---

## 📌 개발 참고사항

- `@CrossOrigin(origins = "http://localhost:5173")` 설정으로 프론트 포트 접근 가능
- Java에서 Python subprocess 실행 → 출력 읽어서 API 응답으로 반환
- 예외 상황 처리 및 exitCode 체크 포함

---

## 🗂 TODO

- [ ] 크롤링 결과 JSON 정제
- [ ] 키워드 중복 요청 캐싱
- [ ] 배포 환경용 CORS 도메인 추가

---

