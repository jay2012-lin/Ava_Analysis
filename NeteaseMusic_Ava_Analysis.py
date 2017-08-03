# -*- coding:utf-8 -*-
# 日期：2017/8/1 时间：下午4:28
# Author:Jaylin
# 根据原始数据统计各头像用户组的不同用户行为，并且使用matplotlib绘图
# 主要分析结果：
# 1、比例饼图／条形图
# 2、用户行为的均值表现表
# 3、FF(fans / follows)
# 4、CC(collects / create) 独自和总和
# 5、相关的歌单标签统计图
# 6、性别分布，tweets分布
import json,copy
import matplotlib.pyplot as plt
import os,pickle
import numpy as np
from collections import Counter
import matplotlib.font_manager as fm

dir_path = '../avatar'
type_name = ['Ce','As','On','Sp','Hf','Ba','An','Ot','Cc','Lo','Sc','Sd','Ob','Eg']
type_index = [3,10,2,5,8,1,4,9,7,11,12,14,6,13]
#首先统计各种类型出现的次数以及比例
def sta_each_type():
    type_index_ = [4,2,1,12,3,7,8,5,6,13,9,14,10,11]

    type_dir = os.listdir(dir_path)
    type_dir.remove('.DS_Store')  # 14个类
    num = 0
    num_dir = {}
    for type in type_dir:
        item_list = os.listdir((dir_path)+'/'+type)
        item_list.remove('.DS_Store')
        num_dir[type] = len(item_list)
        num += num_dir[type]

    print num
    for type in num_dir.keys():
        print type,"num is:",num_dir[type],float(num_dir[type])/num

    def cmp(x,y):
        # 注意这儿返回的是正负数／0 要用减号不能用大于小于号
        return int(x.split('_')[0]) - int(y.split('_')[0])

    type_list = num_dir.keys()
    type_list = sorted(type_list,cmp=cmp,reverse=False)
    # print type_list
    type_percent = [num_dir[item]/float(num)*100 for item in type_list]
    type_percent_ = []
    for i in range(len(type_percent)):
        type_percent_.append(type_percent[type_index_[i]-1])
    print type_percent_

    # 开始绘图
    x_pos = list(range(len(type_list)))
    plt.bar(x_pos,type_percent_,align='center',alpha=0.5)

    plt.grid()

    max_y = max(type_percent)
    plt.ylim([0,max_y*1.1])

    plt.ylabel('Percent')
    # rotation参数表示倾斜的角度
    # plt.xticks(x_pos,type_name,size='small',rotation=60)
    plt.xticks(x_pos,type_name,size='small',rotation=0)
    plt.title("Bar plot of each type's percent")

    for a,b in zip(x_pos,type_percent_):
        plt.text(a, b + 0.005, '%.1f' % b, ha='center', va='bottom', fontsize=7)

    # plt.savefig('../pic/type_percent.png')
    # 在show()之后调用导致保存的图片为空白 原因：在plt.show()后实际上已经创建了一个新的空白的图片（坐标轴）
    plt.show()

# sta_each_type()
# 绘制饼图
def plot_pie():
    type_percent = [8.415381757384358, 3.4088798067991823, 13.793423741408137, 11.285528515697568, 6.706297603566784, 2.4986067248746053, 3.4924763143228685, 4.607096414638677, 5.108675459780791, 0.9381385844324726, 4.92290544306149, 25.171837265465353, 4.551365409622886, 5.099386958944827]
    # 先画一个大范围 然后选择合适的比例
    fig = plt.figure(figsize=(3.5, 7.5))
    colors = ['peru',
              'brown',
              'royalblue',
              'deeppink',
              'lightpink',
              'yellow',
              'fuchsia',
              'olive',
              'gold',
              'darkkhaki',
              'blue',
              'cornflowerblue',
              'lawngreen',
              'tomato']
    plt.pie(
        type_percent,
        labels=type_name,
        #shadow=True,
        colors=colors,
        explode=(0.035, 0.035, 0.035, 0.035, 0.035, 0.035, 0.035, 0.035, 0.035, 0.035, 0.035, 0.035, 0.035, 0.035),  # space between slices
        startangle=90,  # rotate conter-clockwise by 90 degrees
        autopct='%1.1f%%',  # display fraction as percentag
        pctdistance=1.1,  # 百分比的距离 跟圆心的倍数关系
        labeldistance=5,  #文本离圆心的距离 大一点表示不需要
    )
    # plt.legend(fancybox=True)
    plt.legend(loc='lower center',frameon=False,fancybox=True,ncol=14,handlelength=0.6,handleheight=0.6,handletextpad=0.1,borderaxespad=0.6,columnspacing=0.6) # bbox_to_anchor=(0.1,0),
    plt.axis('equal')  # plot pyplot as circle
    plt.tight_layout()
    plt.show()

