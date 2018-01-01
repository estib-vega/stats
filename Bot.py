from __future__ import division
from datetime import datetime, timedelta
from ChromeDriver import ChromeDriver
import os
from analytics import get_followers_delta

class Bot(ChromeDriver):
    def __init__(self, username, password, max_total_likes_per_run=200, number_of_runs=5, wait_period_between_runs=40, likes_per_user=5, unfollow_after_days=3, max_new_follows=60):
        self.username = username
        self.password = password
        self.max_total_likes_per_run = max_total_likes_per_run
        self.number_of_runs = number_of_runs
        self.max_new_follows = max_new_follows
        self.wait_period_between_runs = wait_period_between_runs
        self.unfollow_after_days = unfollow_after_days
        self.usernames_to_ignore = []
        self.hashtags_to_like = []
        self.likes_overall = 0
        self.likes_dictionary = {}
        self.likes_per_user = likes_per_user
        self.file_names = {
            "followers": "followers/followers_{}_{}.txt",
            "cookies": "cookies.pkl",
            "likes": "likes/likes_{}.txt",
            "new_follows": "new_follows/{}.txt"
        }
        ChromeDriver.__init__(self)

    def today(self):
        return datetime.now().strftime("%Y-%m-%d")

    def get_post_links(self, max_links=10):
        link_tags = self.get_element_array("explore_post_links")
        links = []
        for link_tag in link_tags[:max_links]:
            link_attribute = self.browser_commands["link_attribute"]
            link = link_tag.get_attribute(link_attribute)
            links.append(link)
        return links

    def get_post_hashtags(self):
        hashtags = []
        tags = self.get_element_array("post_hashtag_link")
        for tag in tags:
            try:
                text_attribute = self.browser_commands["text_attribute"]
                a_inner_text = tag.get_attribute(text_attribute).strip()
                if a_inner_text.startswith("#"):
                    hashtag = a_inner_text[1:]
                    hashtags.append(hashtag)
            except Exception:
                pass
        return hashtags

    def follow_user(self, username):
        self.go_to_user_profile(username)
        follow_button = self.get_element("user_follow_button")
        inner_text = self.browser_commands["text_attribute"]
        text = follow_button.get_attribute(inner_text)
        if text.strip() != "Siguiendo" and text.strip() != "Pendiente":
            self.click("user_follow_button")

    def unfollow_user(self, username):
        self.go_to_user_profile(username)
        follow_button = self.get_element("user_follow_button")
        inner_text = self.browser_commands["text_attribute"]
        text = follow_button.get_attribute(inner_text)
        if text.strip() == "Siguiendo":
            self.click("user_follow_button")
            self.click("user_unfollow_window_unfollow_button")

    def get_post_creator(self):
        profile_link_tag = self.get_element("post_username_link")
        link_attribute = self.browser_commands["link_attribute"]
        profile_link = profile_link_tag.get_attribute(link_attribute)
        username = profile_link.split("/")[-2]
        return profile_link, username

    def log_like(self, username, post_link):
        likes_file_name = self.file_names["likes"].format(self.today())
        with open(likes_file_name, "a") as likes_file:
            likes_file.write("{},{},{}\n".format(username, post_link, datetime.now()))

    def like(self, post_link, username):
        self.go_to(post_link)
        self.log_like(username, post_link)
        self.click("post_like_button")
        self.likes_overall += 1
        print self.likes_overall

    def like_posts(self):
        creator_profile_link, username = self.get_post_creator()
        if username in self.usernames_to_ignore:
            print "should ignore:", username
            return
        print "liking posts from:", username
        self.go_to(creator_profile_link)
        post_links = self.get_post_links()
        for post_link in post_links[:self.likes_per_user]:
            try:
                if self.likes_overall >= self.max_total_likes_per_run: return
                self.like(post_link, username)
            except Exception:
                print "could not like"


    def like_post_creator(self, post_link):
        self.go_to(post_link)
        post_hashtags = self.get_post_hashtags()
        for hashtag in post_hashtags:
            if hashtag in self.hashtags_to_like:
                print "contains hashtag", hashtag
                self.like_posts()
                return

    def like_explore_posts(self):
        if self.likes_overall >= self.max_total_likes_per_run: return

        explore = self.addresses["explore"]
        self.go_to(explore)
        post_links = self.get_post_links()
        for post_link in post_links:
            self.like_post_creator(post_link)

    def get_liked_today(self, today):
        try:
            likes_file_name = self.file_names["likes"].format(today)
            likes = set()
            with open(likes_file_name) as likes_file:
                for line in likes_file:
                    username, _, _ = line.strip().split(",")
                    likes.add(username)
            return list(likes)
        except Exception:
            return []

    def get_followers_for(self, username, write_to_file=True, now=None):
        print datetime.now()
        self.go_to_user_profile(username)
        self.click("user_followers_link")

        followers_window = self.get_element("user_followers_window")

        self.scroll_through_window(followers_window)

        followers = []
        follower_links = self.get_element_array("user_followers_window_username_link")
        for follower_link in follower_links:
            text_selector = self.browser_commands["text_attribute"]
            usrnm = follower_link.get_attribute(text_selector).strip()
            if usrnm == "": continue
            followers.append(usrnm)

        if write_to_file:
            followers_file_name = self.file_names["followers"].format(username, now.strftime("%Y-%m-%d"))
            if os.path.exists(followers_file_name):
                os.remove(followers_file_name)
            with open(followers_file_name, "a") as followers_file:
                for follower in followers:
                    followers_file.write("{}\n".format(follower))

        print "Followers: {}".format(len(followers))
        self.click("user_followers_window_close_button")
        print datetime.now()
        return followers

    def follow_new_followers(self, now):
        today = now.strftime("%Y-%m-%d")
        yesterday_time = now - timedelta(1)
        yesterday = yesterday_time.strftime("%Y-%m-%d")

        yesterdays_followers = self.file_names["followers"].format(self.username, yesterday)
        today_followers = self.file_names["followers"].format(self.username, today)

        new_followers, _ = get_followers_delta(yesterdays_followers, today_followers)
        print len(new_followers), "new followers"

        return len(new_followers)

    def unfollow_past_followers(self, now):
        past_time = now - timedelta(self.unfollow_after_days)
        past = past_time.strftime("%Y-%m-%d")
        print "unfollowing from day", past, self.unfollow_after_days
        past_new_follows = self.file_names["new_follows"].format(past)
        if os.path.exists(past_new_follows):
            with open(past_new_follows) as past_followers_file:
                for past_follower in past_followers_file:
                    try:
                        self.unfollow_user(past_follower)
                    except Exception as e:
                        print e

    def explore(self):
        try:
            now = datetime.now() - timedelta(1)
            self.start_session(cookie_file=self.file_names["cookies"])
            self.get_followers_for(self.username, now=now)
            number_of_new_followers = self.follow_new_followers(now)

            past_liked_usernames = []
            for day in range(14):
                now = datetime.now() - timedelta(day + 1)
                liked_past = self.get_liked_today(now.strftime("%Y-%m-%d"))
                past_liked_usernames = list(set(past_liked_usernames + liked_past))

            is_tomorrow = False
            while not is_tomorrow:
                today = now.strftime("%d")
                maybe_tomorrow = datetime.now().strftime("%d")
                if today != maybe_tomorrow:
                    is_tomorrow = True
                    continue
                print "waiting for tomorrow"
                self.wait(15 * 60)



            for run in range(self.number_of_runs):
                liked_today = self.get_liked_today(self.today())
                self.usernames_to_ignore = list(set(past_liked_usernames + liked_today))

                while self.likes_overall < self.max_total_likes_per_run:
                    self.like_explore_posts()

                self.likes_overall = 0
                seconds_to_wait = self.wait_period_between_runs * 60
                if run != self.number_of_runs - 1:
                    self.wait(seconds_to_wait)

        except Exception as e:
            print e
        print "ended"
        print "new followers", number_of_new_followers
        self.end_session()

if __name__ == "__main__":
    bot = Bot("estib_vega", "")
    bot.start_session(cookie_file=bot.file_names["cookies"])
    now = datetime.now()
    #bot.unfollow_past_followers(now)
    # bot.unfollow_past_followers(now - timedelta(1))
    # bot.unfollow_past_followers(now - timedelta(2))
    bot.unfollow_past_followers(now - timedelta(3))