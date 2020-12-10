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
import json

import scrapy

from APIDocSpider.items import ApidocspiderItem

HTML_TYPE = {
    "package_html": 1,
    "class_html": 2
}

class CrawlPackageHtml(scrapy.Spider):
    name = 'crawlPackageHtml'

    # Construct the URL to crawl class API based on the crawled package API name
    with open('./APIDocSpider/output/package.json', 'r') as f:
        url_list = json.load(f)
    offset = 0
    baseURL = 'https://docs.spring.io/spring-framework/docs/current/javadoc-api/'
    start_urls = [baseURL + url_list[offset]["qualified_name"].replace('.', '/') + '/package-summary.html']

    def parse(self, response):
        item = ApidocspiderItem()
        item["qualified_name"] = self.url_list[self.offset]["qualified_name"]
        item["url"] = response.url
        item["html"] = response.text
        item["html_type"] = HTML_TYPE["package_html"]
        yield item

        # Construct next new URL to crawl class API based on the crawled package API name
        if self.offset < len(self.url_list) - 1:
            self.offset += 1
            url = self.baseURL + self.url_list[self.offset]["qualified_name"].replace('.',
                                                                                      '/') + '/package-summary.html'
            yield scrapy.Request(url, callback=self.parse)


class CrawlClassHtml(scrapy.Spider):
    name = 'crawlClassHtml'

    # Construct the URL based on the crawled class API name to crawl field, method, enum constant and so on.
    with open('./APIDocSpider/output/class.json', 'r') as f:
        url_list = json.load(f)
    offset = 0
    baseURL = 'https://docs.spring.io/spring-framework/docs/current/javadoc-api/'
    start_urls = [baseURL
                  + url_list[offset]["qualified_name"].split(url_list[offset]["full_declaration"])[0].replace('.', '/')
                  + url_list[offset]["full_declaration"] + '.html']

    def parse(self, response):
        item = ApidocspiderItem()
        item["qualified_name"] = self.url_list[self.offset]["qualified_name"]
        item["url"] = response.url
        item["html"] = response.text
        item["html_type"] = HTML_TYPE["class_html"]
        yield item

        # Construct next new URL based on the crawled package API name to crawl API.
        if self.offset < len(self.url_list) - 1:
            self.offset += 1
            url = self.baseURL + self.url_list[self.offset]["qualified_name"].split(
                self.url_list[self.offset]["full_declaration"])[0].replace('.', '/') + \
                self.url_list[self.offset]["full_declaration"] + '.html'
            yield scrapy.Request(url, callback=self.parse)


class CrawlReferenceDocHtml(scrapy.Spider):
    name = 'crawlReferenceDocHtml'

    # Urls of Spring Reference Doc's chapters
    start_urls = [
        'https://docs.spring.io/spring-framework/docs/current/reference/html/overview.html#overview',
        'https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#spring-core',
        'https://docs.spring.io/spring-framework/docs/current/reference/html/testing.html#testing',
        'https://docs.spring.io/spring-framework/docs/current/reference/html/data-access.html#spring-data-tier',
        'https://docs.spring.io/spring-framework/docs/current/reference/html/web.html#spring-web',
        'https://docs.spring.io/spring-framework/docs/current/reference/html/web-reactive.html#spring-webflux',
        'https://docs.spring.io/spring-framework/docs/current/reference/html/integration.html#spring-integration',
        'https://docs.spring.io/spring-framework/docs/current/reference/html/languages.html#languages'
    ]

    def parse(self, response):
        item = ApidocspiderItem()
        item["url"] = response.url
        item["html"] = response.text
        yield item
