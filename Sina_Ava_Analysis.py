# -*-coding:UTF-8-*-
# Author:jaylin
# File:Boxplot.py
# Time:2017/6/14 11:25
import pickle
import datetime
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


'''
all_data = [np.random.normal(0, std, 100) for std in range(1, 4)]

fig = plt.figure(figsize=(8,6))

plt.boxplot(all_data,
            notch=False, # box instead of notch shape
            #sym='rs',    # red squares for outliers
            vert=True)   # vertical box aligmnent

plt.xticks([y+1 for y in range(len(all_data))], ['x1', 'x2', 'x3'])
plt.xlabel('measurement x')
t = plt.title('Box plot')
plt.show()
'''

fr = open('result.pickle','rb')
data = pickle.load(fr)
fr.close()
types = ['On','Sp','As','Lo','Ot','Ch','An','Ob','Sc','Ca','Sd','Pl']
print len(types)

def tweets_boxplot(types):
    tweets = []
    for i in range(12):
        tweets.append([])
    for item in data:
        for key in item.keys():
            # print item[key]["type"]
            try:
                tweets[int(item[key]["type"])].append(int(item[key]["Num_Tweets"]))
            except Exception as e:
                print e
    with open("analysis.txt","a") as f:
        f.write("tweets median:")
        f.write(str([np.median(item) for item in tweets]))
        #f.write(",".join([str(np.median(item)) for item in tweets]))
        f.write("\n")
    fig = plt.figure(figsize=(8, 6))
    plt.axis([-6, 6, 0, 4000])
    plt.boxplot(tweets,
                # notch=False, # box instead of notch shape
                # sym='rs',    # red squares for outliers
                # showmeans=True,
                vert=True)  # vertical box aligmnent

    plt.xticks([y + 1 for y in range(len(tweets))],types)
    plt.xlabel('Profile Image')
    plt.title('Tweets Boxplot')
    plt.show()

def ff_boxplot(types):
    ff = []
    for i in range(12):
        ff.append([])
    for item in data:
        for key in item.keys():
            # print item[key]["type"]
            try:
                ff[int(item[key]["type"])].append(float(item[key]["Num_Fans"]/float(item[key]["Num_Follows"])))
            except Exception as e:
                print e
    with open("analysis.txt","a") as f:
        f.write("FF median:")
        f.write(str([np.median(item) for item in ff]))
        #f.write(",".join([str(np.median(item)) for item in ff]))
        f.write("\n")
    fig = plt.figure(figsize=(8, 6))
    plt.axis([-6, 6, 0, 100])
    plt.boxplot(ff,
                # notch=False, # box instead of notch shape
                # sym='rs',    # red squares for outliers
                # showmeans=True,
                vert=True)  # vertical box aligmnent

    plt.xticks([y + 1 for y in range(len(ff))],types)
    plt.xlabel('Profile Image')
    plt.title('FF Boxplot')
    plt.show()