plot_pie()
# 下一步
# 1.将不同用户的各种行为信息整理存入pickle，以便以后的计算
# 2.计算歌单的标签空间，根据用户类别统计生成不同类别对应的标签向量（收藏和创建）、还有歌单的其他信息

# 先加载playlist信息，生成标签空间，然后逐步处理user的每一条信息，统计每个类的信息
# 每个用户的行为特征 id,special_description,playlist_create_no,playlist_collect_no,level,gender
# is_special,self_description,fans,follows,total_songs,activities,age,playlist_create,playlist_collect
# 歌单的所包含的项目：play,num_comments,share,songs_num,collected,tag,description
playlist_file = '../data/playlist.json'
user_file = '../data/User.json'
type_file = '../data/type_info.pickle'
def sta_user_activity():
    # 加载歌单文件
    playlist_dic = {}
    with open(playlist_file,'rb') as f:
        for line in f:
            playlist_info = json.loads(line)
            id = int(playlist_info['id'])
            playlist_dic[id] = playlist_info
            # break

    print '加载歌单文件结束，总记录为：%d'%len(playlist_dic.keys())
    print playlist_dic[759211740]
    playlist_keys = set(playlist_dic.keys())

    # 加载用户文件
    user_dic = {}
    with open(user_file,'rb') as f:
        for line in f:
            user_info = json.loads(line)
            id = int(user_info['id'])
            user_dic[id] = user_info

    print '加载用户信息文件结束，总记录为：%d'%len(user_dic.keys())

    # 所有的类别信息保存在以下字典中
    all_type_data = {}

    # 开始处理类别文件
    type_dir = os.listdir(dir_path)
    type_dir.remove('.DS_Store')  # 14个类
    print '总共有%d个用户种类！'%len(type_dir)
    for type in type_dir:
        type_info_list = []
        print '%s开始处理！' % type
        type_users = os.listdir(dir_path+'/'+type)
        type_users.remove('.DS_Store')
        type_users = [int(item[:-4]) for item in type_users]
        for user in type_users:
            user_info = user_dic[user]
            del user_info['_id']
            del user_info['ava_downloaded']
            del user_info['avatar_url']
            del user_info['location']
            del user_info['nickName']

            user_info['special_description'] = 0 if user_info['special_description'] == "" else 1
            user_info['self_description'] = 0 if user_info['self_description'] == "" else 1

            # 加载歌单信息
            create_list = user_info['playlist_create']
            collect_list = user_info['playlist_collect']

            create_list_user = {}
            collect_list_user = {}

            for playlist_item in create_list:
                playlist_item = int(playlist_item)
                if playlist_item in playlist_keys:
                    playlist_info = playlist_dic[playlist_item]
                    # print playlist_info
                    if '_id' in playlist_info.keys():
                        del playlist_info['_id']
                    if 'name' in playlist_info.keys():
                        del playlist_info['name']
                    if 'author' in playlist_info.keys():
                        del playlist_info['author']
                    if 'comments' in playlist_info.keys():
                        del playlist_info['comments']
                    if 'ava_downloaded' in playlist_info.keys():
                        del playlist_info['ava_downloaded']
                    if 'avatar_url' in playlist_info.keys():
                        del playlist_info['avatar_url']
                    if 'create_time' in playlist_info.keys():
                        del playlist_info['create_time']
                    # del playlist_info['description']
                    create_list_user[playlist_item] = playlist_info


            for playlist_item in collect_list:
                playlist_item = int(playlist_item)
                if playlist_item in playlist_keys:
                    playlist_info = playlist_dic[playlist_item]
                    if '_id' in playlist_info.keys():
                        del playlist_info['_id']
                    if 'name' in playlist_info.keys():
                        del playlist_info['name']
                    if 'author' in playlist_info.keys():
                        del playlist_info['author']
                    if 'comments' in playlist_info.keys():
                        del playlist_info['comments']
                    if 'ava_downloaded' in playlist_info.keys():
                        del playlist_info['ava_downloaded']
                    if 'avatar_url' in playlist_info.keys():
                        del playlist_info['avatar_url']
                    if 'create_time' in playlist_info.keys():
                        del playlist_info['create_time']
                    # del playlist_info['description']
                    collect_list_user[playlist_item] = playlist_info

            user_info['playlist_create'] = create_list_user
            user_info['playlist_collect'] = collect_list_user

            type_info_list.append(user_info)

        all_type_data[type] = type_info_list

        print '%s处理完毕！'%type

    with open(type_file,'wb') as f:
        pickle.dump(all_type_data,f)

