import scrapy
import csv
import re
from datetime import timedelta, date
import sys

class GetArticlesSpider(scrapy.Spider):
	name = 'elperiodicoarticles'

	def start_requests(self):
		urls = []
		a=10000
		b=100000
		for i in range(a,b):
			url = "https://www.elperiodico.com/es/a/20081129/b-{0}".format(str(i))
			yield scrapy.Request(url=url, callback=self.parse, meta={'ID':str(i)})

	def parse(self,response):
		ID = response.meta['ID']
		
		section = response.css('div.article-seccio::text').extract_first()

		title = response.css('h1.title::text').extract_first()

		subtitle = response.css('div.subtitle')
		subtitle = subtitle.css('h2::text').extract_first()

		mainarticle = response.css('div.ep-detail-body').css('p::text').extract()
		mainarticle = ' '.join(mainarticle)

		location_date_info = response.css('time.date').css('span::text').extract()
		location_date_info = ','.join([i.strip() for i in location_date_info])

		category = response.css('p.epigraph').css('span::text').extract_first()

		datetime = response.css('meta[name=date]::attr(content)').extract_first()

		mydict = {  'id' : ID,
					'url' : response.request.url,
					'datetime' : datetime,
					'title' : title,
					'subtitle' : subtitle,
					'category' : category,
					'author' : response.css('span.author-link::text').extract_first(),
					'mainarticle' : mainarticle,
					'location_date_info' : location_date_info
					}

		for key in mydict:
			try:
				for char in ["\n","\t",";"]:
					mydict[key] = mydict[key].replace(char," ")
				mydict[key] = ' '.join(mydict[key].split())
			except:
				pass

		yield mydict
