# Java 17 + Python3 기반 이미지로 변경
FROM eclipse-temurin:17-jdk

WORKDIR /app

# Chrome 및 필수 도구 설치
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    wget \
    unzip \
    curl \
    gnupg \
    ca-certificates \
    chromium-driver \
    chromium \
    && apt-get clean

# Chrome 환경 변수
ENV CHROME_BIN=/usr/bin/chromium
ENV PATH="$PATH:/usr/lib/chromium"

# pip 업그레이드 및 Python 패키지 설치
RUN pip3 install --upgrade pip && \
    pip3 install selenium webdriver-manager

# 프로젝트 복사 및 빌드
COPY . .
RUN chmod +x gradlew
RUN ./gradlew build -x test

# 실행
CMD ["java", "-jar", "build/libs/naver-crawler-api-0.0.1-SNAPSHOT.jar"]
