#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2021/11/17 15:01
# @Author  : John
# @File    : test.py
# @Remake  :
import re

a = '变量$:3; *:2'
params_num_pattern = re.search('\$:(\d)', a)
params_num = params_num_pattern.group(1)
print(params_num)