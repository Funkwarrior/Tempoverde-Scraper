from email.mime import image
from numpy import product
import scrapy
from tempoverde.items import ImgItem

class ActiveSpider(scrapy.Spider):
    name = 'active'
    allowed_domains = ['www.active-srl.com']
    start_urls = [
        'https://www.active-srl.com/it/catalogo/rasaerba/macchine-specifiche-mulching',
        'https://www.active-srl.com/it/catalogo/rasaerba/scocca-lamiera',
        'https://www.active-srl.com/it/catalogo/rasaerba/scocca-alluminio',
        ]

    custom_settings = {
        'IMAGES_STORE': './images/active',
    }

    def parse(self, response):
        for link in response.css('div.product a.see-details-hover::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_products)

    def parse_products(self, response):
        descrizione = response.css('h1::text').get().strip() if response.css('h1::text').get() is not None else None
        sottocategoria = response.css('li.expanded.active-trail a:first-child::text').get().strip() if response.css('li.expanded.active-trail a:first-child::text').get() is not None else None
        price = 0
        description = response.css('div.content.product-page div.description::text').get().strip() if response.css('div.content.product-page div.description::text').get() is not None else None
        details = response.xpath('//*[@id="description"]/div/div/ul/li').xpath('normalize-space()').getall() if response.css('div#description ul li').get() is not None else None
        details_list = "\n".join(details)
        note = details_list

        img = ImgItem()
        img['image_urls'] = [response.css('article.product-page div.image-box div.general-img img:first-child::attr(src)').get()]
        img['image_name'] = descrizione.replace(" ","-")
        # yield img

        yield {
            'Sottocategoria': sottocategoria,
            'Descrizione': descrizione,
            'Listino 4 (ivato)': price,
            'Note': note,
            'Produttore': "Active srl",
            'Cod. Fornitore': "0000",
            'Categoria': "Macchine",
            'Internet': response.url
        }
