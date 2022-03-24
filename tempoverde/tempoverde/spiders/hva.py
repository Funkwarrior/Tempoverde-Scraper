import scrapy
from scrapy.http import FormRequest

class HvaSpider(scrapy.Spider):
    name = 'hva'
    allowed_domains = ['supportsites.husqvarnagroup.com']
    start_urls = ['https://supportsites.husqvarnagroup.com/it']

    def parse(self,response):
        csrf_token = response.xpath('//*[@name="csrf_token"]/@value').extract_first()
        print(csrf_token)
        yield FormRequest.from_response(response, formdata={'csrf_token': csrf_token, 'username':'D1037749', 'password': 'iU521hDE'}, callback=self.parse_after_login)

    def parse_after_login(self,response):
        print(response.xpath('.//div[@class = "col-md-4"]/p/a/text()'))
