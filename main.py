#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: Chengyuan Zhao
@Email: 19110240027@fudan.edu.cn
@Created: 2020/11/17
------------------------------------------
@Modify: 2020/11/17
------------------------------------------
@Description: 
"""
from scrapy.cmdline import execute
import os
import sys
if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    execute(['scrapy', 'crawl', 'crawlReferenceDocHtml'])
