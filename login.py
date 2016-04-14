# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

__author__ = 'InG_byr'
from urllib import request, parse
from configparser import ConfigParser
from bs4 import BeautifulSoup
import sys


# TODO第一次登陆情况未处理，账户密码为空时
class BUPTLogin():
    def __init__(self):
        self.url = 'http://10.3.8.211'
        self.load_config()

    # load the config file
    def load_config(self):
        self.cfg = ConfigParser()
        print(os.getcwd())
        self.cfg.read(os.getcwd()+'/BUPTLogin/'+'app.ini')
        self.saveUser = self.cfg.getboolean('tool', 'saveUser')
        if self.saveUser:
            self.set_user(self.cfg.get('user', 'account'),
                          self.cfg.get('user', 'password'))
        else:
            self.login_failed()

    # set the account and password
    def set_user(self, account, password):
        self.account = account
        self.password = password

    # get the options
    def get_input_user(self, sysargv):
        if len(sysargv) == 3:
            self.set_user(sysargv[1], sysargv[2])
            print('>>>strat login account: {}'.format(sysargv[1]))
        elif len(sysargv) == 2:
            raise SystemExit('[error]need more options, forget to input the password?')
        elif len(sysargv) > 3:
            raise SystemExit('[error]too much options!')

    # login to BUPT network
    def start_login(self):
        postData = parse.urlencode([
            ('DDDDD', self.account),
            ('upass', self.password),
            ('savePWD', 0),
            ('0MKKey', '')
        ])
        # send request
        req = request.Request(self.url)
        req.add_header('User-Agent',
                       'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
        with request.urlopen(req, data=postData.encode('utf-8')) as f:
            self.show_result(f.read())

    # parse the response html
    def show_result(self, htmlDoc):
        soup = BeautifulSoup(htmlDoc, 'lxml')
        if soup.title.string == u'信息返回窗':
            print('>>>Login failed, please input account and password again!')
            self.login_failed()
            self.start_login()
        if soup.title.string == u'登录成功窗':
            # when login successfully, save the user
            print('>>>Login successfully')
            self.save_user(self.account, self.password)
            self.show_use_data()

    #when login failed
    def login_failed(self):
        account = input('>>>Account: ')
        password = input('>>>Password: ')
        self.set_user(account, password)

    # reopen the website to get information
    def show_use_data(self):
        req = request.Request(self.url)
        with request.urlopen(req) as f:
            htmlDoc = f.read()
        statPage = BeautifulSoup(htmlDoc, 'lxml')
        stat = statPage.head.script.string.encode('gb18030')
        fee = int(stat[55:65])
        flow = int(stat[30:40])
        flow0 = flow % 1024
        flow1 = flow - flow0
        flow0 = flow0 * 1000
        flow0 = flow0 - flow0 % 1024
        fee1 = fee - fee % 100
        flow3 = '.'
        print('>>>Used internet traffic : {0}{1}{2} MByte'.format(int(flow1 / 1024), flow3, int(flow0 / 1024)))
        print('>>>Balance : {} RMB'.format(fee1 / 10000))

    # when login successfully save the user auto
    def save_user(self, account, password):
        self.cfg.set('user', 'account', account)
        self.cfg.set('user', 'password', password)
        self.cfg.set('tool', 'saveUser', 'True')
        self.cfg.write(open(os.getcwd()+'/BUPTLogin/'+'app.ini', 'r+'))


if __name__ == '__main__':
    mLogin = BUPTLogin()
    mLogin.get_input_user(sys)
    mLogin.start_login()
