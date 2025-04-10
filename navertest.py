from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def crawl_naver_place_info(keyword):
    # 1. 브라우저 실행
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # 2. 네이버 지도 접속
    driver.get("https://map.naver.com/p")
    time.sleep(5)

    # 3. 전체 페이지는 iframe 구조. 검색창은 페이지 최상단의 Shadow DOM 내부가 아님.
    # 검색창은 iframe 밖에 있으므로, 직접 탐색 가능
    try:
        search_input = driver.find_element(By.CSS_SELECTOR, "input.input_search")
        search_input.send_keys(keyword)
        search_input.send_keys(Keys.ENTER)
    except Exception as e:
        print("검색창 입력 실패:", e)
        driver.quit()
        return

    time.sleep(5)

    # 4. 검색 결과 iframe 진입
    driver.switch_to.frame("searchIframe")
    time.sleep(2)

    # 5. 첫 번째 장소 클릭
    try:
        first_place = driver.find_element(By.CSS_SELECTOR, "ul > li")

        # li 내부에서 a 태그를 다시 탐색
        link_in_place = first_place.find_element(By.CSS_SELECTOR, "a")
        link_in_place.click()
    except Exception as e:
        print("장소 클릭 실패:", e)
        # driver.quit()
        # return

    time.sleep(3)

    # 6. 상세 정보 iframe으로 전환
    driver.switch_to.default_content()
    driver.switch_to.frame("entryIframe")
    time.sleep(2)

    # 7. 정보 추출
    try:
        title = driver.find_element(By.CSS_SELECTOR, "span.GHAhO").text
        category = driver.find_element(By.CSS_SELECTOR, "span.lnJFt").text
        address = driver.find_element(By.CSS_SELECTOR, "span.LDgIH").text
        phone = driver.find_element(By.CSS_SELECTOR, "span.xlx7Q").text
        print(f"이름: {title}")
        print(f"분류: {category}")
        print(f"주소: {address}")
        print(f"전화번호: {phone}")
    except Exception as e:
        print("정보 추출 실패:", e)

    # 8. 메뉴 탭 클릭 → 메뉴 내용 로딩
    try:
        # 모든 탭 중 텍스트가 '메뉴'인 탭 클릭
        menu_tabs = driver.find_elements(By.CSS_SELECTOR, ".veBoZ")
        for tab in menu_tabs:
            if tab.text.strip() == "메뉴":
                tab.click()
                time.sleep(2)  # 메뉴 탭 전환 대기
                break
    except Exception as e:
        print("메뉴 탭 클릭 실패:", e)

    # 9. 메뉴 정보 추출
    try:
        menu_names = driver.find_elements(By.CSS_SELECTOR, ".lPzHi")
        menu_prices = driver.find_elements(By.CSS_SELECTOR, ".GXS1X em")

        if not menu_names:
            print("❌ 메뉴 항목 없음.")
        else:
            print("\n[메뉴]")
            for name, price in zip(menu_names, menu_prices):
                print(f"- {name.text.strip()}: {price.text.strip()}원")
    except Exception as e:
        print("메뉴 추출 실패:", e)

    # 10. 리뷰 탭 클릭
    try:
        review_tabs = driver.find_elements(By.CSS_SELECTOR, ".veBoZ")
        for tab in review_tabs:
            if tab.text.strip() == "리뷰":
                tab.click()
                time.sleep(2)  # 리뷰 탭 로딩 대기
                break
    except Exception as e:
        print("리뷰 탭 클릭 실패:", e)

    # 11. 리뷰 더보기 버튼 눌러서 더 가져오기 (.fvwqf)
    try:
        max_reviews = 30
        clicked = 0
        while True:
            # 현재 수집된 리뷰 개수
            current_reviews = driver.find_elements(By.CSS_SELECTOR, ".pui__vn15t2 a")
            if len(current_reviews) >= max_reviews:
                break

            # 더보기 버튼 찾기
            try:
                more_button = driver.find_element(By.CSS_SELECTOR, ".fvwqf")
                driver.execute_script("arguments[0].click();", more_button)  # JS로 안전 클릭
                clicked += 1
                time.sleep(1.5)  # 로딩 대기
            except:
                break  # 더보기 버튼 없음

            if clicked >= 5:  # 최대 클릭 횟수 제한 (안전장치)
                break
    except Exception as e:
        print("리뷰 더보기 처리 실패:", e)

    # 12. 리뷰 본문 추출
    try:
        print("\n[리뷰 최대 30개]")

        review_blocks = driver.find_elements(By.CSS_SELECTOR, ".pui__vn15t2 a")
        reviews = []

        for review in review_blocks:
            text = review.text.strip()
            if text == "더보기":
                continue
            html_content = review.get_attribute("innerHTML")
            clean_text = html_content.replace("<br>", "\n").strip()
            reviews.append(clean_text)

        if not reviews:
            print("리뷰 없음.")
        else:
            for idx, r in enumerate(reviews[:30], 1):  # 30개 제한 출력
                print(f"{idx}. {r}")

    except Exception as e:
        print("리뷰 추출 실패:", e)








    driver.quit()

# 실행
crawl_naver_place_info("잠실 맛집")
