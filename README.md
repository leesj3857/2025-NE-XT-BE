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

## 🔐 Password Handling

- **Password Hashing**: Passwords are securely stored using Django's built-in `set_password()` method.
- **Encryption Method**: Django uses PBKDF2 with a SHA256 hash.

---

## 📅 Email Verification Code Handling

- **Code Generation**: Random 6-digit numeric code (`random.randint(100000, 999999)`)
- **Storage**: `EmailVerification` table records (`email`, `code`, `purpose`, `created_at`, `token`)
- **Expiration**: Codes expire 5 minutes after creation (`is_expired()` method).
- **One-Time Token**: For password reset and signup, a one-time `token` (URL-safe random 32-byte string) is generated after code verification.

---

## 🔎 Optional Admin API

### Remote Migration Execution

- **Effect**: Runs Django migration remotely to apply new DB changes.

---