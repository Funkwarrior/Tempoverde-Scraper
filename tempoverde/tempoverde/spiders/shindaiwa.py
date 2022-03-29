from email.mime import image
from numpy import product
import scrapy
from tempoverde.items import ImgItem
import logging


class ShindaiwaSpider(scrapy.Spider):
    name = 'shindaiwa'
    allowed_domains = ['shindaiwa-italia.it']
    start_urls = [
                'https://www.shindaiwa-italia.it/prodotti/motoseghe/motoseghe-potatura',
                'https://www.shindaiwa-italia.it/prodotti/motoseghe/motoseghe-multifunzione',
                'https://www.shindaiwa-italia.it/prodotti/motoseghe/motoseghe-forestali',
                'https://www.shindaiwa-italia.it/prodotti/potatori/potatori-telescopici',
                'https://www.shindaiwa-italia.it/prodotti/soffiatori/soffiatori-aspiratori',
                'https://www.shindaiwa-italia.it/prodotti/soffiatori/soffiatori-a-mano',
                'https://www.shindaiwa-italia.it/prodotti/soffiatori/soffiatori-a-zaino',
                'https://www.shindaiwa-italia.it/prodotti/tosasiepi/tosasiepi-ad-asta',
                'https://www.shindaiwa-italia.it/prodotti/tosasiepi/tosasiepi-a-doppia-lama',
                'https://www.shindaiwa-italia.it/prodotti/tosasiepi/tosasiepi-a-lama-singola',
                'https://www.shindaiwa-italia.it/prodotti/decespugliatori/decespugliatori-a-zaino',
                'https://www.shindaiwa-italia.it/prodotti/decespugliatori/decespugliatori-standard',
                'https://www.shindaiwa-italia.it/prodotti/altre-macchine/macchina-multifunzione',
                'https://www.shindaiwa-italia.it/prodotti/altre-macchine/mototroncatrice',
                'https://www.shindaiwa-italia.it/prodotti/accessori/lame-e-catene',
                'https://www.shindaiwa-italia.it/prodotti/accessori/testine-a-filo',
                'https://www.shindaiwa-italia.it/prodotti/accessori/filo-in-nylon',
                'https://www.shindaiwa-italia.it/prodotti/accessori/dischi-di-taglio',
                'https://www.shindaiwa-italia.it/prodotti/accessori/altri-accessori',
                'https://www.shindaiwa-italia.it/prodotti/accessori/protettivo-catene',
                'https://www.shindaiwa-italia.it/prodotti/accessori/olio-mix',
                'https://www.shindaiwa-italia.it/prodotti/accessori/abbigliamento-antitaglio',
                'https://www.shindaiwa-italia.it/prodotti/accessori/abbigliamento-protettivo',
                'https://www.shindaiwa-italia.it/prodotti/accessori/abbigliamento-casual',
                ]

    custom_settings = {
        'IMAGES_STORE': './../output/images/shindaiwa',
        'FEED_URI' : "./../output/shindaiwa.xlsx"
    }

    def parse(self, response):
        for link in response.css('section#product-list a.c-item::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_products)

    def parse_products(self, response):
        descrizione = response.css('h1::text').get().strip() if response.css('h1::text').get() is not None else None
        #sottocategoria = response.css('li.expanded.active-trail a:first-child::text').get().strip() if response.css('li.expanded.active-trail a:first-child::text').get() is not None else None
        price = response.css('h2.c-product__price::text').get().strip().replace("€","").replace(" ","").replace(".","").replace("*","") if response.css('h2.c-product__price::text').get() is not None else None
        description = response.css('div#long-description p::text').get().strip() if response.css('div#long-description p::text').get() is not None else None
        details = response.xpath('//*[@class="c-product__data"]/table//tr').xpath('normalize-space()').getall() if response.xpath('//*[@class="c-product__data"]/table//tr').get() is not None else None
        logging.debug("=============================")
        logging.debug(description)

        note = ""

        if description is not None:
            note = description

        if details is not None:
            note = note +"\n".join(details)


        yield {
            # 'Sottocategoria': sottocategoria,
            'Descrizione': descrizione,
            'Listino 4 (ivato)': price,
            'Produttore': "Shindaiwa",
            'Cod. Fornitore': "0000",
            'Categoria': "Macchine",
            'Internet': response.url,
            'Note': note,
        }

        img = ImgItem()
        img['image_urls'] = [response.urljoin(response.css('ul.c-slider__wrap  img::attr(src)').get())]
        img['image_name'] = descrizione.replace(" ","-").replace("/", "-")

        yield img