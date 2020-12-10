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
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ApiDocHtmlModel(Base):
    __tablename__ = 'api_doc_html'

    id = Column(Integer, primary_key=True, autoincrement=True, name="Id")
    qualified_name = Column(String(255), name="QualifiedName")
    html_type = Column(Integer,  name="HtmlType")
    url = Column(String(255), name="Url")
    html = Column(Text(), name="Html")

    def __init__(self, item):
        self.qualified_name = item["qualified_name"]
        self.html_type = item["html_type"]
        self.url = item["url"]
        self.html = item["html"]

    def insert(self, session, autocommit=True):
        session.add(self)
        if autocommit:
            session.commit()
        session.close()


class ReferenceDocHtmlModel(Base):
    __tablename__ = 'reference_doc_html'

    id = Column(Integer, primary_key=True, autoincrement=True, name="Id")
    url = Column(String(255), name="Url")
    html = Column(Text(), name="Html")

    def __init__(self, item):
        self.url = item["url"]
        self.html = item["html"]

    def insert(self, session, autocommit=True):
        session.add(self)
        if autocommit:
            session.commit()
        session.close()