def gender_bar(types):

    total = []  # 12 * 2
    for i in range(12):
        total.append([0,0])

    for item in data:
        for key in item.keys():
            # print item[key]["type"]
            try:
                if item[key]["Gender"] == u'\u7537':
                    total[int(item[key]["type"])][0] +=1
                elif item[key]["Gender"] == u'\u5973':  # 女
                    total[int(item[key]["type"])][1] += 1
            except Exception as e:
                print e
        # print num_m+num_f
        # male.append(num_m/(num_m+num_f))
        # female.append(num_f/(num_m+num_f))
    for i in range(len(total)):
        total[i][0] = float(total[i][0])/(float(total[i][0])+float(total[i][1]))
        total[i][1] = 1 - total[i][0]
    total = np.array(total).T
    with open("analysis.txt","a") as f:
        f.write("Gender distribution(male first):")
        f.write(str(total))
        f.write("\n")
    f, ax1 = plt.subplots(1, 1, figsize=(10, 5))

    bar_width = 0.5

    # positions of the left bar-boundaries
    bar_l = [i + 1 for i in range(12)]
    bar_l = np.array(bar_l)

    # positions of the x-axis ticks (center of the bars as bar labels)
    tick_pos = [i + (bar_width / 2) for i in bar_l]

    ax1.bar(bar_l+bar_width/2, total[0], width=bar_width,
            label='male', alpha=0.5, color='b')
    ax1.bar(bar_l+bar_width/2, total[1], width=bar_width,
            bottom=total[0], label='female', alpha=0.5, color='r')
    # ax1.bar(bar_l, green_data, width=bar_width,
    #         bottom=[i + j for i, j in zip(blue_data, red_data)], label='green data', alpha=0.5, color='g')

    plt.sca(ax1)
    plt.xticks(tick_pos, types)

    ax1.set_ylabel("Percent")
    ax1.set_xlabel("Profile Image")
    plt.legend(loc='upper left')
    plt.xlim([min(tick_pos) - bar_width, max(tick_pos) + bar_width])
    plt.grid()
    #plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

    plt.show()

def age_boxplot(types):
    age = []
    date = datetime.datetime.now()
    for i in range(12):
        age.append([])
    num = 0
    for item in data:
        for key in item.keys():
            # print item[key]["type"]
            try:
                age_temp = (date-item[key]["Birthday"]).days/365
                age[int(item[key]["type"])].append(float(age_temp))
                num += 1
            except Exception as e:
                print e
    with open("analysis.txt","a") as f:
        f.write("age median:")
        f.write(str([np.median(item) for item in age]))
        #f.write(",".join([str(np.median(item)) for item in ff]))
        f.write("\n")
        f.write("年龄四分位点：")
        f.write(str([np.percentile(item,75) for item in age]))
        f.write("\n")
        f.write("年龄最大值点：")
        f.write(str([np.percentile(item,100) for item in age]))
        f.write("\n")
        f.write("总人数：5663,生日缺失人数：%s"%(5663-num))
        f.write("\n")
    fig = plt.figure(figsize=(8, 6))
    plt.axis([-6, 6, 15, 45])
    plt.boxplot(age,
                # notch=False, # box instead of notch shape
                # sym='rs',    # red squares for outliers
                # showmeans=True,
                vert=True)  # vertical box aligmnent

    plt.xticks([y + 1 for y in range(len(age))],types)
    plt.xlabel('Profile Image')
    plt.title('Age Boxplot')
    plt.show()

def fans_boxplot(types):
    fans = []
    for i in range(12):
        fans.append([])
    for item in data:
        for key in item.keys():
            # print item[key]["type"]
            try:
                num_fans = item[key]["Num_Fans"]
                #print num_fans
                fans[int(item[key]["type"])].append(int(num_fans))
            except Exception as e:
                #print "xxx"
                print e
    with open("analysis.txt", "a") as f:
        f.write("fans_num median:")
        f.write(str([np.median(item) for item in fans]))
        # f.write(",".join([str(np.median(item)) for item in ff]))
        # f.write("\n")
        # f.write("总人数：5663,生日缺失人数：%s" % (5663 - num))
        f.write("\n")
    fig = plt.figure(figsize=(8, 6))
    plt.axis([-6, 6, 15, 12000])
    plt.boxplot(fans,
                # notch=False, # box instead of notch shape
                # sym='rs',    # red squares for outliers
                # showmeans=True,
                vert=True)  # vertical box aligmnent

    plt.xticks([y + 1 for y in range(len(fans))], types)
    plt.xlabel('Profile Image')
    plt.title('Fans_Num Boxplot')
    plt.show()

