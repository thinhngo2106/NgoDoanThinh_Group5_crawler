import scrapy
import json

class WearSpider(scrapy.Spider):
    name = "wear"
    dem = 0
    start_urls = ['https://www.wear.com.vn/']
    def parse(self, response):
        #kiểm tra điều kiện trang có trả về không, trang có phải là trang mô tả sản phẩm hay không
        if response.status == 200 and response.css('meta[property="og:type"]::attr("content")').get() == 'product':
            data = {
                'link': response.url,
                'Thương hiệu': response.css('table#chi-tiet tbody tr td.last a::text').get(),
                'Tình trạng' : response.css('div.group-status > span.first_status > span.status_name.availabel::text').get().replace("\t","").replace("\n",""),
                'Tên': response.css('h1.title-product::text').get(),
                'Ảnh': response.css('div.hidden > div.item > a::attr(href)').getall(),
                'Giá bán': response.css('div.price-box span.special-price  span.price::text').get(),
                'Giá cũ': response.css('div.price-box > span.old-price > del.price.product-price-old.sale::text').get()
            }

            with open('C:/Users/Thinh/PycharmProjects/Crawl_data/tutorial/tutorial/spiders/output/outputtiki.txt', 'a', encoding='utf8') as f:
                f.write(json.dumps(data, ensure_ascii=False))
                f.write('\n')
                self.CRAWLED_COUNT += 1
                self.crawler.stats.set_value('CRAWLED_COUNT', self.CRAWLED_COUNT)
                print('SUCCESS:', response.url)

        yield from response.follow_all(css='a[href^="https://www.wear.com.vn"]::attr(href), a[href^="/"]::attr(href)', callback=self.parse)