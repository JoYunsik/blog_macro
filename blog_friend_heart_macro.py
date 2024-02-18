from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyperclip
naver_id = '2and1two'
password = 'moomoo0405'
keyword = '서이추'
option = 5  # option이 5면 (5+1)x16 = 96 개 하트 누르기
text = '우리 서로이웃추가해요~!'
wait_time = 10

browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
browser.get(
    "https://m.blog.naver.com/")
time.sleep(2)

# 이웃 새글 클릭
try:
    new_feed = WebDriverWait(browser, wait_time).until(
        EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, '이웃새글')))
except:
    browser.quit()
new_feed.click()

# 확인클릭
try:
    confirm_button = WebDriverWait(browser, wait_time).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div[4]/div/div/div/div[2]/a')))
except:
    browser.quit()
confirm_button.click()
# 네이버 로그인

try:
    elem_id = WebDriverWait(browser, wait_time).until(
        EC.presence_of_element_located((By.ID, 'id')))
except:
    browser.quit()

elem_id.click()
pyperclip.copy(naver_id)
elem_id.send_keys(Keys.CONTROL, 'v')

elem_pw = browser.find_element(By.ID, 'pw')
elem_pw.click()
pyperclip.copy(password)
elem_pw.send_keys(Keys.CONTROL, 'v')

browser.find_element(By.ID, 'log.login').click()

time.sleep(3)
# 스크롤 내리기
try:
    WebDriverWait(browser, wait_time).until(
        EC.title_is('네이버 블로그'))  # 네이버 블로그 화면으로 복귀하면 스크롤 내리기 시작
except:
    browser.quit()

for i in range(option):
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep(0.5)

time.sleep(1)

heart_buttons = browser.find_elements(By.CSS_SELECTOR, '.u_likeit_list_btn._button.off')

for heart_button in heart_buttons:
    browser.execute_script("arguments[0].click()",heart_button)
    
time.sleep(3)
browser.quit()
