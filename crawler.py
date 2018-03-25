import scrapy


class YellowPageSpider(scrapy.Spider):
    name        = 'yellow_spider'
    hostname    = 'https://www.yellowpages.com/'
    keyword     = 'restaurant'
    location    = 'Boston%2C+MA'
    pages       = 10

    def start_requests(self):
        """
        Prepare urls for each of page we gonna crawl
        :return:
        """
        urls = [
            'https://www.yellowpages.com/search?search_terms=%s&geo_location_terms=%s&page=%d'%(self.keyword,self.location,p+1,) for p in range(self.pages)
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def regular_data(self,data):
        """
        Validate data and reformat
        :param data:
        :return:
        """
        _data = data.copy()
        _data['detail_url'] = self.hostname+_data['detail_url']
        _data['categories'] = _data['categories'].split(',') if _data['categories'] else None
        _data['address']['street'] = _data['address']['street'].strip() if _data['address']['street'] else ''
        _data['address']['locality'] = _data['address']['locality'].strip() if _data['address']['locality'] else ''
        # _data['address']['postal_code'] = _data['address']['postal_code'].strip()
        return _data


    def parse(self, response):
        """
        Parsing the HTML response with each xpath and regulate the data for further processing

        :param response:
        :return:
        """
        SET_SELECTOR = '.result'
        for result in response.css(SET_SELECTOR):
            obj = {
                'source_id'         :result.xpath('@id').extract_first(),
                'name'              :result.xpath('.//*[@itemprop="name"]/text()').extract_first(),
                'telephone'         :result.xpath('.//*[@itemprop="telephone"]/text()').extract_first(),
                'detail_url'        :result.xpath('.//a[@class="business-name"]/@href').extract_first(),
                'images'            :result.xpath('.//*[@itemprop="image"]/@src').extract(),
                'categories'        :result.xpath('.//div[@class="categories"]//text()').extract_first(),
                'website'           :result.xpath('.//a[@class="track-visit-website"]/@href').extract_first() ,
                'address_street'    :result.xpath('.//*[@itemprop="streetAddress"]/text()').extract_first(),
                'address_locality'  :result.xpath('.//*[@itemprop="addressLocality"]/text()').extract_first(),
                'postal_code'       :result.xpath('.//*[@itemprop="postalCode"]/text()').extract_first(),
            }

            yield self.regular_data(obj)

