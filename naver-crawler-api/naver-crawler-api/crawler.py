from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import sys
import io
import time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def crawl_naver_place_info(keyword):
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--blink-settings=imagesEnabled=false")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 10)

    # 1. 네이버 지도 접속
    driver.get("https://map.naver.com/p")

    try:
        search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.input_search")))
        search_input.send_keys(keyword)
        search_input.send_keys(Keys.ENTER)
    except Exception as e:
        print("검색창 입력 실패:", e, file=sys.stderr)
        driver.quit()
        return

    try:
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "searchIframe")))
        first_place = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul > li")))
        link_in_place = first_place.find_element(By.CSS_SELECTOR, "a")
        link_in_place.click()
    except:
        pass

    driver.switch_to.default_content()
    try:
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "entryIframe")))
    except:
        print("entryIframe 진입 실패", file=sys.stderr)
        driver.quit()
        return

    # 기본 정보 추출
    try:
        title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.GHAhO"))).text
        category = driver.find_element(By.CSS_SELECTOR, "span.lnJFt").text
    except:
        title = category = ""

    # 메뉴 탭 클릭
    try:
        menu_tabs = driver.find_elements(By.CSS_SELECTOR, ".veBoZ")
        for tab in menu_tabs:
            if tab.text.strip() == "메뉴":
                tab.click()
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".lPzHi, .tit")))
                break
    except:
        pass

    # 메뉴 추출
    menu_list = []
    
    try:
        menu_names = driver.find_elements(By.CSS_SELECTOR, ".lPzHi")
        if not menu_names:
            menu_names = driver.find_elements(By.CSS_SELECTOR, ".store_delivery .tit")

        menu_prices = driver.find_elements(By.CSS_SELECTOR, ".GXS1X em")
        if not menu_prices:
            menu_prices = driver.find_elements(By.CSS_SELECTOR, ".store_delivery .price > strong")

        for name, price in zip(menu_names, menu_prices):
            menu_list.append({
                "name": name.text.strip(),
                "price": price.text.strip()
            })
    except Exception as e:
        print("❌ 메뉴 추출 실패:", e)
    
    
    try:
        review_tabs = driver.find_elements(By.CSS_SELECTOR, ".veBoZ")
        
        clicked_review = False
        for tab in review_tabs:
            if tab.text.strip() == "리뷰":
                tab.click()
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".pui__vn15t2 a")))
                clicked_review = True
                break
        
        # ➕ 대체 시도: .tan_inner span들에서 '리뷰' 찾아 클릭
        if not clicked_review:
            fallback_spans = driver.find_elements(By.CSS_SELECTOR, ".tab_inner span")
            for span in fallback_spans:
                if span.text.strip() == "리뷰":
                    driver.execute_script("arguments[0].click();", span) 
                    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".pui__vn15t2 a")))
                    break
    except:
        pass

    # 리뷰 탭 클릭
    try:
        review_tabs = driver.find_elements(By.CSS_SELECTOR, ".veBoZ")
        print(review_tabs,'리뷰탭')
        for tab in review_tabs:
            if tab.text.strip() == "리뷰":
                tab.click()
                
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".pui__vn15t2 a")))
                break
    except:
        pass
    # 리뷰 더보기 버튼 반복 클릭
    try:
        max_reviews = 30
        clicked = 0
        while True:
            current_reviews = driver.find_elements(By.CSS_SELECTOR, ".pui__vn15t2 a")
            if len(current_reviews) >= max_reviews:
                break
            try:
                more_button = driver.find_element(By.CSS_SELECTOR, ".fvwqf")
                driver.execute_script("arguments[0].click();", more_button)
                wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, ".pui__vn15t2 a")) > len(current_reviews))
                clicked += 1
            except:
                break
            if clicked >= 5:
                break
    except:
        pass

    # 리뷰 추출
    review_list = []
    try:
        review_blocks = driver.find_elements(By.CSS_SELECTOR, ".pui__vn15t2 a")
        for review in review_blocks:
            if review.text.strip() == "더보기":
                continue
            html_content = review.get_attribute("innerHTML")
            clean_text = html_content.replace("<br>", "\n").strip()
            review_list.append(clean_text)
    except:
        pass

    driver.quit()

    return {
        "title": title,
        "category": category,
        "menu": menu_list,
        "reviews": review_list
    }

if __name__ == "__main__":
    keyword = " ".join(sys.argv[1:])
    data = crawl_naver_place_info(keyword)
    print(json.dumps(data, ensure_ascii=False))
