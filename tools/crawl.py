from tools.type import types,removeString,removeDyamic,selectDyamic,removeComment
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from time import sleep
import json
import os
import django
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs
from selenium.common.exceptions import TimeoutException, NoSuchElementException

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WebPython.settings')
django.setup()

from home.models import Post
from home.models import Comment

class Crawl:
    def __init__(self, browser, page):
        self.browser = browser
        self.page = page

    def get(self):
        self.browser.execute_script("document.body.style.zoom='0.2';")
        sleep(5)

        # like comment
            # Like and comment
        try:
            # Lấy số lượt like của fanpage
            like_element = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, './/a[contains(@href, "&sk=friends_likes") and contains(text(), "lượt thích")]'))
            )
            page_likes = like_element.text
            self.page.like_counts = page_likes

            # Lấy số lượt follow của fanpage
            follow_element = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, './/a[contains(@href, "&sk=followers") and contains(text(), "lượt theo dõi")]'))
            )
            page_follows = follow_element.text
            self.page.follow_counts = page_follows

            # Lưu dữ liệu vào database
            self.page.save()

        except TimeoutException:
            print('==> Không thể lấy số lượt like hoặc follow của fanpage: Quá thời gian chờ')
        except NoSuchElementException:
            print('==> Không thể lấy số lượt like hoặc follow của fanpage: Không tìm thấy phần tử')
        except Exception as e:
            print(f'==> Không thể lấy số lượt like hoặc follow của fanpage: {e}')

        pageLinkPost = f"{self.page.link}/posts/"
        pageLinkStory = "https://www.facebook.com/permalink.php"
        self.pageLinkPost = pageLinkPost
        self.pageLinkStory = pageLinkStory

        listPosts = self.browser.find_elements(By.XPATH, '//*[@aria-posinset]')
        if len(listPosts) > 5:
            listPosts = listPosts[:5]
        print(f"Có tổng: {len(listPosts)} bài post")

        post_links = []
        actions = ActionChains(self.browser)
        for p in listPosts:
            links = p.find_elements(By.CSS_SELECTOR, "a[attributionsrc]")
            for link in links:
                if link.size['width'] > 0 and link.size['height'] > 0:
                    actions.move_to_element(link).perform()
                    href = link.get_attribute('href')
                    if any(substring in href for substring in [pageLinkPost, pageLinkStory]):
                        post_links.append(href)
        
        if(len(post_links) > 0):
            self.checkPost(post_links)
        sleep(1)
    
    def checkPost(self, post_links):
        post_ids = []
        for link in post_links:
            if self.pageLinkPost in link:
                id = link.replace(self.pageLinkPost, '').split('?')[0]
                if id not in post_ids:
                    post_ids.append(id)
            elif self.pageLinkStory in link:
                parsed_url = urlparse(link)
                query_params = parse_qs(parsed_url.query)
                story_fbid = query_params.get('story_fbid', [None])[0]
                if story_fbid not in post_ids:
                    post_ids.append(story_fbid)

        print(f"=> Ra được: {len(post_links)}")
            
        existing_posts = Post.objects.filter(post_id__in=post_ids).values_list('post_id', flat=True)
        new_post_ids = [post_id for post_id in post_ids if post_id not in existing_posts]
        
        new_post_links = []
        for post_id in new_post_ids:
            for link in post_links:
                if post_id in link:
                    new_post_links.append({
                        'id': post_id,
                        'link': link
                    })
                    
        if new_post_links:
            for post in new_post_links:
                sleep(1)
                self.crawlPost(post)

    def crawlPost(self, postLink):
        data = {
            'post_id': postLink["id"],
            'link_facebook': postLink['link'],
            'page_id': self.page.id,
            'content': '',
            'media' : {
                'images': [],
                'videos': []
            },
            'share': 0,
            'comment': 0,
            'like': 0,
            'up': False,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        dataComment = []
        self.browser.get(f"{postLink['link']}")
        sleep(5)

        # Chờ cho modal xuất hiện
        modal = WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.XPATH, types['modal']))
        )
        # Lấy nội dung
        try:
            content = WebDriverWait(modal, 5).until(
                EC.visibility_of_element_located((By.XPATH, types['content']))
            )
            contentText = content.text
            for string in removeString:
                contentText = contentText.replace(string, '')
            data['content'] = contentText.strip()
        except:
            print(f'==> Bài post: {postLink["id"]} page: {self.page.link} không có nội dung!')
            pass

        # Lấy ảnh và video
        try:
            media = self.browser.find_element(By.XPATH,types['media'])
            images = media.find_elements(By.CSS_SELECTOR,'img')
            for img in images:
                src = img.get_attribute('src')
                if "emoji.php" not in src:
                    data['media']['images'].append(img.get_attribute('src'))
                
            videos = media.find_elements(By.CSS_SELECTOR,'video')
            for video in videos:
                data['media']['videos'].append(video.get_attribute('src'))
        except:
            print(f'==> Bài post: {postLink["id"]} page: {self.page.link} không ảnh hoặc video!')
        
        # Lấy lượng like, chia sẻ
        try:
            like_share_element = modal.find_element(By.XPATH, types['dyamic'])

            listCount = like_share_element.text
            for string in removeDyamic:
                listCount = listCount.replace(string, '')

            listCount = listCount.split('\n')
            if listCount:
                data['like'] = listCount[1] if len(listCount) > 1 else 0
                for dyamic in listCount:
                    if selectDyamic['comment'] in dyamic:
                        data['comment'] = dyamic
                    if selectDyamic['share'] in dyamic:
                        data['share'] = dyamic
        except:
            print(f'==> Bài post: {postLink["id"]} page: {self.page.link} không có lượng like hoặc chia sẻ!')

        # Lấy comment
        try:
            comments = modal.find_elements(By.CSS_SELECTOR, types['comments'])
            # Click vào các từ xem thêm
            for cm in comments:
                try:
                    xem_them = cm.find_element(By.XPATH, types['hasMore'])
                    if xem_them:
                        self.browser.execute_script("arguments[0].click();", xem_them)
                except:
                    pass
            countComment = 0
            for cm in comments:
                if countComment >= 10:
                    break
                textComment = ''
                try:
                    div_elements = cm.find_elements(By.XPATH, './div')[1]
                    div_2 = div_elements.find_elements(By.XPATH, './div')
                    if not div_2 or not div_2[0]: 
                        continue
                    textComment = div_2[0].text
                except:
                    countComment += 1
                    pass
                    
                for text in removeComment:
                    textComment = textComment.replace(text,'')

                textComment = textComment.strip()
                textArray = textComment.split('\n')

                if 'Fan cứng' in textComment:
                    user_name = textArray[1]
                    textContentComment = ' '.join(textArray[2:])
                else:
                    user_name = textArray[0]
                    textContentComment = ' '.join(textArray[1:])

                if user_name == '' or textContentComment == '':
                    continue

                countComment += 1
                dataComment.append({
                    'post_id': postLink["id"],
                    'user_name': user_name,
                    'content': textContentComment
                })

        except Exception as e:
            print(f'==> Bài post: {postLink["id"]} page: {self.page.link} không có bình luận!: {e}')

        self.insertPostAndComment(data,dataComment, postLink['link'])
        
    def insertPostAndComment(self, data, dataComment, link):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            data['media'] = json.dumps(data['media'])
            post = Post.objects.create(**data)
            post_id = post.id
            if len(dataComment) > 0:
                for comment in dataComment:
                    comment['post_id'] = post_id
                    Comment.objects.create(**comment)
        except Exception as e:
            with open('errors.log','a',encoding='utf-8') as file: 
                file.write(f"[{current_time}]: {e} \n")


    