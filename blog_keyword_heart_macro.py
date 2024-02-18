from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyperclip
import time

naver_id = 'choys0528'
password = 'ys647393'
keyword = '서이추'
option = 0  # option이 9번이면 (9+1)x20 = 200 개 블로그 
text = '우리 서로이웃추가해요~!'
wait_time = 10

# 창 띄우기
browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
browser.get(
    "https://m.blog.naver.com/SectionPostSearch.naver?orderType=date&searchValue={0}".format(keyword))
time.sleep(2)

# 네이버 로그인
try:
    login_button1 = WebDriverWait(browser, wait_time).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/header/div[3]/button/i')))
except:
    browser.quit()
login_button1.click()

try:
    login_button2 = WebDriverWait(browser, wait_time).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'profile_login__W23Uv')))
except:
    browser.quit()
login_button2.click()

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
# 블로그 아이디 수집
address_list = []
for i in range((option+1)*20):
    address = browser.find_element(
        By.XPATH, '//*[@class="item__u7k_a"][{0}]//a'.format(i+1)).get_attribute('href')
    address_list.append(address)

print(address_list)
print(len(address_list))


# 새탭으로 주소불러오기
for address in address_list:

    browser.execute_script('window.open("{0}");'.format(address))  # 새 탭으로 열기
    # time.sleep(1)
    browser.switch_to.window(browser.window_handles[-1])  # 새로 연 탭으로 이동

    # 서로이웃추가 신청
    time.sleep(0.5)
    browser.find_element(By.CLASS_NAME, 'post_function_t1').click()
    try:
        button = browser.find_elements(
            By.CLASS_NAME, 'u_likeit_list_btn')[1]
        if button.get_attribute('aria-pressed') == 'true':
            browser.close()
            browser.switch_to.window(browser.window_handles[-1])
            continue
        browser.find_element(
            By.XPATH, '//*[@id="_tools_layer"]/ul/li[2]/div/div/a').click()

        time.sleep(0.5)
        browser.close()
        browser.switch_to.window(browser.window_handles[-1])
    except:
        time.sleep(1)
        browser.close()
        browser.switch_to.window(browser.window_handles[-1])


# try:
#     button = WebDriverWait(browser, wait_time).until(EC.presence_of_element_located(By.ID, 'bothBuddyRadio'))
# except:
#     browser.quit()
