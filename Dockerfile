FROM eclipse-temurin:17-jdk-alpine

WORKDIR /app

# 1. Python, pip, 크롬 설치
RUN apk add --no-cache \
    python3 \
    py3-pip \
    chromium \
    chromium-chromedriver \
    bash

# 2. 크롬 경로 환경 변수 설정 (headless용)
ENV CHROME_BIN=/usr/bin/chromium-browser
ENV PATH="$PATH:/usr/lib/chromium/"

# ✅ 3. 필요한 파이썬 패키지 직접 설치
RUN pip3 install --no-cache-dir selenium webdriver-manager

# 4. 프로젝트 복사 및 빌드
COPY . .
RUN chmod +x gradlew
RUN ./gradlew build -x test

# 5. 실행
CMD ["java", "-jar", "build/libs/naver-crawler-api-0.0.1-SNAPSHOT.jar"]
