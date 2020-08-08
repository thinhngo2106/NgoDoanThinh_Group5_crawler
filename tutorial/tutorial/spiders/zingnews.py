import scrapy


class ZingNewsSpider(scrapy.Spider):
    name = "zingnews"
    links_list =[]
    dem = 0
    start_urls = ['https://zingnews.vn/']

    id = 1115947

    def parse(self, response):
        #kiểm tra điều kiện trang có trả về không, trang có phải là bài viết hay không
        if response.status == 200 and response.css('meta[property="og:url"]::attr("content")').get() != '' and response.css('meta[http-equiv="REFRESH"]::attr("content")').get() is not None:
            #mở file lưu dữ liệu
            f = open('C:/Users/Thinh/PycharmProjects/Crawl_data/tutorial/tutorial/spiders/output/output.txt','a+',  encoding='utf-8')
            print(ZingNewsSpider.dem)
            #lấy link
            url = response.url
            f.write(url + '\n')
            #lấy tên chủ dề
            topic = response.css('p.the-article-category a::text').get()
            f.write("Chủ đề: " + topic.strip() + '\n')
            #lấy tiêu đề của bài báo
            title = response.css("h1.the-article-title::text").get()
            f.write("Tiêu đề: " + title.strip() + '\n')
            #lấy tóm tắt bài báo
            summary = response.css('p.the-article-summary::text').get()
            f.write("Tóm tắt: " + summary.strip() + '\n')
            #lấy nội dung
            content = '\n'.join([
                    ''.join(c.css('*::text').getall())
                        for c in response.css('div.the-article-body p')
                ])
            f.write(content + '\n')
            #lấy thời gian bài báo đăng
            date = response.css('li.the-article-publish::text').get()
            f.write("Thòi gian: " + date.strip() + '\n')


        link = 'https://zingnews.vn/zingnews-post' + str(ZingNewsSpider.id) + '.html'
        if ZingNewsSpider.id > 0:
            yield response.follow(link, callback=self.parse,dont_filter=True)
            #cho chạy từ id bài báo đã cho
            ZingNewsSpider.id -= 1
            ZingNewsSpider.dem += 1

