# Use lightweight Java 17 base image
FROM eclipse-temurin:17-jdk-alpine

# Set working directory inside container
WORKDIR /app

# Copy project files into the container
COPY . .

# Build the project without running tests
RUN ./gradlew build -x test

# Run the compiled jar
CMD ["java", "-jar", "build/libs/naver-crawler-api-0.0.1-SNAPSHOT.jar"]
