def get_followers_delta(file_1, file_2):
    followers_1 = []
    followers_2 = []
    new_followers = []
    lost_followers = []
    with open(file_1) as first:
        for username in first:
            followers_1.append(username.rstrip())

    with open(file_2) as second:
        for username in second:
            followers_2.append(username.rstrip())

    for username in followers_2:
        if username not in followers_1:
            new_followers.append(username.rstrip())
    
    for username in followers_1:
        if username not in followers_2:
            lost_followers.append(username.rstrip())
    
    return new_followers, lost_followers


def get_like_data(file):
    like_data = []
    with open(file) as f:
        for line in f:
            line_list = line.split(',')
            username, post_link, datetime = line_list
            like_data.append([username.rstrip(), post_link.rstrip(), datetime.rstrip()])
    return like_data

def get_follower_data():
    import os
    followers_logs = os.listdir("followers")
    followers_logs.sort()
    likes_logs = os.listdir("likes")
    n = len(followers_logs)
    i = 0
    complete_new_followers = []
    complete_lost_followers = []
    while i <= (n - 2):
        file_1 = "followers/{}".format(followers_logs[i])
        file_2 = "followers/{}".format(followers_logs[i + 1])
        new_followers, lost_followers = get_followers_delta(file_1, file_2)

        complete_new_followers += new_followers
        complete_lost_followers += lost_followers

        # print file_1
        # print "new followers:", len(new_followers), "lost followers:", len(lost_followers)
        # net_gain = (len(new_followers) - len(lost_followers))
        # print "net gain:", net_gain
        i += 1
    
    total_new_followers = len(set(complete_new_followers))
    total_lost_followers = len(set(complete_lost_followers))
    # print "total new followers:", total_new_followers, "total lost followers:", total_lost_followers

    total_new_staying_followers = [item for item in set(complete_new_followers) if item not in set(complete_lost_followers)]

    # print "staying:", len(total_new_staying_followers)

    n = len(likes_logs)
    i = 0
    complete_like_data = []
    liked_follower = set()
    staying_liked_follower = set()
    for liked_file in likes_logs:
        file = "likes/{}".format(liked_file)
        like_data = get_like_data(file)
        for single_like in like_data:
            username = single_like[0]
            if username in set(complete_new_followers):
                liked_follower.add(username)
            if username in total_new_staying_followers:
                staying_liked_follower.add(username)
        complete_like_data.append(like_data)


    return liked_follower, staying_liked_follower, complete_like_data, complete_new_followers

if __name__ == "__main__":
    import os
    followers_logs = os.listdir("followers")
    followers_logs.sort()
    likes_logs = os.listdir("likes")
    n = len(followers_logs)
    i = 0
    complete_new_followers = []
    complete_lost_followers = []
    while i <= (n - 2):
        file_1 = "followers/{}".format(followers_logs[i])
        file_2 = "followers/{}".format(followers_logs[i + 1])
        new_followers, lost_followers = get_followers_delta(file_1, file_2)

        complete_new_followers += new_followers
        complete_lost_followers += lost_followers

        print file_1
        print "new followers:", len(new_followers), "lost followers:", len(lost_followers)
        net_gain = (len(new_followers) - len(lost_followers))
        print "net gain:", net_gain
        i += 1
    
    total_new_followers = len(set(complete_new_followers))
    total_lost_followers = len(set(complete_lost_followers))

    print "total new followers:", total_new_followers, "total lost followers:", total_lost_followers

    total_new_staying_followers = [item for item in set(complete_new_followers) if item not in set(complete_lost_followers)]

    print "staying:", len(total_new_staying_followers)

    n = len(likes_logs)
    i = 0
    # complete_like_data = []
    liked_follower = set()
    staying_liked_follower = set()
    for liked_file in likes_logs:
        file = "likes/{}".format(liked_file)
        like_data = get_like_data(file)
        for single_like in like_data:
            username = single_like[0]
            if username in set(complete_new_followers):
                liked_follower.add(username)
            if username in total_new_staying_followers:
                staying_liked_follower.add(username)
        # complete_like_data.append(like_data)

    print "liked followers:", len(liked_follower)
    print "liked staying followers:", len(staying_liked_follower)
    # print liked_follower
    print "---"
    # print staying_liked_follower


