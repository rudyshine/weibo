# -*-coding:utf8-*-
import time
import selenium
import codecs
from selenium import webdriver
import re
import pandas as pd
import csv

def login(username_,password_,url):
    print("login begin...")
    browser.get(url)
    time.sleep(25)
    print('finsh time.sleep1')

    # #右上登陆
    # login_btn = browser.find_element_by_xpath('//a[@node-type="loginBtn"]')
    # login_btn.click()
    # time.sleep(10)
    # print('finsh time.sleep2')
    #
    # ### 选择账号登录
    # time.sleep(2)
    # name_login = browser.find_element_by_xpath('//a[@action-data="tabname=login"]')
    # name_login.click()

    #### 输入用户名,密码
    username = browser.find_element_by_xpath('//input[@node-type="username"]')
    password = browser.find_element_by_xpath('//input[@node-type="password"]')
    username.clear()
    username.send_keys(username_)
    # time.sleep(2)
    password.clear()
    password.send_keys(password_)
    # time.sleep(2)

    ###提交登陆
    sub_btn = browser.find_element_by_xpath('//a[@suda-data="key=tblog_weibologin3&value=click_sign"]')
    sub_btn.click()
    time.sleep(10)
    # while True:
    #     try:
    #         #     verify_img = browser.find_element_by_xpath('//img[@node-type="verifycode_image"]')
    #         verify_img = browser.find_element_by_xpath('//a[@node-type="submitBtn"]')
    #         # except exceptions.NoSuchElementException:
    #         #     break
    #         if verify_img:
    #             # 输入验证码
    #             verify_code = browser.find_element_by_xpath('//input[@node-type="verifycode"]')
    #             verify_code_ = input('verify_code > ')
    #             verify_code.clear()
    #             verify_code.send_keys(verify_code_)
    #
    #             # 提交登陆
    #             sub_btn = browser.find_element_by_xpath('//a[@suda-data="key=tblog_weibologin3&value=click_sign"]')
    #             sub_btn.click()
    #             time.sleep(2)
    #             print("long in ")
    #             break
    #     except:
    #         pass
    print("login finish")

def get_infor(url):

    browser.get(url)
    time.sleep(5)
    print("start collect info...")
    ##昵称
    str_name = browser.find_element_by_xpath('//*[@id="Pl_Official_Headerv6__1"]/div/div/div[2]/div[2]/h1')
    str_t = str_name.text.split(" ")
    num_name = str_t[0]  # 空格分隔 获取第一个值 "Eastmount 详细资料 设置 新手区"
    ##微博数
    str_wb = browser.find_element_by_xpath('//*[@id="Pl_Core_T8CustomTriColumn__3"]/div/div/div/table/tbody/tr/td[3]/a/strong')
    pattern = r"\d+\.?\d*"  # 正则提取"微博[0]" 但r"(.∗?)"总含[]
    guid = re.findall(pattern, str_wb.text, re.S | re.M)
    for value in guid:
        num_wb =int(value)
        break
    # 关注数
    str_gz = browser.find_element_by_xpath('//*[@id="Pl_Core_T8CustomTriColumn__3"]/div/div/div/table/tbody/tr/td[1]/a/strong')
    guid = re.findall(pattern, str_gz.text, re.M)
    num_gz = int(guid[0])
    # 粉丝数
    str_fs = browser.find_element_by_xpath('//*[@id="Pl_Core_T8CustomTriColumn__3"]/div/div/div/table/tbody/tr/td[2]/a/strong')
    guid = re.findall(pattern, str_fs.text, re.M)
    num_fs = int(guid[0])

    # print("start save info...")
    # with open('test.csv','w+') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(["昵称","微博数","关注数","粉丝数"])
    #     data = [num_name,num_wb,num_gz,num_fs]
    #     writer.writerow(data)
    # print("save info done!")

    print("start save info...")
    writer = csv.writer(open('weibo_info.csv','a',))
    # writer.writerow(["昵称","微博数","关注数","粉丝数"])
    data = [num_name,num_wb,num_gz,num_fs]
    writer.writerow(data)
    print("save info done!")

