
# 📘 Translation API (Category & Region)

This backend provides translation services for:

- 📂 **Korean Category ➝ English**
- 📍 **English Region ➝ Korean**

All translations are cached in a PostgreSQL database and logged for analytics.

---

## 🔧 Technology Stack

- **Backend**: Django 5 + Django REST Framework
- **Database**: PostgreSQL (via Render)
- **Translation API**: DeepL Free API
- **Deployment**: Docker + Render

---

## ✅ Features

### 1. Translate Korean Category ➝ English

- **Endpoint**: `POST /api/translate/`
- **Request Body**:
  ```json
  {
    "text": "음식점 > 한식 > 냉면"
  }
  ```
- **Response**:
  ```json
  {
    "translated_text": "Restaurant > Korean Food > Cold Noodles"
  }
  ```
- 🔁 Caches translated result in `Category` table.
- 📝 Logs each request in `CategoryLog`.

---

### 2. Translate English Region ➝ Korean

- **Endpoint**: `POST /api/translate/region/`
- **Request Body**:
  ```json
  {
    "text": "Gangnam-gu"
  }
  ```
- **Response**:
  ```json
  {
    "translated_text": "강남구"
  }
  ```
- 🔁 Caches translated result in `RegionName` table.
- 📝 Logs each request in `RegionLog`.

---

## 🛠️ Optional Admin API

### Run Migration Remotely

- **Endpoint**: `POST /api/migrate/`
- **Effect**: Runs `python manage.py migrate` remotely (used when pre-deploy is not available).

---

## 📌 Planned Features

- [ ] 장소 상세 정보 API
- [ ] English ➝ Korean category translation
- [ ] 사용자 로그인 & 인증
- [ ] 사용자 장소 즐겨찾기 저장 API

---

## 🧪 How to Test

You can test using **Postman** or any REST client:

- Set base URL to: `https://your-render-app.onrender.com`
- Send JSON `POST` requests to `/api/translate/` and `/api/translate/region/`.

---

© 2025 Smart&Wise | Developer: 이승준