#sta_user_activity()
# 检查统计文件是否正确
# with open(type_file,'rb') as f:
#     type_info = pickle.load(f)
#     print type_info['10_object'][0]
# {u'special_description': 0, u'playlist_create_no': u'19', u'playlist_collect_no': u'41', u'level': u'7', u'gender': u'1', u'is_special': 0, u'id': 100293966, u'self_description': 0, u'fans': u'2', u'playlist_collect': {80290112: {u'play': u'484579', u'description': u'\u4ecb\u7ecd\uff1a \u6b22\u8fce\u5927\u5bb6\u6536\u85cf\u8bc4\u8bba\u5206\u4eab\u3002 \u4e5f\u8bf7\u5927\u5bb6\u4e0d\u8981\u9519\u8fc7\u6211\u7684\u53e6\u4e00\u4e2a\u76f8\u540c\u98ce\u683c\u6b4c\u5355\u201c\u98de\u884c\u71c3\u6599\u201d\uff0c\u66f2\u76ee\u66f4\u65b0\uff0c\u66f4\u70b8\u3002 \u61c2\u8d27\u7684\u4eba\u90fd\u5173\u6ce8\u6211\u4e86\u7684Avilledd on Air\u7535\u53f0 ', u'num_comments': 179, u'share': u'298', u'songs_num': 280, u'tag': [u'\u6b27\u7f8e', u'\u9152\u5427', u'\u7535\u5b50'], u'collected': u'19367', u'id': u'80290112'}, 114100258: {u'play': u'53918', u'description': u'', u'num_comments': 46, u'share': u'22', u'songs_num': 39, u'tag': [], u'collected': u'3692', u'id': u'114100258'}, 36890629: {u'play': u'446647', u'description': u'\u4ecb\u7ecd\uff1a \u602a\u732bEP\u4e13\u8f91\u4e0d\u65ad\u66f4\u65b0\u300a\u8272\u73af\u7cfb\u5217\u5df2\u5b8c\u7ed3\u300b\u6ce8\uff1a\u7d2b\u73afDubstep,\u9ec4\u73afElectro,\u7eff\u73afGlitch Hop,\u9752\u73afHard Dance,\u7070\u73afEDM,\u6a59\u73afHouse,\u84dd\u73afTrance,\u7ea2\u73afDrum&Bass,\u6d0b\u7ea2\u73afDrumstep,\u6e56\u84dd\u73afNu Disco \u732b\u5382\u6700\u65b0\u7684\u7cfb\u5217\u5c01\u9762EP\u6b4c\u5355\u5df2\u4e0a\u7ebf\uff0c \u5206\u4e3a2015-2016\u4e00\u7cfb\u5217\u548c2016-2017\u7cfb\u5217\uff0c\u6b22\u8fce\u6536\u85cf\uff01\u6301\u7eed\u66f4\u65b0 ', u'num_comments': 362, u'share': u'360', u'songs_num': 147, u'tag': [u'\u6b27\u7f8e', u'\u7535\u5b50'], u'collected': u'20192', u'id': u'36890629'}, 33567239: {u'play': u'86035', u'description': u'\u4ecb\u7ecd\uff1a \u2605\u53ef\u98df\u7528\u6b4c\u5355\u2605\u4e0d\u52a0\u9632\u8150\u5242\u2605Weibo\uff1aDopeMusicCN ', u'num_comments': 38, u'share': u'20', u'songs_num': 1317, u'tag': [u'\u6b27\u7f8e', u'\u8bf4\u5531', u'\u9152\u5427'], u'collected': u'1249', u'id': u'33567239'}, 84130540: {u'play': u'45621', u'description': u'', u'num_comments': 27, u'share': u'22', u'songs_num': 40, u'tag': [], u'collected': u'3501', u'id': u'84130540'}, 318807436: {u'play': u'422426', u'description': u'\u4ecb\u7ecd\uff1a hiphop\u7ec3\u821e\uff0cparty\uff0c\u6bd4\u8d5b\u66f2\u76ee\u3002\u6301\u7eed\u66f4\u65b0\u3002 ', u'num_comments': 107, u'share': u'165', u'songs_num': 119, u'tag': [u'\u821e\u66f2'], u'collected': u'13847', u'id': u'318807436'}, 133484817: {u'play': u'356209', u'description': u'\u4ecb\u7ecd\uff1a \u4f5c\u4e3a\u4e00\u540dSkrillex\u7684\u4e50\u8ff7\u8fd9\u90fd\u662f\u672c\u4eba\u770b\u904dSkrillex\u5927\u795e\u8fd1\u51e0\u5e74\u6240\u6709\u7684\u73b0\u573a\u800c\u6536\u85cf\u7684\u7ecf\u5178\u66f2\u5b50\uff0c\u91cc\u9762\u5305\u542b\u4e86\u73b0\u573aRap\u8854\u63a5\u66f2\u548cTrap&Brostep\u7b49\u98ce\u683c\u7684\u66f2\u5b50\uff0c\u6211\u4f1a\u4e0d\u5b9a\u65f6\u7684\u66f4\u65b0 ', u'num_comments': 212, u'share': u'173', u'songs_num': 145, u'tag': [u'\u7535\u5b50', u'\u5174\u594b'], u'collected': u'9248', u'id': u'133484817'}, 126494633: {u'play': u'1302160', u'description': u'\u4ecb\u7ecd\uff1a \u591c\u662f\u7f20\u7ef5\u7684\u60c5\u6b32\uff0c\u4e0d\u77e5\u4ece\u4f55\u4e0b\u624b\uff1f\u6253\u5f00\u8fd9\u4e2a\u6b4c\u5355\uff0c\u4e00\u5207\u5c3d\u5728\u7f8e\u5999\u7684\u8ba1\u5212\u4e2d\u3002 future bass /chill trap / lofi/vaporwave /jazz /hiphop/lounge ', u'num_comments': 912, u'share': u'974', u'songs_num': 69, u'tag': [u'\u6b27\u7f8e', u'\u7535\u5b50', u'\u6027\u611f'], u'collected': u'43981', u'id': u'126494633'}, 320222878: {u'play': u'1495228', u'description': u"\u4ecb\u7ecd\uff1a \u25aaThug Life\u89c6\u9891\u91cc\u81f3\u4eca\u51fa\u73b0\u8fc7\u7684\u6240\u6709\u6b4c\u66f2\u5168\u6536\u5f55\uff01\u8d70\u5728\u8857\u4e0a\u542c\u7740\u8fd9\u4e9b\u6b4c\u611f\u89c9\u5c4c\u7206\u4e86\u6709\u6ca1\u6709\uff01\uff01\u5efa\u8bae\u968f\u673a\u64ad\u653e\u3002 \u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014 I DIDN'T CHOOSE THE THUG LIFE IT CHOOSE ME!! ", u'num_comments': 345, u'share': u'828', u'songs_num': 82, u'tag': [u'\u6b27\u7f8e', u'\u8bf4\u5531', u'\u6000\u65e7'], u'collected': u'55903', u'id': u'320222878'}, 329514245: {u'play': u'239608', u'description': u'\u4ecb\u7ecd\uff1a \u7cbe\u9009\u7684Trap Rap\u6b4c\u5355 \u6301\u7eed\u66f4\u65b0 ', u'num_comments': 61, u'share': u'96', u'songs_num': 183, u'tag': [u'\u7535\u5b50', u'\u8bf4\u5531', u'\u5174\u594b'], u'collected': u'8432', u'id': u'329514245'}}, u'total_songs': u'2010', u'follows': u'41', u'activities': u'0', u'age': u'95\u540e', u'playlist_create': {}}

