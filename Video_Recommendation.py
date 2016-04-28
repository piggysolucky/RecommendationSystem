import urllib
import json
from bs4 import BeautifulSoup
import requests
import csv
import binascii
import numpy
import random
import sys
import time
import pylab
from ap import *


def download_list_id():
    userNames = []
    # Get top 1000 users on youtube
    for pageNum in range(1, 11):
        usersUrl = "http://www.statsheep.com/p/Top-Subscribers?page=" + str(pageNum)
        usersPage = requests.get(usersUrl).text
        soup = BeautifulSoup(usersPage, 'lxml')
        dataTable = soup.find("table", class_="data-table")
        hyperlinks = dataTable.findAll("a")
        for link in hyperlinks:
            userNames += link.contents
    userNames = set(userNames)

    # Convert user names to user Id
    userIds = []
    for userName in userNames:
        url = "https://www.googleapis.com/youtube/v3/channels?part=contentDetails&forUsername=" + userName + "&key=AIzaSyDoXGmy_RpUY1cUYWCceN2kSWT4-vDZOaE"
        response = urllib.urlopen(url)
        channelIdInfo = json.loads(response.read())
        items = channelIdInfo["items"]
        userIds += [item["id"] for item in items]

    # Get the playlistIds in a channel's playlist
    channelPlaylistIds = []
    for userId in userIds:
        url = "https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId=" + userId + "&key=AIzaSyDoXGmy_RpUY1cUYWCceN2kSWT4-vDZOaE"
        response = urllib.urlopen(url)
        channelPlaylistInfo = json.loads(response.read())
        channelPlaylist = channelPlaylistInfo["items"]
        channelPlaylistIds += [item["id"] for item in channelPlaylist]

    with open("channelPlaylistIds.txt", 'w') as f:
        f.write('\n'.join(channelPlaylistIds))


def download_title_data():
    with open("channelPlaylistIds.txt", 'r') as f:
        channelPlaylistIds = map(lambda x: x.strip(), f.readlines())

    # Get the video titles in the playlist
    f = open("titles.csv", 'w')
    writer = csv.writer(f)
    for playlistId in channelPlaylistIds:
        url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=" + playlistId + "&key=AIzaSyDoXGmy_RpUY1cUYWCceN2kSWT4-vDZOaE&maxResults=50"
        try:
            response = urllib.urlopen(url)
            channelVideolistInfo = json.loads(response.read())
            videoList = channelVideolistInfo["items"]
        except:
            print url
            continue
        videoListSnippets = [item["snippet"] for item in videoList]
        title = [item["title"].encode('utf-8') for item in videoListSnippets]
        writer.writerow(title)
    f.close()


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_english(s):
    try:
        s.decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def refine_words(title):
    marks = map(chr, range(33, 48) + range(58, 65) + range(91, 97) + range(123, 127))
    for m in marks:
        title = title.replace(m, " ")

    word_list_raw = title.lower().split()
    word_list = []
    for word in word_list_raw:
        word = word.rstrip("\r\n")
        if word != '' and not is_number(word) and is_english(word) and word not in stop_words:
            word_list.append(word)

    return word_list


def load_data():
    with open("titles.csv", 'r') as f:
        reader = csv.reader(f)
        all_data = list(reader)

    useful_lines = []
    count = 0
    refined_lists = []
    for play_list in all_data:
        refined_titles = []
        for video in play_list:
            refined = refine_words(video)
            if len(refined) >= shingle_len:
                refined_titles.append(refined)
        if any(len(t) > 0 for t in refined_titles):
            refined_lists.append(refined_titles)
            useful_lines.append(count)
        count += 1

    with open("processed_titles.csv", 'w') as f:
        writer = csv.writer(f)
        writer.writerows(refined_lists)

    with open("good_titles.csv", 'w') as f:
        writer = csv.writer(f)
        for r in useful_lines:
            writer.writerow(all_data[r])

    return refined_lists


