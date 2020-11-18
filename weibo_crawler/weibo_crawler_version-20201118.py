# /usr/bin/env python 3.7
# -*- coding: utf-8 -*-
# author=yiyang
# time=2020/10/18 19:16


import requests
import pprint
import time
import re
import random
import traceback
import sys

# 全局参数

starid = 5492443184  # 在这里添你想了解的明星ID（通常是10位数）。比如：王一博：5492443184，邓超：5187664653，迪丽热巴：1669879400。
header = eval(open('header.txt').read())
main_urls_shell = open('url_shell_path.txt').read()
comment_urls_shell = open('comment_urls_shell.txt').read()
weibo_contents = []  # 设空集合，微博内容待取
comment_contents = []  # 设空集合，评论内容待取


page = 1
while page < 100:
    time.sleep(random.randint(1, 3))
    main_url_content = requests.get(main_urls_shell.format(starid, starid, page), headers=header)  # 将实参传入requests，得到请求结果
    try:
        result_main = main_url_content.json()  # 对请求结果进行解析
    except Exception as e:
        print('str(Exception):\t', str(Exception))
        print('str(e):\t\t', str(e))
        print('repr(e):\t', repr(e))
        print ('repr(e):\t', repr(e))
        exc_type, exc_value, exc_traceback = sys.exc_info() 
        print('e.message:\t', exc_value)
        print("Note, object e and exc of Class %s is %s the same." % 
              (type(exc_value), ('not', '')[exc_value is e]))
        print('traceback.print_exc(): ', traceback.print_exc())
        print('traceback.format_exc():\n%s' % traceback.format_exc())
        print('########################################################')
        continue
    cards = result_main['data']['cards']  # 获取解析结果中的cards簇
    # print(cards)
    n1 = 1
    for card in cards:  # 遍历cards簇
        mblog = card.get('mblog')  # 取出mblog簇，ps.用.get取出避免空值报错
        if mblog:  # 用if True防止空值报错
            created_at = mblog['created_at']  # 发布微博的时间
            attitudes_count = str(mblog['attitudes_count'])  # 点赞次数
            comments_count = str(mblog['comments_count'])  # 评论数量
            reposts_count = str(mblog['reposts_count'])  # 转发数量
            raw_text = mblog['raw_text']  # 微博内容
            mid = mblog['mid']  # 一个重要的参数，相当于是微博主页内容的动态id，后面要用到
            weibo_content = '{}发的微博:{} 点赞数：{}，评论数：{}，转发数：{}\n网友评论如下：\n'.format(created_at, raw_text, attitudes_count,
            comments_count, reposts_count)
            # weibo_contents.append(weibo_content)
            print(weibo_content)
            with open(r'第{}条微博相关评论.txt'.format((page-1)*10+n1), "a", encoding="UTF-8") as f:
                f.write(weibo_content)
                f.write('\n')
                max_id = '0'  # max_id的初始值
                max_id_type = '0'  # max_id_type的初始值
                k1 = 1  # 计数器
                comments_page_url = comment_urls_shell.format(mid, mid, max_id, max_id_type)  # 将参数传入评论页的shell
                time.sleep(random.randint(1, 3))
                comments_url_content = requests.get(comments_page_url, headers=header)  # 返回评论页的内容
                result_comment = comments_url_content.json()  # 这个语句有时会报错，可能是.json解析的错误也可能是反爬虫战术。我们用try-except包裹，这样出错时程序也不中断
                try:
                    data_s = result_comment['data']['data']  # 评论簇
                except Exception as e:
                    continue
                max_id = result_comment['data']['max_id']  # 评论页动态生成的id
                max_id_type = result_comment['data']['max_id_type']  # 评论页id的属性代码（虽然好像没有什么卵用）
                total_number = result_comment['data']['total_number']  # 该微博评论的总数
                for data in data_s:  # 遍历评论簇
                    comment_text = re.sub('\<.*>', '', data['text'])  # 评论内容
                    comentator_name = data['user']['screen_name']  # 评论人的ID
                    comment_time = re.sub('\+.*', '', data['created_at'])  # 评论时间
                    comment_content = '(第{}/{}条)ID:{} {}评论："{}"'.format(k1, total_number, comentator_name, comment_time, comment_text)
                    comment_contents.append(comment_content)  # 用.append将评论内容取出
                    print(comment_content)
                    f.write(comment_content)
                    f.write('\n')
                    k1 += 1
                n1 += 1
                f.close()
#                n1 += 1
    page += 1
