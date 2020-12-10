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
import scrapy
import json
from APIDocSpider.items import ApidocspiderItem


class CrawlClassSpider(scrapy.Spider):
    API_TYPE = {'Field Summary': 6,
                'Constructor Summary': 7,
                'Method Summary': 11,
                'Enum Constant Summary': 12,
                # 'Nested Class Summary',

                # This two elements are in annotations
                'Optional Element Summary': 29,
                'Required Element Summary': 30}
    name = 'crawlMethod'

    # Construct the URL based on the crawled class API name to crawl field, method, enum constant and so on.
    with open('./APIDocSpider/output/class.json', 'r') as f:
        url_list = json.load(f)
    offset = 0
    baseURL = 'https://docs.spring.io/spring-framework/docs/current/javadoc-api/'
    start_urls = [baseURL
                  + url_list[offset]["qualified_name"].split(url_list[offset]["full_declaration"])[0].replace('.', '/')
                  + url_list[offset]["full_declaration"] + '.html']
    # start_urls = ['https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/test/web/servlet/ResultMatcher.html']
    # Set a unique ID for each API
    api_id = 4419

    def parse(self, response):
        node_list = response.xpath("//div[@class='summary']/ul/li/ul/li/table")
        class_name = self.url_list[self.offset]["qualified_name"]
        for index, node in enumerate(node_list):
            api_type = node.xpath("../h3/text()").extract()[0]

            # Don't consider 'Nested Class Summary', because it has been processed as 'Class Summary'in crawClass.
            if api_type == 'Nested Class Summary':
                continue

            subnode_list = node.xpath("./tr[position()>1]")
            for subnode in subnode_list:
                item = ApidocspiderItem()
                item["api_id"] = self.api_id
                item["api_type"] = self.API_TYPE[api_type]

                # The crawl rules for 'Constructor Summary' differ somewhat from those for other API
                if api_type == 'Constructor Summary':
                    item["full_declaration"] = ' '.join([n.replace('\n', ' ') for n in subnode.xpath("./td/code//text()").extract()])
                    item["qualified_name"] = class_name + '.' + ' '.join([n.replace('\n', ' ') for n in subnode.xpath("./td/code//text()").extract()])
                    item["short_description"] = ' '.join(
                        [n.replace('\n', ' ') for n in subnode.xpath("./td/div//text()").extract()])
                else:
                    item["full_declaration"] = ' '.join([n.replace('\n', ' ') for n in subnode.xpath("./td[1]//text()").extract()]) + ' ' + \
                                               ' '.join([n.replace('\n', ' ') for n in subnode.xpath("./td[2]/code//text()").extract()])
                    item["qualified_name"] = class_name + '.' + ' '.join([n.replace('\n', ' ') for n in subnode.xpath("./td[2]/code//text()").extract()])
                    item["short_description"] = ' '.join(
                        [n.replace('\n', ' ') for n in subnode.xpath("./td[2]/div//text()").extract()])
                self.api_id += 1
                yield item

        # Construct next new URL based on the crawled package API name to crawl API.
        if self.offset < len(self.url_list) - 1:
            self.offset += 1
            url = self.baseURL + self.url_list[self.offset]["qualified_name"].split(self.url_list[self.offset]["full_declaration"])[0].replace('.', '/') + self.url_list[self.offset]["full_declaration"] + '.html'
            yield scrapy.Request(url, callback=self.parse)
