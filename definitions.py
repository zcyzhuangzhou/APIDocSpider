#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: Chengyuan Zhao
@Email: 19110240027@fudan.edu.cn
@Created: 2020/12/10
------------------------------------------
@Modify: 2020/12/10
------------------------------------------
@Description:
"""
import os

from sekg.graph.factory import GraphInstanceFactory
from sekg.mysql.factory import MysqlSessionFactory

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root

MYSQL_CONFIG_PATH = os.path.join(ROOT_DIR, 'mysql_config.json')
MYSQL_FACTORY = MysqlSessionFactory(MYSQL_CONFIG_PATH)
# the data dir
DATA_DIR = os.path.join(ROOT_DIR, './APIDocSpider/data')
# the output dir
OUTPUT_DIR = os.path.join(ROOT_DIR, './APIDocSpider/output')