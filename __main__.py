# !/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'InG_byr'

from login import BUPTLogin
import sys

mLogin = BUPTLogin()
mLogin.get_input_user(sys.argv)
mLogin.start_login()
