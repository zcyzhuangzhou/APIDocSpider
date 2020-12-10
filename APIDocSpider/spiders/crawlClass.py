#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: Chengyuan Zhao
@Email: 19110240027@fudan.edu.cn
@Created: 2020/11/16
------------------------------------------
@Modify: 2020/11/17
------------------------------------------
@Description:
"""
import scrapy
import json
from APIDocSpider.items import ApidocspiderItem


class CrawlClassSpider(scrapy.Spider):
    # Modify the corresponding API types based on specific HTML page information
    API_TYPE = {"Class Summary": 2,
                "Interface Summary": 3,
                "Exception Summary": 4,
                "Enum Summary": 8,
                "Annotation Types Summary": 9}

    name = 'crawlClass'

    # Construct the URL to crawl class API based on the crawled package API name
    with open('./APIDocSpider/output/package.json', 'r') as f:
        url_list = json.load(f)
    offset = 0
    baseURL = 'https://docs.spring.io/spring-framework/docs/current/javadoc-api/'
    start_urls = [baseURL + url_list[offset]["qualified_name"].replace('.', '/') + '/package-summary.html']

    # Set a unique ID for each API
    api_id = 414

    def parse(self, response):
        node_list = response.xpath("//ul[@class='blockList']/li/table")
        package_name = response.xpath("//h1//text()").extract()[0].split('Package')[1].strip()
        for index, node in enumerate(node_list):
            class_type = node.xpath("./caption/span[1]//text()").extract()[0]
            subnode_list = node.xpath("./tbody/tr")
            for subnode in subnode_list:
                item = ApidocspiderItem()
                item["api_id"] = self.api_id
                item["api_type"] = self.API_TYPE[class_type]
                item["full_declaration"] = subnode.xpath("./td[1]//text()").extract()[0]
                item["qualified_name"] = package_name + '.' + subnode.xpath("./td[1]//text()").extract()[0]
                item["short_description"] = ' '.join([n.strip('\n') for n in subnode.xpath("./td[2]//text()").extract()])
                self.api_id += 1
                yield item

        # Construct next new URL to crawl class API based on the crawled package API name
        if self.offset < len(self.url_list) - 1:
            self.offset += 1
            url = self.baseURL + self.url_list[self.offset]["qualified_name"].replace('.', '/') + '/package-summary.html'
            yield scrapy.Request(url, callback=self.parse)
