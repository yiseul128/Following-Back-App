#from webdrivermanager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from UserInfo import chromedriverPath, username, password
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# might be better ways instead of lists of classes
users_xpath = "//div[@role='dialog']//div[contains(@class, '_ab8w') and contains(@class, '_ab94') and contains(@class, '_ab97') and contains(@class, '_ab9f') and contains(@class, '_ab9k') and contains(@class, '_ab9p') and contains(@class, '_ab9-') and contains(@class, '_aba8') and contains(@class, '_abcm')]"
suggestion_xpath = "//div[@role='dialog']//div[contains(@class, '_ab8s') and contains(@class, '_ab8w') and contains(@class, '_ab94') and contains(@class, '_ab99') and contains(@class, '_ab9f') and contains(@class, '_ab9m') and contains(@class, '_ab9p') and contains(@class, '_aba8') and contains(@class, '_abcm')]//div[contains(@class, '_ab8w') and contains(@class, '_ab94') and contains(@class, '_ab97') and contains(@class, '_ab9f') and contains(@class, '_ab9k') and contains(@class, '_ab9p') and contains(@class, '_ab9-') and contains(@class, '_aba8') and contains(@class, '_abcm')]"

def login(driver):
    username_el = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.NAME, "username"))
    )
    username_el.send_keys(username)
    password_el = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.NAME, "password"))
    )
    password_el.send_keys(password)
    password_el.send_keys(u'\ue007') # enter key

def nav_to_profile(driver):
    dropdown_alt = '[alt*="' + username + '"]'
    profile_href = '[href*=\"' + username + '\"]'
    click_btn(driver, dropdown_alt)
    click_btn(driver, profile_href)

def click_btn(driver, selector):
    element = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, selector)) # tuple => extra bracket
    )
    element.click()

def get_users(driver, n):
    global users_xpath

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, users_xpath))
    )

    scroll_down(driver, n)

    all_user_elems = driver.find_elements(By.XPATH, users_xpath)
    suggest_user_elems = driver.find_elements(By.XPATH, suggestion_xpath)
    user_elems = [x for x in all_user_elems if x not in suggest_user_elems]

    users = []
    for i in range(len(user_elems)):
        try:
            row_text = user_elems[i].text
            if("Follow" in row_text) or ("Remove" in row_text):
                name = row_text[:row_text.index("\n")]
                users += [name]
        except:
            print("exception")

    return users

def scroll_down(driver, n):
    global users_xpath, suggestion_xpath
    iter_count = 0

    while True:
        scroll_top_num = str(iter_count*1000)
        iter_count += 1
        driver.execute_script("document.querySelector('div[role=dialog] div._aano').scrollTop="+scroll_top_num)

        if n==len(driver.find_elements(By.XPATH, users_xpath)) - len(driver.find_elements(By.XPATH, suggestion_xpath)):
            return;

def __main__():
    s = Service(chromedriverPath)
    driver = webdriver.Chrome(service=s)
    driver.get("https://www.instagram.com/")
    time.sleep(1)

    login(driver)
    nav_to_profile(driver)

    followers_href = '[href*=\"' + username + '/followers/\"]'
    following_href = '[href*=\"' + username + '/following/\"]'
    close_label = '[aria-label="Close"]'
    followers_xpath = "//li[contains(@class, '_aa_5') and contains(., 'followers')]//span"
    following_xpath = "//li[contains(@class, '_aa_5') and contains(., 'following')]//span"

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, followers_xpath))
    )

    followers_num = int(driver.find_elements(By.XPATH, followers_xpath)[0].text)
    #print("er num:", followers_num)
    following_num = int(driver.find_elements(By.XPATH, following_xpath)[0].text)
    #print("ing num:", following_num)

    click_btn(driver, followers_href)
    followers_list = get_users(driver, followers_num)
    #print(followers_list);
    click_btn(driver, close_label)

    click_btn(driver, following_href)
    following_list = get_users(driver, following_num)
    #print(following_list);
    click_btn(driver, close_label)

    # find following not in followers
    not_following_back = [x for x in following_list if x not in followers_list]
    print("Users who do not follow you back:", not_following_back)

    time.sleep(600)

    return

__main__()