def tweets_like_boxplot(types):
    tweets_like = []
    for i in range(12):
        tweets_like.append([])
    for item in data:
        for key in item.keys():
            # print item[key]["type"]
            try:
                mean_Like = item[key]["Mean_Like"]
                #print num_fans
                if mean_Like != 0.0:
                    print mean_Like
                    tweets_like[int(item[key]["type"])].append(mean_Like)
            except Exception as e:
                #print "xxx"
                print e
    with open("analysis.txt", "a") as f:
        f.write("Tweets_Like median:")
        f.write(str([np.median(item) for item in tweets_like]))
        # f.write(",".join([str(np.median(item)) for item in ff]))
        # f.write("\n")
        # f.write("总人数：5663,生日缺失人数：%s" % (5663 - num))
        f.write("\n")
    fig = plt.figure(figsize=(8, 6))
    plt.axis([-6, 6, 0, 80])
    plt.boxplot(tweets_like,
                # notch=False, # box instead of notch shape
                # sym='rs',    # red squares for outliers
                # showmeans=True,
                vert=True)  # vertical box aligmnent

    plt.xticks([y + 1 for y in range(len(tweets_like))], types)
    plt.xlabel('Profile Image')
    plt.title('Tweets_Like Boxplot')
    plt.show()

def tweets_comments_boxplot(types):
    tweets_comments = []
    for i in range(12):
        tweets_comments.append([])
    for item in data:
        for key in item.keys():
            # print item[key]["type"]
            try:
                mean_comment = item[key]["Mean_Comment"]
                #print num_fans
                if mean_comment != 0.0:
                    print mean_comment
                    tweets_comments[int(item[key]["type"])].append(mean_comment)
            except Exception as e:
                #print "xxx"
                print e
    with open("analysis.txt", "a") as f:
        f.write("Tweets_Comment median:")
        f.write(str([np.median(item) for item in tweets_comments]))
        # f.write(",".join([str(np.median(item)) for item in ff]))
        # f.write("\n")
        # f.write("总人数：5663,生日缺失人数：%s" % (5663 - num))
        f.write("\n")
    fig = plt.figure(figsize=(8, 6))
    plt.axis([-6, 6, 0, 20])
    plt.boxplot(tweets_comments,
                # notch=False, # box instead of notch shape
                # sym='rs',    # red squares for outliers
                # showmeans=True,
                vert=True)  # vertical box aligmnent

    plt.xticks([y + 1 for y in range(len(tweets_comments))], types)
    plt.xlabel('Profile Image')
    plt.title('Tweets_Comment Boxplot')
    plt.show()

def tweets_transfer_boxplot(types):
    tweets_transfer = []
    for i in range(12):
        tweets_transfer.append([])
    for item in data:
        for key in item.keys():
            # print item[key]["type"]
            try:
                mean_transfer = item[key]["Mean_Trandfer"]
                #print num_fans
                if mean_transfer != 0.0:
                    print mean_transfer
                    tweets_transfer[int(item[key]["type"])].append(mean_transfer)
            except Exception as e:
                #print "xxx"
                print e
    with open("analysis.txt", "a") as f:
        f.write("Tweets_Transfer median:")
        f.write(str([np.median(item) for item in tweets_transfer]))
        # f.write(",".join([str(np.median(item)) for item in ff]))
        # f.write("\n")
        # f.write("总人数：5663,生日缺失人数：%s" % (5663 - num))
        f.write("\n")
    fig = plt.figure(figsize=(8, 6))
    plt.axis([-6, 6, 0, 20])
    plt.boxplot(tweets_transfer,
                # notch=False, # box instead of notch shape
                # sym='rs',    # red squares for outliers
                # showmeans=True,
                vert=True)  # vertical box aligmnent

    plt.xticks([y + 1 for y in range(len(tweets_transfer))], types)
    plt.xlabel('Profile Image')
    plt.title('Tweets_Transfer Boxplot')
    plt.show()

#tweets_boxplot(types)
#ff_boxplot(types)

#gender_bar(types)
age_boxplot(types)
#fans_boxplot(types)
#tweets_like_boxplot(types)
#tweets_comments_boxplot(types)
#tweets_transfer_boxplot(types)



