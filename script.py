from __future__ import division
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from random import random, shuffle
import pickle
from analytics import get_followers_delta, get_like_data, get_follower_data
from Bot import Bot

username = "estib_vega"
password = ""

class AnalyticsBot:
    def __init__(self, username, password, min_wait=0.05, like_chance=100, max_total_likes=200):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome(executable_path=r"/Users/steve/Downloads/chromedriver")
        self.tags_to_explore = []
        self.min_wait = min_wait
        self.like_chance = like_chance
        self.max_total_likes = max_total_likes
        self.likes_overall = 0
        self.likes_dictionary = {}
        self.ignore = []
        self.should_check_probability = False

    def get_post_links(self):
        contents = self.driver.find_elements_by_xpath("//article/div/div/div/div/a")
        links = []
        for content_element in contents:
            link = content_element.get_attribute("href")
            links.append(link)
        return links



    def get_user_stats(self, username, back=True):
        self.driver.get("https://www.instagram.com/{}/?hl=es".format(username))

        publications_tag = self.driver.find_element_by_xpath("//header/section/ul/li[1]")
        followers_tag = self.driver.find_element_by_xpath("//header/section/ul/li[2]/a/span")
        followees_tag = self.driver.find_element_by_xpath("//header/section/ul/li[3]/a")

        pub = publications_tag.get_attribute("innerText").split()[0]
        follr = followers_tag.get_attribute("title") if followers_tag.get_attribute("title") else followers_tag.get_attribute("innerText").split()[0]
        follee = followees_tag.get_attribute("innerText").split()[0]
        if back: self.driver.back()
        publications = int(pub.replace(',', ''))
        followers = int(follr.replace(',', ''))
        followees = int(follee.replace(',', ''))
        return publications, followers, followees


    def exchange_cookies(self):
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        pickle.dump(self.driver.get_cookies(), open("cookies.pkl","wb"))


    

  

    def get_hastags(self):
        hashtags = []
        tags = self.driver.find_elements_by_xpath("//li[@role='menuitem']//a")
        for tag in tags:
            try:
                a_inner_text = tag.get_attribute("innerText").strip()
                if a_inner_text.startswith("#"):
                    hastag = a_inner_text[1:]
                    hashtags.append(hastag)
            except Exception:
                pass
        return hashtags

    def analytics(self):
        # self.driver.implicitly_wait(10) # seconds

        # self.driver.get("https://www.instagram.com")
        # self.exchange_cookies()

        _, staying_liked_follower, complete_like_data, complete_new_followers = get_follower_data()

        user_like_dictionary = {}
        tag_dictionary = {}

        for day in complete_like_data:
            for single_like in day:
                username, post_link, date = single_like
                user_like_dictionary.setdefault(username, []).append([post_link, date])

        # for username in staying_liked_follower:

        #     publications, followers, followees = self.get_user_stats(username, back=False)
        #     print username
        #     print publications, followers, followees
        #     ratio = followers / followees
        #     print ratio

        #     username_likes = user_like_dictionary[username]
        #     for single_likes in username_likes:
        #         post_link, date =  single_likes
        #         self.driver.get(post_link)
        #         hashtags = self.get_hastags()
        #         if len(hashtags) == 0:
        #             tag_dictionary.setdefault("##no_hastags##", 0)
        #             tag_dictionary["##no_hastags##"] += 1
        #         else:
        #             for hashtag in hashtags:
        #                 tag_dictionary.setdefault(hashtag, 0)
        #                 tag_dictionary[hashtag] += 1
                    
        #     print "\n"
        
        # with open("tags.txt", 'a') as tag_log:
        #     for tag in sorted(tag_dictionary.items(), key = lambda kv: (kv[1], kv[0]), reverse=True):
        #         try:
        #             tag_log.write("{},{}\n".format(tag[0], tag[1]))
        #         except Exception:
        #             pass

        for username in complete_new_followers:
            try:
                publications, followers, followees = self.get_user_stats(username, back=False)
                ratio = followers / followees
                print ratio
                links = self.get_post_links()
                for link in links:
                    self.driver.get(link)
                    hashtags = self.get_hastags()
                    if len(hashtags) == 0:
                        tag_dictionary.setdefault("##no_hastags##", 0)
                        tag_dictionary["##no_hastags##"] += 1
                    else:
                        for hashtag in hashtags:
                            tag_dictionary.setdefault(hashtag, 0)
                            tag_dictionary[hashtag] += 1

            except Exception:
                pass
           
        with open("tags.txt", 'a') as tag_log:
            for tag in sorted(tag_dictionary.items(), key = lambda kv: (kv[1], kv[0]), reverse=True):
                try:
                    tag_log.write("{},{}\n".format(tag[0], tag[1]))
                except Exception:
                    pass



        self.driver.close()
        
        

    def set_tags_to_explore(self, tags):
        self.tags_to_explore = tags


# analyticsBot = AnalyticsBot(username, password)


# analyticsBot.analytics()

# analyticsBot.set_tags_to_explore(["art", "artist", "drawing", "ilustration", "sketch", "photography"])

if __name__ == "__main__":
    bot = Bot(username, password, wait_period_between_runs=40)
    bot.hashtags_to_like = ["art", "artist", "drawing", "ilustration", "sketch", "photography", "graffiti"]
    bot.explore()