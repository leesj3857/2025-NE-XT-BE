package com.koreat.naver_crawler_api.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebConfig {
    @Bean
    public WebMvcConfigurer corsConfigurer() {
        return new WebMvcConfigurer() {
            @Override
            public void addCorsMappings(CorsRegistry registry) {
                registry.addMapping("/**") // 모든 경로에 대해
                        .allowedOrigins("http://localhost:5173") // ✅ 프론트 주소
                        .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS") // ✅ preflight 포함
                        .allowedHeaders("*") // 모든 헤더 허용
                        .allowCredentials(false); // 쿠키 전달 필요 없으면 false
            }
        };
    }
}