# 性别绘图
def sta_gender():
    gender_list = []
    with open(type_file,'rb') as f:
        type_info = pickle.load(f)

    for type in type_info.keys():
        print type
        temp_list = []
        for item in type_info[type]:
            if 'gender' in item.keys():
                temp_list.append(int(item['gender']))
        gender_list.append(temp_list)

    male_list = []
    female_list = []
    for type_item in gender_list:
        male_list.append(type_item.count(1))
        female_list.append(type_item.count(2))

    for i in range(len(male_list)):
        sum = male_list[i] + female_list[i]
        male_list[i] = float(male_list[i]) / sum
        female_list[i] = float(female_list[i]) / sum

    male_list_ = []
    female_list_ = []
    for i in range(len(male_list)):
        male_list_.append(male_list[type_index[i]-1])
        female_list_.append(female_list[type_index[i]-1])

    print male_list_,female_list_

    # 绘图
    f, ax1 = plt.subplots(1, 1, figsize=(10, 5))

    bar_width = 0.5

    # positions of the left bar-boundaries
    bar_l = [i + 1 for i in range(14)]
    bar_l = np.array(bar_l)

    # positions of the x-axis ticks (center of the bars as bar labels)
    tick_pos = [i + (bar_width / 2) for i in bar_l]

    ax1.bar(bar_l + bar_width / 2, male_list_, width=bar_width,
            label='male', alpha=0.5, color='b')
    ax1.bar(bar_l + bar_width / 2, female_list_, width=bar_width,
            bottom=male_list_, label='female', alpha=0.5, color='r')
    plt.axis([-6, 6, 0, 1])

    plt.sca(ax1)
    plt.xticks(tick_pos, type_name)

    ax1.set_ylabel("Percent")
    ax1.set_xlabel("Profile Image")
    plt.legend(loc='upper left')
    plt.xlim([min(tick_pos) - bar_width, max(tick_pos) + bar_width])
    plt.grid()
    # plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

    plt.show()

