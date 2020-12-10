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
import re
import scrapy
import json
from APIDocSpider.items import ApidocspiderItem


class CrawlClassSpider(scrapy.Spider):
    API_TYPE = {
        'Constructor Summary': 7,
        'Method Summary': 11,

        'Parameters': 14,
        'Returns': 15,
        'Throws': 16
    }
    METHOD_MODIFIER = [
        'public',
        'private',
        'protected',
        'final',
        'static',
        'synchronize',
        'native'
    ]
    name = 'crawlAttribute'

    # Construct the URL based on the crawled class API name to crawl field, method, enum constant and so on.
    with open('./APIDocSpider/output/class.json', 'r') as f:
        url_list = json.load(f)
    offset = 0
    baseURL = 'https://docs.spring.io/spring-framework/docs/current/javadoc-api/'
    start_urls = [baseURL
                  + url_list[offset]["qualified_name"].split(url_list[offset]["full_declaration"])[0].replace('.', '/')
                  + url_list[offset]["full_declaration"] + '.html']

    # Set a unique ID for each API
    api_id = 35800

    def parse(self, response):
        node_list = response.xpath("//div[@class='summary']/ul/li/ul/li/table")
        for index1, node in enumerate(node_list):
            api_type = node.xpath("../h3/text()").extract()[0]

            # Don't consider 'Nested Class Summary', because it has been processed as 'Class Summary'in crawClass.
            if api_type not in self.API_TYPE.keys():
                continue

            subnode_list = node.xpath("./tr[position()>1]")
            for index2, subnode in enumerate(subnode_list):
                # url to locate method detail page
                method_detail_url = ''

                full_declared_param_list = []
                qualified_param_type_list = []
                param_value_list = []

                # Process parameters
                if api_type == 'Constructor Summary':
                    method_detail_url = subnode.xpath("./td/code/span/a/@href").extract()[0].rsplit('#', 1)[1]
                    # full_declaration = self.url_list[self.offset]["full_declaration"]
                    qualified_param_type_list = [item for item in subnode.xpath("./td/code/span/a/@href").extract()[0]
                        .split(self.url_list[self.offset]["full_declaration"], 1)[1].split('-') if
                                                 item not in {'-', '', ' '}]
                    del qualified_param_type_list[0]
                    method_full_declaration = ' '.join(
                        [n.replace('\n', ' ') for n in subnode.xpath("./td/code//text()").extract()])
                    if method_full_declaration.split('(', 1)[1].strip(')'):
                        full_declared_param_list = re.findall("[a-zA-Z0-9_][^\u00a0]*[\u00a0]{1}[a-zA-Z0-9_]+",
                                                              method_full_declaration.split('(', 1)[1].strip(')'))
                    else:
                        full_declared_param_list = method_full_declaration.split('(', 1)[1].strip(')')
                    param_value_list = [param.split('\u00a0', 1)[1] for param in full_declared_param_list if
                                        full_declared_param_list]
                elif api_type == 'Method Summary':
                    method_detail_url = subnode.xpath("./td[2]/code/span/a/@href").extract()[0].rsplit('#', 1)[1]
                    qualified_param_type_list = [item for item in
                                                 subnode.xpath("./td[2]/code/span/a/@href").extract()[0]
                                                     .split(
                                                     self.url_list[self.offset]["full_declaration"], 1)[1].split('-') if
                                                 item not in {'-', '', ' '}]
                    del qualified_param_type_list[0]
                    method_full_declaration = ' '.join(
                        [n.replace('\n', ' ') for n in subnode.xpath("./td[2]/code//text()").extract()])
                    if method_full_declaration.split('(', 1)[1].strip(')'):
                        full_declared_param_list = re.findall("[a-zA-Z0-9_][^\u00a0]*[\u00a0]{1}[a-zA-Z0-9_]+",
                                                              method_full_declaration.split('(', 1)[1].strip(')'))
                    else:
                        full_declared_param_list = method_full_declaration.split('(', 1)[1].strip(')')
                    param_value_list = [param.split('\u00a0', 1)[1] for param in full_declared_param_list if
                                        full_declared_param_list]

                # crawl method detail nodes
                method_node_list = response.xpath(
                    "//div[@class='details']/ul/li/ul[" + str(
                        index1 + 1) + "]/li/a[@name='" + method_detail_url + "']/following::*[1]/li/dl/dt")
                attribute_index_list = self.get_attribute_index(method_node_list)

                # When parameter is not empty, but there is not introduction of parameter in method detail page
                if full_declared_param_list and 'Parameters:' not in response.xpath(
                        "//div[@class='details']/ul/li/ul[" + str(index1 + 1) + "]/li/ul[" + str(
                            index2 + 1) + "]/li/dl/dt/span/text()").extract():
                    for i in range(len(full_declared_param_list)):
                        item = ApidocspiderItem()
                        item["api_id"] = self.api_id
                        item["api_type"] = self.API_TYPE['Parameters']
                        item["full_declaration"] = full_declared_param_list[i].strip()
                        item["qualified_name"] = (qualified_param_type_list[i] + ' ' + param_value_list[i]).strip()
                        item["short_description"] = ''
                        self.api_id += 1
                        yield item

                # When there is not introduction of return in method detail page
                if api_type == 'Method Summary' and 'Returns:' not in response.xpath(
                        "//div[@class='details']/ul/li/ul[" + str(index1 + 1) + "]/li/ul[" + str(
                            index2 + 1) + "]/li/dl/dt/span/text()").extract():
                    item = ApidocspiderItem()
                    item["api_id"] = self.api_id
                    item["api_type"] = self.API_TYPE['Returns']

                    modifier_and_type = ' '.join(
                        [n.strip('\n')
                         for n in subnode.xpath("./td[1]/code//text()").extract()]).split(' ', 1)
                    if modifier_and_type[0] in self.METHOD_MODIFIER:
                        item["full_declaration"] = ' '.join(modifier_and_type[1:]).strip()
                    else:
                        item["full_declaration"] = ' '.join(modifier_and_type).strip()

                    if subnode.xpath("./td[1]/code/a/@href"):
                        if re.findall("api/(.*?).html", subnode.xpath("./td[1]/code/a/@href").extract()[0]):
                            item["qualified_name"] = (re.findall("api/(.*?).html",
                                                                 subnode.xpath("./td[1]/code/a/@href").extract()[0]
                                                                 )[0].replace('/', '.') + " (R)").strip()
                        elif re.findall("\.\./(.*?).html", subnode.xpath("./td[1]/code/a/@href").extract()[0]):
                            item["qualified_name"] = (re.findall("(.*?).html",
                                                                 subnode.xpath(
                                                                     "./td[1]/code/a/@href").extract()[0].rsplit('../',
                                                                                                                 1)[1]
                                                                 )[0].replace('/', '.') + " (R)").strip()
                        else:
                            item["qualified_name"] = item["full_declaration"].strip()
                    else:
                        item["qualified_name"] = item["full_declaration"].strip()

                    item["short_description"] = ''
                    self.api_id += 1
                    yield item

                for index3, method_node in enumerate(method_node_list):
                    attribute_type = method_node.xpath("./span/text()").extract()[0].strip(':')
                    start_index = sum(attribute_index_list[:index3]) + 1
                    if attribute_type == 'Parameters':
                        for i in range(attribute_index_list[index3]):
                            item = ApidocspiderItem()
                            item["api_id"] = self.api_id
                            item["api_type"] = self.API_TYPE[attribute_type]
                            item["full_declaration"] = full_declared_param_list[i].strip()
                            item["qualified_name"] = (qualified_param_type_list[i] + ' ' + param_value_list[i]).strip()
                            item["short_description"] = ' '.join(
                                [n.strip('\n')
                                 for n in method_node.xpath("../dd[" + str(start_index + i) + "]/text()").extract()]
                            ).split('-', 1)[1].strip()
                            self.api_id += 1
                            yield item
                    elif attribute_type == 'Returns':
                        for i in range(attribute_index_list[index3]):
                            item = ApidocspiderItem()
                            item["api_id"] = self.api_id
                            item["api_type"] = self.API_TYPE[attribute_type]

                            modifier_and_type = ' '.join(
                                [n.strip('\n')
                                 for n in subnode.xpath("./td[1]/code//text()").extract()]).split(' ', 1)
                            if modifier_and_type[0] in self.METHOD_MODIFIER:
                                item["full_declaration"] = ' '.join(modifier_and_type[1:]).strip()
                            else:
                                item["full_declaration"] = ' '.join(modifier_and_type).strip()

                            if subnode.xpath("./td[1]/code/a/@href"):
                                if re.findall("api/(.*?).html", subnode.xpath("./td[1]/code/a/@href").extract()[0]):
                                    item["qualified_name"] = (re.findall("api/(.*?).html",
                                                                         subnode.xpath(
                                                                             "./td[1]/code/a/@href").extract()[0]
                                                                         )[0].replace('/', '.') + " (R)").strip()
                                elif re.findall("\.\./(.*?).html", subnode.xpath(
                                        "./td[1]/code/a/@href").extract()[0]):
                                    item["qualified_name"] = (re.findall("(.*?).html",
                                                                         subnode.xpath(
                                                                             "./td[1]/code/a/@href").extract()[
                                                                             0].rsplit('../', 1)[1]
                                                                         )[0].replace('/', '.') + " (R)").strip()
                                else:
                                    item["qualified_name"] = item["full_declaration"].strip()
                            else:
                                item["qualified_name"] = item["full_declaration"].strip()

                            item["short_description"] = ' '.join(
                                [n.strip('\n')
                                 for n in method_node.xpath("../dd[" + str(start_index + i) + "]/text()").extract()]
                            ).strip()
                            self.api_id += 1
                            yield item
                    elif attribute_type == 'Throws':
                        for i in range(attribute_index_list[index3]):
                            item = ApidocspiderItem()
                            item["api_id"] = self.api_id
                            item["api_type"] = self.API_TYPE[attribute_type]
                            item["full_declaration"] = method_node.xpath("../dd[" + str(start_index + i) +
                                                                         "]/code//text()").extract()[0].strip()
                            if method_node.xpath("../dd[" + str(start_index + i) +
                                                 "]/code/a/@href"):
                                if re.findall("api/(.*?).html", method_node.xpath("../dd[" + str(start_index + i) +
                                                                                  "]/code/a/@href").extract()[0]):
                                    item["qualified_name"] = (re.findall("api/(.*?).html",
                                                                         method_node.xpath(
                                                                             "../dd[" + str(start_index + i) +
                                                                             "]/code/a/@href").extract()[0]
                                                                         )[0].replace('/', '.') + " (E)").strip()
                                elif re.findall("\.\./(.*?).html", method_node.xpath(
                                        "../dd[" + str(start_index + i) +
                                        "]/code/a/@href").extract()[0]):
                                    item["qualified_name"] = (re.findall("(.*?).html",
                                                                         method_node.xpath(
                                                                             "../dd[" + str(start_index + i) +
                                                                             "]/code/a/@href").extract()[
                                                                             0].rsplit('../', 1)[1]
                                                                         )[0].replace('/', '.') + " (E)").strip()
                                else:
                                    item["qualified_name"] = item["full_declaration"]
                            else:
                                item["qualified_name"] = item["full_declaration"]
                            if len([n.strip('\n') for n in method_node.xpath(
                                    "../dd[" + str(start_index + i) + "]/text()").extract()]) == 1:
                                item["short_description"] = ' '.join(
                                    [n.strip('\n')
                                     for n in method_node.xpath("../dd[" + str(start_index + i) + "]/text()").extract()]
                                ).split('-', 1)[1].strip()
                            else:
                                item["short_description"] = ''
                            self.api_id += 1
                            yield item

        # Construct next new URL based on the crawled package API name to crawl API.
        if self.offset < len(self.url_list) - 1:
            self.offset += 1
            url = self.baseURL + \
                  self.url_list[self.offset]["qualified_name"].split(self.url_list[self.offset]["full_declaration"])[
                      0].replace('.', '/') + self.url_list[self.offset]["full_declaration"] + '.html'
            yield scrapy.Request(url, callback=self.parse)

    def get_attribute_index(self, method_node_list):
        attribute_index_list = []
        for index, method_node in enumerate(method_node_list):
            if index == len(method_node_list) - 1:
                attribute_index_list.append(
                    len(method_node.xpath("../dt[" + str(index + 1) + "]/following-sibling::*")))
                break
            attribute_index_list.append(len(method_node.xpath("../dt[" + str(index + 1) + "]/following-sibling::*")) -
                                        len(method_node.xpath(
                                            "../dt[" + str(index + 2) + "]/following-sibling::*")) - 1)
        return attribute_index_list
