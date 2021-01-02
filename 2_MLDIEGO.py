from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader


class articulos(Item):

    Titulo= Field()
    Precio=Field()

    Direccion= Field ()
    Porcentaje_de_recomendaciones= Field()
    Antiguedad= Field()
    Ventas_concretadas= Field()
    url= Field ()


class mercadolibre(CrawlSpider):
    name= "MercadoLibreSpider"
    custom_settings = {
      'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
      'CLOSESPIDER_PAGECOUNT': 250 # Max number of pages to scrape
    }
    allowed_domains = ['zapatos.mercadolibre.com.ve', 'articulo.mercadolibre.com.ve']

    start_urls=["https://zapatos.mercadolibre.com.ve/zapatos/"]

    download_delay= 1

    rules=(
        Rule(
            LinkExtractor(
                allow=r"/_Desde_\d+"
            ), follow=True

        ),
        Rule(
            LinkExtractor(
                allow=r"/MLV-"
            ),follow=True, callback="parse_items"

        ),
        )
    
    def LimpiarTexto (self,texto):
        nuevo_texto=texto.replace("\n"," ").replace("\r", " ").replace("\t", " ").strip()
        return nuevo_texto

    def parse_items(self,response):

        item=ItemLoader(articulos(),response)

        item.add_xpath("Titulo","//h1/text()", MapCompose(self.LimpiarTexto))

        try:
            item.add_xpath("Precio","//fieldset[@class='item-price  ']/span/span[2]/text()")
        except:
             item.add_xpath("Precio","//fieldset[@class='item-price  item-price__more-than-six']//span[@class='price-tag-fraction']/text()")
             
        try:
            item.add_xpath("Direccion","//div[@class='card-section seller-location']//p[@class='card-description text-light']/strong/text()")
        except:
            item.add_xpath("Direccion","//p[class='text-light']/text()")

        item.add_xpath("Porcentaje_de_recomendaciones","//div[@class='reputation-info block']/dl/dd[1]/strong/text()")

        try:
            item.add_xpath("Antiguedad","//div[@class='reputation-info block']/dl/dd[2]/strong/text()")
        except:
            item.add_xpath("Antiguedad","informacion no suministrada")
        try:
            item.add_xpath("Ventas_concretadas","//div[@class='reputation-info block']/dl/dd[3]/strong/text()")
        except:
            item.add_xpath("Ventas_concretadas","informacion no suministrada")
        try:

            item.add_xpath("url","//link[@rel='canonical']/@href")

        except:
            item.add_xpath("url","informacion no suministrada")


        yield item.load_item()

  


    #scrip to run: scrapy runspider 2_MLDIEGO.py -o MLShoes.csv -t csv
      #scrip to run: scrapy runspider 2_MLDIEGO.py -o MLShoes.xlsx -t xlsx


