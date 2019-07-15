from __future__ import division
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
from datetime import datetime, timedelta
import pickle



class ChromeDriver:
    def __init__(self, headless=False):
        chrome_options = Options()

        if headless:
            chrome_options.add_argument("--headless")

        chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        self.min_seconds_of_wait_to_diplay = 15
        self.driver = webdriver.Chrome(executable_path=r"/Users/jvega/Documents/chromedriver", chrome_options=chrome_options)
        self.driver.implicitly_wait(10)

        self.addresses = {
            "landing_page": "https://www.instagram.com",
            "login": "https://www.instagram.com/accounts/login/?next=/explore",
            "explore": "https://www.instagram.com/explore",
            "username": "https://www.instagram.com/{}",
            "tag": "https://www.instagram.com/explore/tags/{}"
        }

        self.selectors = {
            "login_username_input": "//input[@name='username']",
            "login_password_input": "//input[@type='password']",
            "login_submit_button": "//button[@type='submit']",
            "post_like_button": "//article/div[2]/section/span/button[span[@aria-label='Like']]",
            "post_username_link": "//header/div/div/div/h2/a",
            "post_hashtag_link": "//li[@role='menuitem']//a",
            "post_creation_date": "//article/div[2]/div[2]//time",
            "user_publications_tag": "//header/section/ul/li[1]",
            "user_followers_link": "//header/section/ul/li[2]/a",
            "user_followees_link": "//header/section/ul/li[3]/a",
            "user_followers_window": "//div[@role='dialog']/div[2]",
            "user_followers_window_close_button": "//div[@role='dialog']/div/div/div/button",
            "user_followers_window_username_link": "//div[@role='dialog']/div/ul//a",
            "user_follow_button": "//header/section/div//button",
            "user_unfollow_window_unfollow_button": "//div[@role='presentation']/div[@role='dialog']//button",
            "explore_post_links": "//article/div/div/div/div/a"
        }

        self.browser_commands = {
            "link_attribute": "href",
            "text_attribute": "innerText",
            "title_attribute": "title",
            "date_attribute": "datetime",
            "scroll_top_attribute": "scrollTop",
            "scroll_height_attribute": "scrollHeight",
            "scroll_script": "arguments[0].scrollTop = arguments[1]"
        }

    def wait(self, seconds):
        now = datetime.now()
        wait_till = now + timedelta(seconds=seconds)
        if seconds > self.min_seconds_of_wait_to_diplay:
            print("waiting until", wait_till)
        sleep(seconds)

    def go_to(self, address):
        return self.driver.get(address)

    def go_to_user_profile(self, username):
        profile_link = self.addresses["username"].format(username)
        self.go_to(profile_link)

    def get_element(self, selector_name):
        selector = self.selectors[selector_name]
        return self.driver.find_element_by_xpath(selector)

    def get_element_array(self, selector_name):
        selector = self.selectors[selector_name]
        return self.driver.find_elements_by_xpath(selector)

    def write_into_text_input(self, selector_name, text):
        input_element = self.get_element(selector_name)
        input_element.clear()
        input_element.send_keys(text)

    def click(self, selector_name):
        element = self.get_element(selector_name)
        element.click()

    def execute_script(self, *args, **kwargs):
        self.driver.execute_script(*args)

    def login(self, username, password):
        login_address = self.addresses["login"]
        self.go_to(login_address)

        self.write_into_text_input("login_username_input", username)
        self.write_into_text_input("login_password_input", password)
        self.click("login_submit_button")

    def exchange_cookies(self, cookie_file):
        cookies = pickle.load(open(cookie_file, "rb"))
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        pickle.dump(self.driver.get_cookies(), open(cookie_file,"wb"))

    def start_session(self, username="", password="", cookie_file=""):
        landing_page = self.addresses["landing_page"]
        self.go_to(landing_page)
        self.exchange_cookies(cookie_file)
        self.session_start_time = datetime.now()

        # Should check if cookie file is provided, or if cookie expired and
        # needs to re-login

    def end_session(self):
        self.driver.close()

    def scroll_through_window(self, window, found_end_tolerance=10, step=400):
        top = self.browser_commands["scroll_top_attribute"]
        height = self.browser_commands["scroll_height_attribute"]

        scroll_top = window.get_attribute(top)

        found_end_count = 0
        while True:
            print(".")
            target_scroll = int(scroll_top) + step
            scroll_script = self.browser_commands["scroll_script"]
            self.execute_script(scroll_script, window, target_scroll)
            self.wait(0.3)

            if scroll_top == window.get_attribute(top):
                found_end_count += 1
                print("end?")
            elif scroll_top < window.get_attribute(height):
                found_end_count = 0
            if found_end_count == found_end_tolerance:
                print("this is the end")
                break
            scroll_top = window.get_attribute(top)

    def scroll_down_window(self):
        self.wait(2)
        scroll_by = 500
        script = "window.scrollBy(0,{})".format(scroll_by)
        for _ in range(10):
            self.execute_script(script)
            self.wait(1)