# sta_gender()

# 开始统计信息 绘制图片
all_sta_data = '../data/all_sta_data.txt'
def sta_and_write2file():
    with open(type_file,'rb') as f:
        type_info = pickle.load(f)

    # 逐个处理每个类别的信息
    playlist_create_no_list = []
    playlist_collect_no_list = []
    level_list = []
    fans_list = []
    follows_list = []
    total_songs_list = []
    activities_list = []
    age_list = []

    playlist_create_play_list = []
    playlist_create_num_comments_list = []
    playlist_create_share_list = []
    playlist_create_songs_num_list = []
    playlist_create_tag_list = []

    playlist_collect_play_list = []
    playlist_collect_num_comments_list = []
    playlist_collect_share_list = []
    playlist_collect_songs_num_list = []
    playlist_collect_tag_list = []


    types = type_info.keys()
    for type in types:
        playlist_create_no_list_ = []
        playlist_collect_no_list_ = []
        level_list_ = []
        fans_list_ = []
        follows_list_ = []
        total_songs_list_ = []
        activities_list_ = []
        age_list_ = []

        playlist_create_play_list_ = []
        playlist_create_num_comments_list_ = []
        playlist_create_share_list_ = []
        playlist_create_songs_num_list_ = []
        playlist_create_tag_list_ = []

        playlist_collect_play_list_ = []
        playlist_collect_num_comments_list_ = []
        playlist_collect_share_list_ = []
        playlist_collect_songs_num_list_ = []
        playlist_collect_tag_list_ = []

        for item in type_info[type]:
            keys = item.keys()
            if 'playlist_create_no' in keys:
                playlist_create_no_list_.append(int(item['playlist_create_no']))
            if 'playlist_collect_no' in keys:
                playlist_collect_no_list_.append(int(item['playlist_collect_no']))
            if 'level' in keys:
                level_list_.append(int(item['level']))
            if 'fans' in keys:
                fans_list_.append(int(item['fans']))
            if 'follows' in keys:
                follows_list_.append(int(item['follows']))
            if 'total_songs' in keys:
                total_songs_list_.append(int(item['total_songs']))
            if 'activities' in keys:
                activities_list_.append(int(item['activities']))
            if 'age' in keys:
                if item['age'] == '':
                    age_list_.append(-1)
                else:
                    print item['age']
                    age = 15.5 - int(item['age'][:2])
                    age = age if age > 0 else age + 100
                    print age
                    age_list_.append(age)

            if 'playlist_collect' in keys:
                playlist_collect = item['playlist_collect']
                for playlist in playlist_collect.values():
                    playlist_keys = playlist.keys()
                    if 'play' in playlist_keys:
                        playlist_collect_play_list_.append(playlist['play'])
                    if 'num_comments' in playlist_keys:
                        playlist_collect_num_comments_list_.append(playlist['num_comments'])
                    if 'share' in playlist_keys:
                        playlist_collect_share_list_.append(playlist['share'])
                    if 'songs_num' in playlist_keys:
                        playlist_collect_songs_num_list_.append(playlist['songs_num'])
                    if 'tag' in playlist_keys:
                        playlist_collect_tag_list_.append(playlist['tag'])

            if 'playlist_create' in keys:
                playlist_create = item['playlist_create']
                for playlist in playlist_create.values():
                    playlist_keys = playlist.keys()
                    if 'play' in playlist_keys:
                        playlist_create_play_list_.append(playlist['play'])
                    if 'num_comments' in playlist_keys:
                        playlist_create_num_comments_list_.append(playlist['num_comments'])
                    if 'share' in playlist_keys:
                        playlist_create_share_list_.append(playlist['share'])
                    if 'songs_num' in playlist_keys:
                        playlist_create_songs_num_list_.append(playlist['songs_num'])
                    if 'tag' in playlist_keys:
                        playlist_create_tag_list_.append(playlist['tag'])

        playlist_collect_no_list.append(playlist_collect_no_list_)
        playlist_create_no_list.append(playlist_create_no_list_)
        level_list.append(level_list_)
        fans_list.append(fans_list_)
        follows_list.append(follows_list_)
        total_songs_list.append(total_songs_list_)
        activities_list.append(activities_list_)
        age_list.append(age_list_)

        playlist_create_play_list.append(playlist_create_play_list_)
        playlist_create_num_comments_list.append(playlist_create_num_comments_list_)
        playlist_create_share_list.append(playlist_create_share_list_)
        playlist_create_songs_num_list.append(playlist_create_songs_num_list_)
        playlist_create_tag_list.append(playlist_create_tag_list_)

        playlist_collect_play_list.append(playlist_collect_play_list_)
        playlist_collect_num_comments_list.append(playlist_collect_num_comments_list_)
        playlist_collect_share_list.append(playlist_collect_share_list_)
        playlist_collect_songs_num_list.append(playlist_collect_songs_num_list_)
        playlist_collect_tag_list.append(playlist_collect_tag_list_)

    # print playlist_collect_no_list

    with open(all_sta_data,'wb') as f:
        f.write('all type lists:\n')
        f.write(str(types) + '\n')
        f.write('playlist_collect_no_list:\n')
        f.write(str(playlist_collect_no_list) + '\n')
        f.write('playlist_create_no_list:\n')
        f.write(str(playlist_create_no_list) + '\n')
        f.write('level_list:\n')
        f.write(str(level_list) + '\n')
        f.write('fans_list:\n')
        f.write(str(fans_list) + '\n')
        f.write('follows_list:\n')
        f.write(str(follows_list) + '\n')
        f.write('total_songs_list:\n')
        f.write(str(total_songs_list) + '\n')
        f.write('activities_list:\n')
        f.write(str(activities_list) + '\n')
        f.write('age_list:\n')
        f.write(str(age_list) + '\n')
        


        f.write('playlist_create_play_list:\n')
        f.write(str(playlist_create_play_list) + '\n')
        f.write('playlist_create_num_comments_list:\n')
        f.write(str(playlist_create_num_comments_list) + '\n')
        f.write('playlist_create_share_list:\n')
        f.write(str(playlist_create_share_list) + '\n')
        f.write('playlist_create_songs_num_list:\n')
        f.write(str(playlist_create_songs_num_list) + '\n')
        f.write('playlist_create_tag_list:\n')
        f.write(str(playlist_create_tag_list) + '\n')

        f.write('playlist_collect_play_list:\n')
        f.write(str(playlist_collect_play_list) + '\n')
        f.write('playlist_collect_num_comments_list:\n')
        f.write(str(playlist_collect_num_comments_list) + '\n')
        f.write('playlist_collect_share_list:\n')
        f.write(str(playlist_collect_share_list) + '\n')
        f.write('playlist_collect_songs_num_list:\n')
        f.write(str(playlist_collect_songs_num_list) + '\n')
        f.write('playlist_collect_tag_list:\n')
        f.write(str(playlist_collect_tag_list) + '\n')
        
