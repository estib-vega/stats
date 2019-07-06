from __future__ import division
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from random import random, shuffle
import pickle
# from analytics import get_followers_delta, get_like_data, get_follower_data
from Bot import Bot

username = "estib_vega"
password = ""

if __name__ == "__main__":
    bot = Bot(username, password, max_total_likes_per_run=200, number_of_runs=50)
    bot.hashtags_to_like = ["blackandwhite", "weddingday", "natgeo", "nightsky", "usa", "loveyourself", "videomaker", "animallove", "foodies"]
    bot.explore()