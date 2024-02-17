# -*- coding: utf-8 -*-
import scrapy


class GetdataSpider(scrapy.Spider):
    name = 'getdata'
    allowed_domains = ['bionetz.ch']
    
    # An dieser Stelle definieren wir unsere Zieldomains
    start_urls = ['https://bionetz.ch/adressen/detailhandel/bio-fachgeschaefte.html',
    'https://bionetz.ch/adressen/detailhandel/bio-fachgeschaefte/page2.html',
    'https://bionetz.ch/adressen/detailhandel/bio-fachgeschaefte/page3.html',
    'https://bionetz.ch/adressen/detailhandel/bio-fachgeschaefte/page4.html',
    'https://bionetz.ch/adressen/detailhandel/bio-fachgeschaefte/page5.html']

    def parse(self, response):

    	# An dieser Stelle benoetigen wir die xPath von den Elementen, die wir aus der Webseite extrahieren wollen 
    	# Dazu muessen wir uns erst einmal klar machen, wie genau die Webseitenstruktur aufgebaut ist. Hierfuer nutzen wir den Google Chrome Inspector (Rechte Maustase -> Inspect)
    	# Sobald wir die Webseitenstruktur kennen, nutzen wir den xPath-Helper, um den xPath- des Elements zu identifizieren, welches wir extrahieren wollen 
    	single_etikette = response.xpath('//*[@class="listing-summary col-xs-12 col-sm-6"]')

    	# Wir haben durch die Webseitenstruktur gesehen, dass die Klasse "listing-summary col-xs-12 col-sm-6" unsere Informationen enthaelt. Daher bauen wir nun eine Schleife, die diese Elemente extrahiert

    	for etikette in single_etikette: 
    		unternehmens_name = etikette.xpath('.//*[@itemprop="name"]/text()').extract()
    		unternehmens_adresse = etikette.xpath('.//*[@class="address"]/text()').extract_first()

    		# Der Output ist an dieser Stelle noch sehr "noisy". Wir koennen entweder jetzt schon die Daten "sauberer ziehen" in dem wir mit Regex-Opertoren arbeiten. 
    		# Alternativ koennen wir die Daten aber auch spaeter noch sauebern 

    		unternehmens_plz = etikette.xpath('.//*[@class="address"]/text()').re('[^,]*$')

    		# Da wird die Ergebnisse ausgeben lassen wollen, definieren wir ein Dictionary und entfernen die pass-Funktion 
    		yield {'Name': unternehmens_name,
    				'Adresse': unternehmens_adresse,
    				'Postleitzahl' : unternehmens_plz}