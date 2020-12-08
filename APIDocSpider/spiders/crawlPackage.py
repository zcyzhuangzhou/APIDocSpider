#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: Chengyuan Zhao
@Email: 19110240027@fudan.edu.cn
@Created: 2020/11/16
------------------------------------------
@Modify: 2020/11/16
------------------------------------------
@Description:
"""
import scrapy

from APIDocSpider.items import ApidocspiderItem


class CrawlPackageSpider(scrapy.Spider):
    name = 'crawlPackage'
    # allowed_domains = ['https://docs.spring.io/spring-framework/docs/current/javadoc-api']
    start_urls = ['https://docs.spring.io/spring-framework/docs/current/javadoc-api/overview-summary.html']

    # Set a unique ID for each API
    api_id = 1

    def parse(self, response):
        node_list = response.xpath("//tbody/tr")
        for node in node_list:
            item = ApidocspiderItem()
            item["api_id"] = self.api_id
            item["api_type"] = 1
            item["qualified_name"] = node.xpath("./td/a//text()").extract()[0]
            item["full_declaration"] = node.xpath("./td/a//text()").extract()[0]
            item["short_description"] = ' '.join([n.strip('\n') for n in node.xpath("./td/div//text()").extract()])
            self.api_id += 1
            yield item