#sta_and_write2file()

def cal_mean(line_index = 1):
    with open(all_sta_data,'rb') as f:
        for lineno,line in enumerate(f,1):
            if lineno < line_index:
                continue
            if lineno > line_index + 1:
                break
            if lineno == line_index:
                index_name = line
            if lineno == line_index + 1:
                index_data = line

    data = index_data
    data = eval(data)
    for item in data:
        while -1 in item:
            item.remove(-1)
    result = []
    for record in data:
        result.append(np.array(record,dtype=float).mean())
    print result
    print len(result)
    with open('../data/mean.txt','a') as f:
        f.write(index_name)
        f.write(str(result) + '\n')

#cal_mean(line_index = 17)

# 查看topk的tag
def get_topk_tag():
    tag1_line = 28
    tag2_line = 38
    tags = []
    with open(all_sta_data,'rb') as f:
        for lineno,line in enumerate(f,1):
            if lineno == tag1_line or lineno == tag2_line:
                tags.extend(eval(line))
            else:
                continue

    print len(tags)
    tags_ = []
    for a in tags:
        for b in a:
            for item in b:
                tags_.append(item)
    # print tags_
    tags_count = Counter(tags_)
    print len(tags_)
    print len(tags_count)
    # 577491
    # 74
    topk = tags_count.most_common(20)
    for item in topk:
        print item[0],item[1]

