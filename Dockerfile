FROM eclipse-temurin:17-jdk-alpine

WORKDIR /app

# 1. Python + pip + 필요한 도구 설치
RUN apk add --no-cache \
    python3 \
    py3-pip \
    chromium \
    chromium-chromedriver \
    bash

# 2. 크롬 환경 변수 등록 (headless용)
ENV CHROME_BIN=/usr/bin/chromium-browser
ENV PATH="$PATH:/usr/lib/chromium/"

# 3. Python 패키지 설치 (selenium, webdriver-manager 등)
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# 4. Java 프로젝트 설정
COPY . .
RUN chmod +x gradlew
RUN ./gradlew build -x test

# 5. 실행
CMD ["java", "-jar", "build/libs/naver-crawler-api-0.0.1-SNAPSHOT.jar"]
