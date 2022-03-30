from email.mime import image
from numpy import product
import scrapy
import pandas as pd
import logging

class ActiveSpider(scrapy.Spider):
    name = 'active'
    allowed_domains = ['www.active-srl.com']
    start_urls = [
        'https://www.active-srl.com/it/catalogo/rasaerba/macchine-specifiche-mulching',
        'https://www.active-srl.com/it/catalogo/rasaerba/scocca-lamiera',
        'https://www.active-srl.com/it/catalogo/rasaerba/scocca-alluminio',
        ]

    custom_settings = {
        'IMAGES_STORE': './../output/images/active',
        'FEED_URI' : "./../output/active.xlsx",
        'FEED_EXPORT_FIELDS': ["Descrizione", "Categoria", "Sottocategoria", "Listino 4 (ivato)", "Note", "Produttore", "Cod. Fornitore", "Categoria", "Immagine", "Internet"],
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
        note = "\n".join(details)
        img_name = descrizione.replace(" ","-")
        img_src = [response.urljoin(response.css('article.product-page div.image-box div.general-img img:first-child::attr(src)').get())]

        #df = pd.read_excel('Active2021.xlsx')
        #logging.debug(df)
        #prod_cod = df.loc[df['Descrizione'] == img['image_name'], 'Codice'].item()
        #prod_price = df.loc[df['Descrizione'] == img['image_name'], 'Listino iva compresa'].item()
        #logging.debug("=============================")
        #logging.debug(prod_cod, prod_price)

        yield {
            'Sottocategoria': sottocategoria,
            'Descrizione': descrizione,
            'Listino 4 (ivato)': price,
            'Note': note,
            'Produttore': "Active srl",
            'Cod. Fornitore': "0000",
            'Categoria': "Macchine",
            'Internet': response.url,
            'Immagine': "C:\\ImmaginiDanea\\active\\"+img_name+".jpg",
            'image_urls' : img_src,
            'image_name' : img_name,
        }