# get_topk_tag()

# print len(type_name)
# 绘图
def plot_FF():
    fans_line = 10
    follows_line = 12
    with open(all_sta_data,'rb') as f:
        for lineno,line in enumerate(f,1):
            if lineno == fans_line:
                fans_list = eval(line)
            if lineno == follows_line:
                follows_list = eval(line)
            else:
                continue
    ff_list = []
    for a in range(len(fans_list)):
        temp_list = []
        for b in range(len(fans_list[a])):
            try:
                ff = float(fans_list[a][b]) / follows_list[a][b]
                temp_list.append(ff)
            except Exception as e:
                print e
        ff_list.append(temp_list)



    ff_list_new = []
    for index in type_index:
        ff_list_new.append(ff_list[index-1])

    # 计算中位数
    def get_median(data):
        data.sort()
        half = len(data) // 2
        return (data[half] + data[~half]) / 2

    median_list = []
    for ff in ff_list_new:
        median_list.append(get_median(ff))

    print median_list

    fig = plt.figure(figsize=(8, 6))
    plt.axis([-6, 6, -0.5, 20])

    plt.boxplot(ff_list_new,
                # notch=False,  # box instead of notch shape
                # sym='rs',    # red squares for outliers
                showmeans=True,
                vert=True)  # vertical box aligmnent

    plt.xticks([y + 1 for y in range(len(ff_list_new))], type_name)
    plt.xlabel('Profile Image')
    plt.ylabel('FF')
    plt.title('FF Boxplot')
    plt.savefig('../pic/FF.png')
    plt.show()

# plot_FF()

def plot_activities():
    activities_line = 16
    with open(all_sta_data,'rb') as f:
        for lineno,line in enumerate(f,1):
            if lineno == activities_line:
                activities_list = eval(line)
            else:
                continue

    activities_list_new = []
    for index in type_index:
        activities_list_new.append(activities_list[index-1])

    fig = plt.figure(figsize=(8, 6))
    plt.axis([-6, 6, -2, 50])

    plt.boxplot(activities_list_new,
                # notch=False,  # box instead of notch shape
                # sym='rs',    # red squares for outliers
                showmeans=True,
                vert=True)  # vertical box aligmnent

    plt.xticks([y + 1 for y in range(len(activities_list_new))],type_name)
    plt.xlabel('Profile Image')
    plt.ylabel('Tweets')
    plt.title('Tweets Boxplot')
    plt.savefig('../pic/activity.png')
    plt.show()

# plot_activities()

def plot_playlist_re():
    collect_line = 4
    create_line = 6
    with open(all_sta_data, 'rb') as f:
        for lineno, line in enumerate(f, 1):
            if lineno == collect_line:
                collect_list = eval(line)
            if lineno == create_line:
                create_list = eval(line)
            else:
                continue

    cc_list = []
    for a in range(len(collect_list)):
        temp_list = []
        for b in range(len(collect_list[a])):
            try:
                ff = float(collect_list[a][b]) / create_list[a][b]
                temp_list.append(ff)
            except Exception as e:
                print e
        cc_list.append(temp_list)

    cc_list_new = []
    for index in type_index:
        cc_list_new.append(cc_list[index - 1])

    # 计算中位数
    def get_median(data):
        data.sort()
        half = len(data) // 2
        return (data[half] + data[~half]) / 2

    median_list = []
    for ff in cc_list_new:
        median_list.append(get_median(ff))

    print median_list

    fig = plt.figure(figsize=(8, 6))
    plt.axis([-6, 6, -0.5, 10])

    plt.boxplot(cc_list_new,
                # notch=False,  # box instead of notch shape
                # sym='rs',    # red squares for outliers
                showmeans=True,
                vert=True)  # vertical box aligmnent

    plt.xticks([y + 1 for y in range(len(cc_list_new))], type_name)
    plt.xlabel('Profile Image')
    plt.ylabel('CC')
    plt.title('CC Boxplot')
    plt.savefig('../pic/CC.png')
    plt.show()

# plot_playlist_re()

