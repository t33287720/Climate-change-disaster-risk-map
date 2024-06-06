#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from PIL import Image
import io

# URL
URL = "https://dra.ncdr.nat.gov.tw/Frontend/Tools/ShowMapBoxWMS#"
# 檔案名
KML = 'test.kml'
# KML xmlns
xmlns = 'http://www.opengis.net/kml/2.2'

# 創建 Edge WebDriver 
driver = webdriver.Edge()

# 打開網頁
driver.get(URL)

try:
    # 透明度按鈕
    wait = WebDriverWait(driver, 200)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[6]/ul/li[1]/button')))
    element.click()

    # 等待透明度視窗
    input_box = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="alphabox"]/div/div/input')))

    # 使用 JavaScript 設置 slider 的值為1
    script = """
    var input = arguments[0];
    var value = arguments[1];
    input.value = value;
    var event = new Event('input', { bubbles: true });
    input.dispatchEvent(event);
    event = new Event('change', { bubbles: true });
    input.dispatchEvent(event);
    """
    driver.execute_script(script, input_box, '1')

    # 確認值已更新
    output_value = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="rangevalueB"]')))
    print(f"输出框的值: {output_value.text}")
    
    # 透明度按鈕
    wait = WebDriverWait(driver, 50)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[6]/ul/li[1]/button')))
    element.click()

    print("透明度成功設置為1！")
    

except Exception as e:
    print(f"發生錯誤: {e}")


# 讀取並解析 KML 檔案
tree = ET.parse(KML)
root = tree.getroot()

# 定義命名空間
namespace = {'kml': xmlns}

# 初始化經度和緯度的列表
longitudes = []
latitudes = []


# 遍歷所有的 Placemark 標籤
for placemark in root.findall('.//kml:Placemark', namespace):
    # 找到 Point 標籤下的 coordinates 標籤
    point = placemark.find('.//kml:Point/kml:coordinates', namespace)
    if point is not None:
        coordinates = point.text.strip()
        lon, lat, _ = map(float, coordinates.split(','))
        longitudes.append(lon)
        latitudes.append(lat)

# 顯示經度和緯度
print("Longitudes:", longitudes)
print("Latitudes:", latitudes)
time.sleep(1)  # 等待1秒

try:
    for longitude, latitude, in zip(longitudes, latitudes):
        #點擊進階分析(展開)
        button_open = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/button')
        button_open.click()
        time.sleep(2)  # 等待2秒
        
        #點擊經緯度查詢
        button_open = driver.find_element(By.XPATH, '//*[@id="contact-tab"]')
        button_open.click()
        time.sleep(2)  # 等待2秒
        
        # 定義經緯度輸入框
        longitude_input = driver.find_element(By.XPATH, '//*[@id="Searchlongitude"]')
        latitude_input = driver.find_element(By.XPATH, '//*[@id="Searchlatitude"]')

        # 清除输入框的内容
        longitude_input.clear()
        latitude_input.clear()

        # 輸入經緯度
        longitude_input.send_keys(str(longitude))
        latitude_input.send_keys(str(latitude))
        
        # 點擊查詢
        button = driver.find_element(By.XPATH, '//*[@id="contact"]/div/div[4]/button')
        button.click()
        
        #點擊進階分析(收回)
        button_open = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/button')
        button_open.click()
        time.sleep(2)  # 等待2秒
    
        print("查詢成功！")
        try:
            time.sleep(2)  # 等待2秒
            
            # 抓取整個頁面節圖
            screenshot = driver.get_screenshot_as_png()
            img = Image.open(io.BytesIO(screenshot))
        
            # 讀取頁面尺寸
            width, height = img.size
        
            # 讀取頁面中間的顏色
            middle_pixel = img.getpixel((width // 2, height // 2))
            
            # 输出RGB
            print("顏色:", middle_pixel)
            if middle_pixel==(159, 0, 0):
                print(":第五級")
            elif middle_pixel==(202, 59, 0):
                print(":第四級")
            elif middle_pixel==(202, 125, 29):
                print(":第三級")
            elif middle_pixel==(202, 180, 83):
                print(":第二級")
            elif middle_pixel==(202, 202, 186):
                print(":第一級")
            else:
                print(":無")
            
        except Exception as e:
            print("發生錯誤:", e)

except Exception as e:
    print("發生錯誤:", e)

