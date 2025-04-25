# 📘 Translation & User Management API (Category, Region, User, Password)

This backend provides services for:

- 📂 **Korean Category ➞ English Translation**
- 📍 **English Region ➞ Korean Translation**
- 🔐 **User Registration, Login, Email Verification**
- 🔑 **Password Reset via Email Authentication**

All translations and user activities are managed through a PostgreSQL database.

---

## 🔧 Technology Stack

- **Backend**: Django 5 + Django REST Framework
- **Database**: PostgreSQL (via Render)
- **Translation API**: DeepL Free API
- **Deployment**: Docker + Render

---

## ✅ Features

### 1. Translate Korean Category ➞ English

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

### 2. Translate English Region ➞ Korean

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

### 3. Retrieve Place Information

- **Endpoint**: `POST /api/place-info/`
- **Request Body**:
  ```json
  {
    "name": "한강 마법도전",
    "address": "강남구 가락동"
  }
  ```
- **Response**:
  ```json
  {
    "title": "한강 마법도전",
    "category": "Restaurant",
    "address": "강남구 가락동",
    "description": "Famous Korean pancake place",
    "menu_or_ticket_info": { ... },
    "price": "$15",
    "translated_reviews": ["Really delicious!", "Highly recommend!"]
  }
  ```

### 4. User Registration

- **Endpoint**: `POST /api/register/`
- **Request Body**:
  ```json
  {
    "email": "test@example.com",
    "name": "John",
    "password": "password123"
  }
  ```
- **Response**:
  ```json
  {
    "message": "회원가입 성공!"
  }
  ```

### 5. User Login

- **Endpoint**: `POST /api/login/`
- **Request Body**:
  ```json
  {
    "email": "test@example.com",
    "password": "password123"
  }
  ```
- **Response**:
  ```json
  {
    "message": "로그인 성공",
    "access": "ACCESS_TOKEN",
    "refresh": "REFRESH_TOKEN",
    "user_id": 1
  }
  ```

### 6. Check Email Duplication

- **Endpoint**: `POST /api/check-email/`
- **Request Body**:
  ```json
  {
    "email": "test@example.com"
  }
  ```
- **Response**:
  ```json
  {
    "exists": true
  }
  ```

### 7. Send Email Verification Code (Sign Up)

- **Endpoint**: `POST /api/email/send-code/`
- **Request Body**:
  ```json
  {
    "email": "test@example.com"
  }
  ```

### 8. Verify Email Code (Sign Up)

- **Endpoint**: `POST /api/email/verify-code/`
- **Request Body**:
  ```json
  {
    "email": "test@example.com",
    "code": "123456"
  }
  ```

### 9. Send Password Reset Code

- **Endpoint**: `POST /api/password/send-reset-code/`
- **Request Body**:
  ```json
  {
    "email": "test@example.com"
  }
  ```

### 10. Verify Password Reset Code

- **Endpoint**: `POST /api/password/verify_reset_code/`
- **Request Body**:
  ```json
  {
    "email": "test@example.com",
    "code": "123456"
  }
  ```
- **Response**:
  ```json
  {
    "message": "인증 성공",
    "token": "one_time_reset_token"
  }
  ```

### 11. Reset Password

- **Endpoint**: `POST /api/password/reset/`
- **Request Body**:
  ```json
  {
    "email": "test@example.com",
    "token": "one_time_reset_token",
    "new_password": "newpassword456"
  }
  ```

---

## 🔐 Password Handling

- **Password Hashing**: Passwords are securely stored using Django's built-in `set_password()` method.
- **Encryption Method**: Django uses PBKDF2 with a SHA256 hash.

---

## 📅 Email Verification Code Handling

- **Code Generation**: Random 6-digit numeric code (`random.randint(100000, 999999)`)
- **Storage**: `EmailVerification` table records (`email`, `code`, `purpose`, `created_at`, `token`)
- **Expiration**: Codes expire 5 minutes after creation (`is_expired()` method).
- **One-Time Token**: For password reset, a one-time `token` (URL-safe random 32-byte string) is generated after code verification.

---

## 🔎 Optional Admin API

### Remote Migration Execution

- **Endpoint**: `POST /api/migrate/`
- **Effect**: Runs Django migration remotely to apply new DB changes.

---


