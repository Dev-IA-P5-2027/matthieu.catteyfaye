import scrapy
from scrapy import Request
from WebCrawler.items import MediumRepoItem

class MalSpider(scrapy.Spider):
    name = "mal_spider"
    allowed_domains = ["myanimelist.net"]
    # On part de la page principale, comme dans le tuto
    start_urls = ["https://myanimelist.net/manga.php"]

    def parse(self, response):
        # Récupère les URLs de chaque lettre via la navbar alphabétique
        xp = "//div[@id='horiznav_nav']//li/a/@href"
        for url in response.xpath(xp).getall():
            yield Request(response.urljoin(url), callback=self.parse_manga_list_page)

    def parse_manga_list_page(self, response):
        # Sélecteur CSS pour les lignes de manga (adapté à la structure actuelle)
        for row in response.css('div.js-categories-seasonal tr ~ tr'):
            title = row.css('a[id] strong::text').get()

            if not title:
                continue
            title = title.strip()

            type_manga = row.css('td:nth-child(3)::text').get()
            score = row.css('td:nth-child(5)::text').get()

            item = MediumRepoItem()
            item['title'] = title
            item['type_manga'] = type_manga.strip() if type_manga else "N/A"
            item['score'] = score.strip() if score else "N/A"
            yield item

        # Pagination : on passe à la page suivante si elle existe
        next_urls = response.xpath("//div[@class='spaceit']//a/@href").getall()
        for next_url in next_urls:
            yield Request(response.urljoin(next_url), callback=self.parse_manga_list_page)