#!/usr/bin/env python
import urllib2
import xml.etree.cElementTree as ET
from bs4 import BeautifulSoup
import re

base_url = 'http://www.deliveryextra.com.br'

category_urls = ['http://www.deliveryextra.com.br/secoes/C2475/bebes',
                 'http://www.deliveryextra.com.br/secoes/C127/perfumaria',
                 'http://www.deliveryextra.com.br/secoes/C145/limpeza',
                 'http://www.deliveryextra.com.br/secoes/C312/alimentos',
                 'http://www.deliveryextra.com.br/secoes/C76/bebidas',
                 'http://www.deliveryextra.com.br/secoes/C975/carnes',
                 'http://www.deliveryextra.com.br/secoes/C12/feira',
                 'http://www.deliveryextra.com.br/secoes/C189/pet']

products_urls = []

xml_path = 'products.xml'

def get_page_content(url):
	try:
		req = urllib2.Request(url.encode('utf-8'))
		page = urllib2.urlopen(req)
		result = page.read()
		return result
	except Exception as e:
		print "ERROR: Internet access error!"
		print e

# def make_xml(row):
# 	if os.path.exists(xml_path):
# 		tree = ET.parse(xml_path)
# 		xml_root = tree.getroot()
# 	else:
# 		xml_root = ET.Element("produtos")
#
# 	product = ET.SubElement(xml_root, "produto")
#     ET.SubElement(product, "imagem").text = row[0]
#     ET.SubElement(product, "categoria").text = row[1]
#     ET.SubElement(product, "nome").text = row[3]
#     ET.SubElement(product, "preco").text = row[4]

def extract_product_link(content):
    parser = content.split('href="', 1)
    parser = parser[1].split('">', 1)
    products_urls.append(parser[0])

def extract_image_link(content):
    parser = content.split('src="', 1)
    parser = parser[1].split('" width', 1)
    return base_url+str(parser[0])

def extract_product_name(content):
    parser = content.split('title="', 1)
    parser = parser[1].split('">', 1)
    return str(parser[0])


soup = BeautifulSoup(get_page_content(category_urls[0]))
lines = soup.findAll('a', class_='showcase-item__thumb')
# for line in lines:
#     print line
for line in lines:
    extract_product_link(str(line))

print products_urls
#line = soup.find('span', class_='value')
#print (line)
# -- Scraping
 # for url in category_urls:
 #     counter = 0
 #     done = False
 #     soup = BeautifulSoup(get_page_content(url)
 #     while(not done and soup):
 #         counter+=1
 #
 #         content_line = soup.find('img', {'class':'prdImagem'})
 #         image_link = extract_image_link(content_line)
 #
 #         content_line = soup.find('div', class_='showcase-item__info')
 #         product_name = extract_product_name(str(content_line))
