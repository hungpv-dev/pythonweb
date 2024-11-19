from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from tools.type import push
import json
import requests
from io import BytesIO
import pyautogui
from PIL import Image

class Push:
    def __init__(self,browser):
        self.browser = browser
    
    def up(self, post):
        try:
            createPost = self.browser.find_element(By.XPATH,push['createPost'])
            createPost.click()
            sleep(1)
            input_element = self.browser.switch_to.active_element
            input_element.send_keys(post['content'])
            media = json.loads(post['media'])
            images = media['images']

            for src in images:
                self.browser.execute_script("window.open('');")
                self.browser.switch_to.window(self.browser.window_handles[1])
                self.browser.get(src)
                sleep(1)
                pyautogui.hotkey('ctrl', 'c')
                sleep(0.5)
                pyautogui.hotkey('ctrl', 'w')
                self.browser.switch_to.window(self.browser.window_handles[0])
                sleep(1)
                input_element.send_keys(Keys.CONTROL, 'v')
                sleep(1)
            sleep(5)
            submit_button = self.browser.find_element(By.XPATH, "//div[@aria-label='Đăng']")
            submit_button.click()
        except Exception as e:
            print(f'Lỗi khi đăng bài viết: {e}')
        sleep(1000)