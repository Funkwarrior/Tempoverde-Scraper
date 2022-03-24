import scrapy
from scrapy.http import FormRequest

def start_requests(self):
   return [
      FormRequest("INSERT URL", formdata={"user":"D1037749",
           "pass":"iU521hDE"}, callback=self.parse)]

class HvaSpider(scrapy.Spider):
    name = 'hva'
    allowed_domains = ['supportsites.husqvarnagroup.com']
    start_urls = ['http://supportsites.husqvarnagroup.com/']

    def parse(self, response):
        pass
