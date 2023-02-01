from email.mime import image
from numpy import product
import scrapy
import pandas as pd
import logging
import os
from pathlib import Path

SpreadsheetSource = Path(__file__).parent.parent.parent.parent /  "listini/Active2023.xlsx"
class ActiveSpider(scrapy.Spider):
    name = 'active'
    allowed_domains = ['www.active-srl.com']
    start_urls = [
        'https://www.active-srl.com/it/catalogo/rasaerba/macchine-specifiche-mulching',
        'https://www.active-srl.com/it/catalogo/rasaerba/scocca-lamiera',
        'https://www.active-srl.com/it/catalogo/rasaerba/scocca-alluminio',
        'https://www.active-srl.com/it/catalogo/generatori/generatori-di-corrente',
        'https://www.active-srl.com/it/catalogo/trivelle',
        'https://www.active-srl.com/it/catalogo/decespugliatori/professionali-zaino-multifunzione',
        'https://www.active-srl.com/it/catalogo/rasaerba/macchine-specifiche-mulching',
        'https://www.active-srl.com/it/catalogo/arieggiatore',
        'https://www.active-srl.com/it/catalogo/motozappe'

        ]

    custom_settings = {
        'IMAGES_STORE': './../output/images/active',
        'FEED_URI' : "./../output/active.xlsx",
        'FEED_EXPORT_FIELDS': ["Cod.", "Descrizione", "Categoria", "Sottocategoria", "Listino 4 (ivato)", "Note", "Produttore", "Cod. Fornitore", "Categoria", "Immagine", "Internet"],
    }

    df = pd.read_excel(SpreadsheetSource)

    def parse(self, response):
        for link in response.css('div.product a.see-details-hover::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_products)

    def parse_products(self, response):
        descrizione = response.css('h1::text').get().strip() if response.css('h1::text').get() is not None else None
        sottocategoria = response.css('li.expanded.active-trail a:first-child::text').get().strip() if response.css('li.expanded.active-trail a:first-child::text').get() is not None else None
        description = response.css('div.content.product-page div.description::text').get().strip() if response.css('div.content.product-page div.description::text').get() is not None else None
        details = response.xpath('//*[@id="description"]/div/div/ul/li').xpath('normalize-space()').getall() if response.css('div#description ul li').get() is not None else None
        note = "\n".join(details)
        img_name = descrizione.replace(" ","-")
        img_src = [response.urljoin(response.css('article.product-page div.image-box div.general-img img:first-child::attr(src)').get())]
        prod_cod = self.df.loc[self.df["Descrizione"] == descrizione.upper(), "Codice"].item()
        prod_price = self.df.loc[self.df["Descrizione"] == descrizione.upper(), "Pubblico +IVA"].item()

        yield {
            'Cod.': prod_cod,
            'Sottocategoria': sottocategoria,
            'Descrizione': descrizione,
            'Listino 4 (ivato)': prod_price,
            'Note': note,
            'Produttore': "Active srl",
            'Cod. Fornitore': "0006",
            'Categoria': "Macchine",
            'Internet': response.url,
            'Immagine': "C:\\ImmaginiDanea\\active\\"+img_name+".jpg",
            'image_urls' : img_src,
            'image_name' : img_name,
        }