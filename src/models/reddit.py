import requests
import datetime
import os
from webpreview import web_preview


MINIMUM_SCORE = 100

class Reddit(object):
    def get_configuration(self):
        conf = {}
        conf['token_user'] = os.environ['TOKEN_USER']
        conf['token_pw'] = os.environ['TOKEN_PW']
        conf['username'] = os.environ['USERNAME']
        conf['password'] = os.environ['PASSWORD']
        conf['user_agent'] = os.environ['USER_AGENT']
        return conf

    def __get_new_reddit_token_value(self):
        client_auth = requests.auth.HTTPBasicAuth(self.conf['token_user'], self.conf['token_pw'])
        post_data = {"grant_type": "password", "username": self.conf['username'], "password": self.conf['password']}
        headers = {"User-Agent": self.conf['user_agent'] }
        response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
        return response.json()["access_token"]

    def __init__(self, subreddit_list, sort='top', time='day', number_of_links=20):
        self.conf = self.get_configuration()
        self.access_token=self.__get_new_reddit_token_value()
        self.subreddit_list=subreddit_list
        self.sort=sort
        self.time=time
        self.number_of_links=number_of_links

    def create_request_query(self, subreddit, after=''):
        limit = min(100, self.number_of_links)
        reddit_api_url='https://oauth.reddit.com'
        query = '/r/{subreddit}/{sort}?sort={sort}&t={time}&limit={limit}&after={after}'.format(
                subreddit=subreddit, sort=self.sort, time=self.time, limit=limit, after=after
                )
        return reddit_api_url + query

    def get_posts_from_subreddit(self, subreddit, after):
        headers = {"Authorization": "bearer {}".format(self.access_token), "User-Agent": self.conf['user_agent']}
        query = self.create_request_query(subreddit, after)
        response = requests.get(query, headers=headers)
        return response.json()

    def determine_type(self, url):
        picture_ext = ('.jpg', '.png', '.tiff', '.jpeg', '.gif')
        video_ext = ('.gifv', '.mp4', '.mov', '.mkv', '.flv', '.wmv')
        if url.endswith(picture_ext):
            return 'picture'
        if url.endswith(video_ext):
            return 'video'
        return 'other'

    def structure_item(self, item, subreddit):
        url=item["data"]["url"]
        title, description, pic = web_preview(url, timeout=1000)
        score=item["data"]["score"]
        subreddit=item["data"]["subreddit"]
        date = datetime.datetime.today().isoformat()
        object_type = self.determine_type(url)
        log_msg = str(datetime.datetime.now().isoformat())+": Pulled from reddit"
        structured_item = {
                'url' : url,
                'subreddit' : subreddit,
                'description' : description,
                'picture' : pic,
                'score' : score,
                'date' : date,
                'title' : title,
                'uploaded': False,
                'last_status': log_msg,
                'type': object_type 
                }
        return structured_item

    def structure_collected_data(self, data, subreddit):
        structured_data = list()
        for item in data["data"]["children"]:
            structured_item = self.structure_item(item, subreddit)
            structured_data.append(structured_item)
        return structured_data

    def get_after_value(self, raw_data):
        return raw_data['data']['after']


    def collect_all_subreddit_data(self):
        data = list()
        for subreddit in self.subreddit_list:
            after=''
            for count in range(0, self.number_of_links, 100):
                raw_data = self.get_posts_from_subreddit(subreddit, after)
                data.extend(self.structure_collected_data(raw_data, subreddit))
                after = self.get_after_value(raw_data)
        return data


    def check_url_score(self, data):
        valid_data = list()
        for item in data:
            if item['score'] < MINIMUM_SCORE:
                continue
            valid_data.append(item)
        return valid_data


    def run(self):
        data = self.collect_all_subreddit_data()
        data = self.check_url_score(data)
        return data


