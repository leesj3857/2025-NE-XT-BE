FROM eclipse-temurin:17-jdk-alpine

WORKDIR /app

# 1. Python, pip, Chrome 설치 + 빌드 도구 추가
RUN apk add --no-cache \
    python3 \
    py3-pip \
    chromium \
    chromium-chromedriver \
    bash \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    make \
    cargo

# 2. Chrome 환경 변수
ENV CHROME_BIN=/usr/bin/chromium-browser
ENV PATH="$PATH:/usr/lib/chromium/"

# 3. Python 패키지 설치 (✅ 여기서 실패 방지용 추가 의존성 포함)
RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir selenium webdriver-manager

# 4. Java 프로젝트 빌드
COPY . .
RUN chmod +x gradlew
RUN ./gradlew build -x test

# 5. 실행
CMD ["java", "-jar", "build/libs/naver-crawler-api-0.0.1-SNAPSHOT.jar"]
