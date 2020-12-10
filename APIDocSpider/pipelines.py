# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

from APIDocSpider.data.db.html_model import ApiDocHtmlModel, ReferenceDocHtmlModel
from definitions import MYSQL_FACTORY


class ApidocspiderPipeline:
    def open_spider(self, spider):
        self.f = open('./APIDocSpider/output/method.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.f.write(line)
        return item

    def close_spider(self, spider):
        self.f.close()


class HtmlSpiderPipeline:
    def open_spider(self, spider):
        self.session = MYSQL_FACTORY.create_mysql_session_by_server_name(server_name="33RootServer",
                                                                         database="spring",
                                                                         echo=False)

    def process_item(self, item, spider):
        # html_model = ApiDocHtmlModel(item)
        html_model = ReferenceDocHtmlModel(item)
        html_model.insert(session=self.session)
        return item

    def close_spider(self, spider):
        self.session.close()
