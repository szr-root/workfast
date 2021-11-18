#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2021/11/17 15:01
# @Author  : John
# @File    : test.py
# @Remake  :
import re

params_num_pattern = re.search('\$:(\d)', 'xxx')
if params_num_pattern is None:
    params_num = params_num_pattern.group(1)