def get_shingle(word_list):
    shingles = []
    for i in range(len(word_list) - shingle_len + 1):
        shingle = " ".join(word_list[i: i + shingle_len])
        shingle_num = binascii.crc32(shingle) & 0xffffffff  # Hash the shingle to a 32-bit integer.
        shingles.append(shingle_num)

    return shingles


def get_shingles(play_list):
    result = map(get_shingle, play_list)
    shingles = []
    for r in result:
        if r:
            shingles += r

    return shingles


def true_jaccard(shingles):
    num = len(shingles)
    matrix = numpy.zeros((num, num))

    for i in range(num):
        for j in range(i + 1, num):
            s1, s2 = shingles[i], shingles[j]
            matrix[i, j] = len(set(s1).intersection(s2)) * 1.0 / len(set(s1).union(s2))
    return matrix


def min_hash(shingles, total_hash_num):
    max_shingle = 2 ** 32 - 1  # Record the maximum shingle ID that we assigned.
    next_prime = 4294967311
    coeff1 = random.sample(xrange(max_shingle), total_hash_num)
    coeff2 = random.sample(xrange(max_shingle), total_hash_num)

    signatures = []
    for article_shingle in shingles:  # loop each article
        signature = []
        for hash_i in range(total_hash_num):  # loop all hash functions, get min hashed value for each function
            minimum_hashed = numpy.inf
            for s in article_shingle:  # loop all shingles in this article, record the min one
                hashed_val = (coeff1[hash_i] * s + coeff2[hash_i]) % next_prime  # hash function
                if hashed_val < minimum_hashed:
                    minimum_hashed = hashed_val
            signature.append(minimum_hashed)

        signatures.append(signature)

    # calculate the estimates
    num = len(signatures)
    matrix = numpy.zeros((num, num))

    for i in range(num):
        for j in range(i + 1, num):
            s1, s2 = signatures[i], signatures[j]
            # print s1, s2
            match_count = 0
            for hash_num in range(total_hash_num):
                if s1[hash_num] == s2[hash_num]:
                    match_count += 1

            matrix[i, j] = match_count * 1.0 / total_hash_num

    return matrix


def compare_result(t, e):
    """mean-squared error between the true and the estimate similarity"""
    num = len(t)
    total = 0
    for i in range(num):
        for j in range(i + 1, num):
            total += (t[i, j] - e[i, j]) ** 2
    mse = total * 1.0 / num

    return mse


def user_based():
    shingles = []
    for d in data:
        shingles.append(get_shingles(d))

    for num_lists in [1000, 2000, 3000, 4000]:
        print num_lists
        s = shingles[:num_lists]
        t0 = time.time()
        t = true_jaccard(s)
        print "True similarity baseline cost", time.time() - t0, "s"

        MSES = []
        for k in [16, 32, 64, 128]:
            t0 = time.time()
            e = min_hash(s, k)
            print str(k) + "-minhash estimate of similarity cost", time.time() - t0, "s"

            mse = compare_result(t, e)
            print "MSE:", mse
            MSES.append(mse)
        print MSES


def asso_train(transactions, min_support, min_confidence):
    items, rules = runApriori(transactions, min_support, min_confidence)
    rules = sorted(rules, key=lambda (rule, confidence): confidence)[::-1]

    print len(rules), "rules are found. Saved to valid_rules.csv"
    with open("rules.csv", 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["given", "inferred", "confidence"])
        for r in rules:
            temp = [list(r[0][0]), list(r[0][1]), r[1]]
            writer.writerow(temp)

    return rules


def item_based():
    transactions = []
    for play_list in data:
        temp = []
        for t in play_list:
            temp += t
        transactions.append(list(set(temp)))

    for s in [0.015]:
        for num_lists in [4000]:
            print num_lists
            t = transactions[:num_lists]
            t0 = time.time()
            asso_train(t, s, 0.1)
            print "time cost:", time.time() - t0
            # e.g. start -> wars


if __name__ == '__main__':
    with open("SmartStoplist.txt") as f:
        stop_words = [word.strip() for word in f]
    shingle_len = 2
    data = load_data()
    # user_based()
    item_based()
