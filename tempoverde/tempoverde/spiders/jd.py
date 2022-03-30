from dataclasses import replace
from itertools import product
import scrapy
import logging

class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['deere.it']
    start_urls = [
        'https://www.deere.it/it/tosaerba-professionali/trattorini-tosaerba-diesel/',
        'https://www.deere.it/it/tosaerba-professionali/tosaerba-a-raggio-di-sterzata-zero/',
        'https://www.deere.it/it/tosaerba-professionali/frontali-a-taglio-rotativo/',
        'https://www.deere.it/it/tosaerba-professionali/tosaerba-a-taglio-rotativo-per-ampie-superfici/',
        'https://www.deere.it/it/tosaerba/trattorini/serie-ztrak/',
        'https://www.deere.it/it/tosaerba/trattorini/serie-x100/',
        'https://www.deere.it/it/tosaerba/trattorini/serie-x300/',
        'https://www.deere.it/it/tosaerba/trattorini/serie-x500/',
        ]

    custom_settings = {
        'IMAGES_STORE': './../output/images/jd',
        'FEED_URI' : "./../output/jd.xlsx",
        'FEED_EXPORT_FIELDS': ["Descrizione", "Categoria", "Sottocategoria", "Listino 4 (ivato)", "Note", "Produttore", "Cod. Fornitore", "Categoria", "Immagine", "Internet"],
    }

    def parse(self, response):
        for link in response.css('div.table-comp th.first a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_products)

    def parse_products(self, response):
        specs = response.xpath("//div[@class='details']/ul//li").xpath('normalize-space()').getall()
        details = response.xpath("//div[@class='specifications-comp nav-section']//div[@class='table-container']//tr").xpath('normalize-space()').getall()
        note = "\n".join(specs) + "\n" + "\n".join(details)
        img_name = response.css('h1 span.model::text').get().strip().replace(" ","-")
        img_src = [response.urljoin(response.xpath('//*[@class="image-wrapper slides"]/li/picture/source[3]/@srcset').get())]

        yield {
            'Sottocategoria': response.css('h1 span.category::text').get().strip() if response.css('h1 span.category::text').get() is not None else None,
            'Descrizione': response.css('h1 span.model::text').get().strip() if response.css('h1 span.model::text').get() is not None else None,
            'Listino 4 (ivato)': response.css('div.price span.value::text').get().strip().replace('*' , '').replace(' ', '').replace('€','') if response.css('div.price span.value::text').get() is not None else None,
            'Note': note,
            'Produttore': "John Deere",
            'Cod. Fornitore': "1751", # DOSE GIARDINAGGO s.n.c. di Dose Roberto & C.
            'Categoria': "Macchine",
            'Immagine' : "C:\\ImmaginiDanea\\jd\\"+img_name+".jpg",
            'Internet' : response.url,
            'image_urls' : img_src,
            'image_name' : img_name,
        }