def plot_playlist():
    collect_line = 4
    create_line = 6
    with open(all_sta_data, 'rb') as f:
        for lineno, line in enumerate(f, 1):
            if lineno == collect_line:
                collect_list = eval(line)
            if lineno == create_line:
                create_list = eval(line)
            else:
                continue

    cc_list = []
    for a in range(len(collect_list)):
        temp_list = []
        for b in range(len(collect_list[a])):
            try:
                ff = create_list[a][b] + collect_list[a][b]
                # print collect_list[a][b],create_list[a][b]
                temp_list.append(ff)
            except Exception as e:
                print e
        cc_list.append(temp_list)

    cc_list_new = []
    for index in type_index:
        cc_list_new.append(cc_list[index - 1])

    # print cc_list_new[9]
    # for i in cc_list_new[9]:
    #     if i <= 5:
    #         cc_list_new[9].remove(i)
    # print cc_list_new[9]

    # 计算中位数
    def get_median(data):
        data.sort()
        half = len(data) // 2
        return (data[half] + data[~half]) / 2

    median_list = []
    for ff in cc_list_new:
        median_list.append(get_median(ff))

    print median_list

    fig = plt.figure(figsize=(8, 6))
    plt.axis([-6, 6, -0.5,120])

    plt.boxplot(cc_list_new,
                # notch=False,  # box instead of notch shape
                # sym='rs',    # red squares for outliers
                showmeans=True,
                vert=True)  # vertical box aligmnent

    plt.xticks([y + 1 for y in range(len(cc_list_new))], type_name)
    plt.xlabel('Profile Image')
    plt.ylabel('Playlist_Num')
    plt.title('Playlist_Num Boxplot')
    plt.savefig('../pic/total_p.png')
    plt.show()

# plot_playlist()
top20_tags = ['欧美','流行','电子','华语','日语','轻音乐','ACG','影视原声','经典','兴奋','另类/独立','夜晚','摇滚','治愈','放松','古典','民谣','游戏','怀旧','说唱']
# print len(top20_tags)

def process_tags():
    collect_line = 38
    create_line = 28
    with open(all_sta_data, 'rb') as f:
        for lineno, line in enumerate(f, 1):
            if lineno == collect_line:
                collect_list = eval(line)
            if lineno == create_line:
                create_list = eval(line)
            else:
                continue

    print '数据加载完毕！'

    tag_list = []
    for a in collect_list:
        temp_list = []
        for b in a:
            for c in b:
                temp_list.append(c)
        tag_list.append(temp_list)

    print '-'*20

    for index,a in enumerate(create_list):
        temp_list = tag_list[index]
        for b in a:
            for c in b:
                temp_list.append(c)
        tag_list.append(temp_list)

    print '-' * 20

    tag_list_new = []
    for index in type_index:
        tag_list_new.append(tag_list[index - 1])

    ratio_list = []
    for i in range(20):
        ratio_list.append([])

    for index,item in enumerate(tag_list_new):
        item_sum = len(item)
        most_topk = Counter(item).most_common(70)
        # print index
        for a in most_topk:
            # print a[0],a[1]/float(item_sum)
            temp = a[0].encode('utf-8')
            if temp in top20_tags:
                print a[0]
                ratio_list[top20_tags.index(temp)].append(a[1]/float(item_sum))

    print ratio_list
    print len(ratio_list)

    # 绘图
    x = list(range(1,15))
    # 仅仅取差别比较大的几个tag
    ratio_temp = copy.deepcopy(ratio_list)
    ratio_list = []
    filter_index = [0,1,2,3,4,5,6,13]
    for filter in filter_index:
        ratio_list.append(ratio_temp[filter])

    #plt.plot(x, ratio_list[0], marker='x')
    for item in ratio_list:
        plt.plot(x,item)
    '''
    plt.xlim([0, len(x) + 1])
    plt.ylim([0, max(y_1 + y_2) + 10])
    '''
    plt.xticks(x,type_name)
    plt.xlabel('Profile Image')
    plt.ylabel("Tags' Ratio")
    # 设置中文字体
    myfont = fm.FontProperties(fname='/System/Library/Fonts/PingFang.ttc')
    plt.title(u'歌单标签比例',fontproperties=myfont)

    top20_tags_ = [item.decode('utf-8') for item in top20_tags]
    filter_tags = []
    for filter in filter_index:
        filter_tags.append(top20_tags_[filter])
    plt.legend(filter_tags, loc='upper left',prop=myfont)


    plt.show()

# process_tags()


