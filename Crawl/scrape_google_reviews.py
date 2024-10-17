from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

# Khởi tạo driver với Service và Options
def init_driver(driver_path):
    service = Service(executable_path=driver_path)
    chrome_options = Options()
    chrome_options.add_argument("--log-level=3")  # Tắt bớt log của Chrome
    return webdriver.Chrome(service=service, options=chrome_options)

# Hàm lấy thông tin đánh giá từ một tập kết quả
def get_review_summary(result_set):
    rev_dict = {'Review Name': [], 'Review Text': [], 'Review Time': [], 'Rating': []}
    for result in result_set:
        review_name = result.find(class_='d4r55').text if result.find(class_='d4r55') else 'N/A'
        review_text_elements = result.find_all('span', class_='wiI7pd')
        review_text = ' '.join([text_element.get_text(separator=' ', strip=True).replace('\n', ' ') for text_element in review_text_elements]) if review_text_elements else 'N/A'
        review_time = result.find('span', class_='rsqaWe').text if result.find('span', class_='rsqaWe') else 'N/A'
        star_rating = result.find('span', class_='kvMYJc')['aria-label'] if result.find('span', class_='kvMYJc') else 'N/A'
        rev_dict['Review Name'].append(review_name)
        rev_dict['Review Text'].append(review_text)
        rev_dict['Review Time'].append(review_time)
        rev_dict['Rating'].append(star_rating)
    return pd.DataFrame(rev_dict)

# Hàm mở rộng các đánh giá bằng cách bấm vào nút "Thêm"
def expand_reviews(driver):
    try:
        more_buttons = driver.find_elements(By.CLASS_NAME, 'w8nwRe')
        for button in more_buttons:
            driver.execute_script("arguments[0].click();", button)
            time.sleep(1)
    except Exception as e:
        print(f"Error expanding reviews: {e}")

# Hàm cuộn trang để tải toàn bộ nội dung đánh giá
def scroll_reviews(driver, scrollable_div, pause_time=3):
    last_height = driver.execute_script("return arguments[0].scrollHeight;", scrollable_div)
    while True: 
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", scrollable_div)
        time.sleep(pause_time)
        new_height = driver.execute_script("return arguments[0].scrollHeight;", scrollable_div)
        if new_height == last_height:
            break 
        last_height = new_height 

# Hàm lưu dữ liệu vào file CSV
def save_to_csv(df, folder_name='data', file_name='Viettel_reviews_crawldata.csv'):
    folder_path = folder_name
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    file_path = os.path.join(folder_path, file_name)
    
    # Kiểm tra file có tồn tại hay không
    file_exists = os.path.isfile(file_path)
    existing_df = pd.read_csv(file_path, encoding='utf-8') if file_exists else pd.DataFrame(columns=['Review Name', 'Review Text', 'Review Time', 'Rating'])
    
    # Gộp dữ liệu mới và cũ, loại bỏ các bản ghi trùng lặp
    combined_df = pd.concat([existing_df, df], ignore_index=True).drop_duplicates()
    combined_df.to_csv(file_path, index=False, encoding='utf-8-sig')  # Lưu với utf-8-sig để tránh lỗi tiếng Việt

# Hàm chính để crawl dữ liệu từ các URL
def crawl_reviews(urls):
    final_df = pd.DataFrame()

    # Khởi tạo driver
    driver = init_driver(driver_path)
    
    for url in urls:
        driver.get(url)
        time.sleep(5)
        
        # Nhấp vào phần đánh giá nếu có
        try:
            driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div/div/div/button[2]/div[2]').click()
        except Exception as e:
            print(f"Error clicking on reviews: {e}")
        time.sleep(3)

        # Cuộn trang để tải toàn bộ đánh giá
        scrollable_div = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[3]')
        scroll_reviews(driver, scrollable_div)

        # Mở rộng đánh giá nếu cần
        expand_reviews(driver)

        # Parse trang HTML để lấy nội dung
        response = BeautifulSoup(driver.page_source, 'html.parser')
        next_items = response.find_all('div', class_='jftiEf')
        df = get_review_summary(next_items)
        final_df = pd.concat([final_df, df], ignore_index=True)

    driver.quit()
    
    # Lưu dữ liệu vào file CSV
    save_to_csv(final_df)

# Đường dẫn đến file chromedriver.exe
driver_path = r"C:\Users\HP\Viettel Crawl\chromedriver.exe"

# URL để crawl dữ liệu
urls = ['https://www.google.com/maps/place/Viettel+C%E1%BA%A7n+Th%C6%A1/@10.0329256,105.7170117,13z/data=!4m10!1m2!2m1!1zdmlldHRlbCBj4bqnbiB0aMah!3m6!1s0x31a087e0e426752d:0xd552cf81220bd3d8!8m2!3d10.0501606!4d105.7872733!15sChJ2aWV0dGVsIGPhuqduIHRoxqEiA4gBAZIBI3RlbGVjb21tdW5pY2F0aW9uc19zZXJ2aWNlX3Byb3ZpZGVy4AEA!16s%2Fg%2F11c55jj7mh?hl=vi&entry=ttu&g_ep=EgoyMDI0MTAwMi4xIKXMDSoASAFQAw%3D%3D']

# Bắt đầu crawl
crawl_reviews(urls)