def get_comcent():
    print("get_comcent start ja")
    ##在爬取内容之前应该先将滑动条拖到最下方
    js = "var q=document.documentElement.scrollTop=30000"
    for i in range(3):
        browser.execute_script(js)
        print('js:',i)
        time.sleep(10)

    data_text = [] # 保存微博内容
    data_time = [] # 保存发布微博的时间
    data_relay = [] # 转发量
    data_comment = [] # 评论量
    data_support = [] # 支持量

    for i in range(2, 46):
        try:
            lazyload = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__22"]/div/div[%d]/div[1]/div[1]/div[1]/p/a[@href="javascript:void(0)"]' % i)
            lazyload.refresh()
            print('test pass: refresh successful')
        except:
            pass

        try:
            text = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__22"]/div/div[%d]/div[1]/div[4]/div[3]'% i).text
        except selenium.common.exceptions.NoSuchElementException:
            try:
                text = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__22"]/div/div[%d]/div[1]/div[3]/div[3]' % i).text
            except selenium.common.exceptions.NoSuchElementException:
                    try:
                        text = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__22"]/div/div[%d]/div[2]/div[3]/div[3]' % i).text ##广告
                    except selenium.common.exceptions.NoSuchElementException:
                        try:
                            text=browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__22"]/div/div[%d]/div[2]/div[4]/div[3]' % i).text##广告
                        except selenium.common.exceptions.NoSuchElementException:
                            try:
                                text = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__23"]/div/div[%d]/div[1]/div[3]/div[3]' % i).text
                            except selenium.common.exceptions.NoSuchElementException:
                                try:
                                    text = browser.find_element_by_xpath( '//*[@id="Pl_Official_MyProfileFeed__23"]/div/div[%d]/div[2]/div[3]/div[3]' % i).text
                                except selenium.common.exceptions.NoSuchElementException:
                                    try:
                                        text = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__23"]/div/div[%d]/div[1]/div[4]/div[3]' % i).text
                                    except selenium.common.exceptions.NoSuchElementException:
                                        try:
                                            text = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__23"]/div/div[%d]/div[2]/div[4]/div[3]' % i).text
                                        except selenium.common.exceptions.NoSuchElementException: ##超出range(2, 46)
                                            try:
                                                text = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__24"]/div/div[%d]/div[1]/div[3]/div[3]' % i).text
                                            except selenium.common.exceptions.NoSuchElementException:
                                                try:
                                                    text = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__24"]/div/div[%d]/div[2]/div[3]/div[3]' % i).text
                                                except selenium.common.exceptions.NoSuchElementException:
                                                    try:
                                                        text = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__24"]/div/div[%d]/div[1]/div[4]/div[3]' % i).text
                                                    except selenium.common.exceptions.NoSuchElementException:
                                                        try:
                                                            text = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__24"]/div/div[%d]/div[2]/div[4]/div[3]' % i).text
                                                        except selenium.common.exceptions.NoSuchElementException:
                                                            pass

        try:
            Time = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__22"]/div/div[%d]/div[1]/div[4]/div[2]/a[1]'% i).text
        except selenium.common.exceptions.NoSuchElementException:
            try:
                Time = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__22"]/div/div[%d]/div[1]/div[3]/div[2]/a[1]' % i).text
            except selenium.common.exceptions.NoSuchElementException:
                try:
                    Time = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__22"]/div/div[%d]/div[2]/div[3]/div[2]/a[1]' % i).text ##广告
                except selenium.common.exceptions.NoSuchElementException:
                    try:
                        Time = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__22"]/div/div[%d]/div[2]/div[4]/div[2]/a[1]' % i).text ##广告
                    except selenium.common.exceptions.NoSuchElementException:
                        try:
                            Time = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__23"]/div/div[%d]/div[1]/div[3]/div[2]/a[1]' % i).text
                        except selenium.common.exceptions.NoSuchElementException:
                            try:
                                Time = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__23"]/div/div[%d]/div[2]/div[3]/div[2]/a[1]' % i).text
                            except selenium.common.exceptions.NoSuchElementException: ##超出range(2, 46)
                                try:
                                    Time = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__23"]/div/div[%d]/div[1]/div[4]/div[2]/a[1]' % i).text
                                except selenium.common.exceptions.NoSuchElementException:
                                    try:
                                        Time = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__23"]/div/div[%d]/div[2]/div[4]/div[2]/a[1]' % i).text
                                    except selenium.common.exceptions.NoSuchElementException:
                                        try:
                                            Time = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__24"]/div/div[%d]/div[1]/div[3]/div[2]/a[1]' % i).text
                                        except selenium.common.exceptions.NoSuchElementException:
                                            try:
                                                Time = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__24"]/div/div[%d]/div[2]/div[3]/div[2]/a[1]' % i).text
                                            except selenium.common.exceptions.NoSuchElementException:
                                                try:
                                                    Time = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__24"]/div/div[%d]/div[1]/div[4]/div[2]/a[1]' % i).text
                                                except selenium.common.exceptions.NoSuchElementException:
                                                    try:
                                                        Time = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__24"]/div/div[%d]/div[2]/div[4]/div[2]/a[1]' % i).text
                                                    except selenium.common.exceptions.NoSuchElementException:
                                                        pass

        try:
            relay = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__22"]/div/div[%d]/div[2]/div/ul/li[2]/a/span/span/span/em[2]'% i).text
        except selenium.common.exceptions.NoSuchElementException:
            try:
                relay = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__22"]/div/div[%d]/div[3]/div/ul/li[2]/a/span/span/span/em[2]' % i).text ##广告
            except selenium.common.exceptions.NoSuchElementException: ##超出range(2, 46)
                try:
                    relay = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__23"]/div/div[%d]/div[2]/div/ul/li[2]/a/span/span/span/em[2]' % i).text
                except selenium.common.exceptions.NoSuchElementException:
                    try:
                        relay = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__23"]/div/div[%d]/div[3]/div/ul/li[2]/a/span/span/span/em[2]' % i).text
                    except selenium.common.exceptions.NoSuchElementException:
                        try:
                            relay = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__24"]/div/div[%d]/div[2]/div/ul/li[2]/a/span/span/span/em[2]' % i).text
                        except selenium.common.exceptions.NoSuchElementException:
                            try:
                                relay = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__24"]/div/div[%d]/div[3]/div/ul/li[2]/a/span/span/span/em[2]' % i).text
                            except selenium.common.exceptions.NoSuchElementException:
                                pass

        try:
            comment = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__22"]/div/div[%d]/div[2]/div/ul/li[3]/a/span/span/span/em[2]'% i).text
        except selenium.common.exceptions.NoSuchElementException:
            try:
                comment= browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__22"]/div/div[%d]/div[3]/div/ul/li[3]/a/span/span/span/em[2]'% i).text ##广告
            except selenium.common.exceptions.NoSuchElementException: ##超出range(2, 46)
                try:
                    comment = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__23"]/div/div[%d]/div[2]/div/ul/li[3]/a/span/span/span/em[2]' % i).text
                except selenium.common.exceptions.NoSuchElementException:
                    try:
                        comment = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__23"]/div/div[%d]/div[3]/div/ul/li[3]/a/span/span/span/em[2]' % i).text
                    except selenium.common.exceptions.NoSuchElementException:
                        try:
                            comment = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__24"]/div/div[%d]/div[2]/div/ul/li[3]/a/span/span/span/em[2]' % i).text
                        except selenium.common.exceptions.NoSuchElementException:
                            try:
                                comment = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__24"]/div/div[%d]/div[3]/div/ul/li[3]/a/span/span/span/em[2]' % i).text
                            except selenium.common.exceptions.NoSuchElementException:
                                pass
        try:
            support = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__22"]/div/div[%d]/div[2]/div/ul/li[4]/a/span/span/span/em[2]'% i).text
        except selenium.common.exceptions.NoSuchElementException:
            try:
                support = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__22"]/div/div[%d]/div[3]/div/ul/li[4]/a/span/span/span/em[2]' % i).text ##广告
            except selenium.common.exceptions.NoSuchElementException: ##超出range(2, 46)
                try:
                    support = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__23"]/div/div[%d]/div[2]/div/ul/li[4]/a/span/span/span/em[2]' % i).text
                except selenium.common.exceptions.NoSuchElementException:
                    try:
                        support = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__23"]/div/div[%d]/div[3]/div/ul/li[4]/a/span/span/span/em[2]' % i).text
                    except selenium.common.exceptions.NoSuchElementException:
                        try:
                            support = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__24"]/div/div[%d]/div[2]/div/ul/li[4]/a/span/span/span/em[2]' % i).text
                        except selenium.common.exceptions.NoSuchElementException:
                            try:
                                support = browser.find_element_by_xpath('//*[@id="Pl_Official_MyProfileFeed__24"]/div/div[%d]/div[3]/div/ul/li[4]/a/span/span/span/em[2]' % i).text
                            except selenium.common.exceptions.NoSuchElementException:
                                pass

        if text:
            data_text.append(text)
            data_time.append(Time)
            data_relay.append(relay)
            data_comment.append(comment)
            data_support.append(support)
    print("存入csv....")
    weibo = pd.DataFrame({'data_text': data_text, 'data_time': data_time,'data_relay': data_relay,'data_comment': data_comment ,'data_support': data_support})
    table = weibo.set_index('data_text')
    table.head()
    weibo.to_csv('weibo_data0.csv', mode='a', header=False)
    print("done save csv....")
    #
    #收集下一页
    next_page = browser.find_elements_by_xpath('//a[@class="page next S_txt1 S_line1"]')
    for i in next_page:
        next_page[0].click()
        time.sleep(5)
        get_comcent()

if __name__ == '__main__':
    #文件操作读写信息
    inforead = codecs.open("urllist_food.txt", 'r', 'utf-8')
    username = '15089194359'  # 输入你的用户名
    password = 'zsr.1234'  # 输入你的密码
    ##Firefox
    browser = webdriver.Firefox()
    url1="http://weibo.com/"
    login(username, password, url1)
    print('Read file:')
    url = inforead.readline()
    while url!="":
        url = url.rstrip('\r\n')
        get_infor(url)
        get_comcent()
        url = inforead.readline()
