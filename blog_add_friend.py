from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyperclip
import time

naver_id = '2and1two'
password = 'moomoo0405'
keyword = '서이추'
option = 4 # option이 9번이면 (9+1)x20 = 200 개 블로그 이웃추가
text = '안녕하세요! 블로그 구경 왔다가 소통하고 싶어서 서이추 신청합니다. 좋은 하루 되세요!!!'
wait_time =10

# 창 띄우기
browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
browser.get("https://m.blog.naver.com/SectionPostSearch.naver?orderType=date&searchValue={0}".format(keyword))
time.sleep(2)

# 네이버 로그인
try:
    login_button1 = WebDriverWait(browser, wait_time).until(EC.presence_of_element_located((By.XPATH,'//*[@id="root"]/header/div[3]/button/i')))
except:
    browser.quit()
login_button1.click()

try:
    login_button2 = WebDriverWait(browser, wait_time).until(EC.presence_of_element_located((By.CLASS_NAME,'profile_login__W23Uv')))
except:
    browser.quit()
login_button2.click()

try:
    elem_id = WebDriverWait(browser, wait_time).until(EC.presence_of_element_located((By.ID,'id')))
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
    WebDriverWait(browser, wait_time).until(EC.title_is('네이버 블로그')) # 네이버 블로그 화면으로 복귀하면 스크롤 내리기 시작
except:
    browser.quit()

for i in range(option):
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep(0.5)

time.sleep(1)
# 블로그 아이디 수집
id_list=[]
for i in range((option+1)*20):
    address = browser.find_elements(By.CLASS_NAME, 'link__OVpnJ')[i].get_attribute('href')
    id_list.append(address.split('logId=')[1].split('&logNo')[0])

print(id_list)
print(len(id_list))

# 새탭으로 주소불러오기
for id in id_list:
    link = 'https://m.blog.naver.com/BuddyAddForm.naver?blogId={0}&returnUrl=https%253A%252F%252Fm.blog.naver.com%252FPostList.naver%253FblogId%253D{0}'.format(id)

    browser.execute_script('window.open("{0}");'.format(link))  #새 탭으로 열기
    #time.sleep(1)
    browser.switch_to.window(browser.window_handles[-1])  # 새로 연 탭으로 이동
    

    # 서로이웃추가 신청
    time.sleep(0.5)
    try:
        button = browser.find_element(By.ID, 'bothBuddyRadio')
        if button.get_attribute('ng-disabled') == 'true':
            browser.close()
            browser.switch_to.window(browser.window_handles[-1])
            continue
        button.click()
        
        textbox = browser.find_element(By.TAG_NAME, 'textarea')
        textbox.clear()
        textbox.send_keys(text)
        browser.find_element(By.CLASS_NAME,'btn_ok').click()
        time.sleep(1)
        browser.close()
        browser.switch_to.window(browser.window_handles[-1])
    except:
        time.sleep(1)
        browser.close()
        browser.switch_to.window(browser.window_handles[-1])








