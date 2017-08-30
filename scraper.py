#!/usr/bin/env python
import time
import mechanize
import random
import urllib
import os.path
import xml.etree.cElementTree as ET
from bs4 import BeautifulSoup
import re

base_url = 'http://www.deliveryextra.com.br'
login_url = 'https://chk.deliveryextra.com.br/login/login?_ga=2.205476560.1512607359.1503675600-1872537457.1502920969'

category_urls =  {'higiene':'http://www.deliveryextra.com.br/secoes/C2475/bebes',
                 'higiene2':'http://www.deliveryextra.com.br/secoes/C127/perfumaria',
                 'higiene3':'http://www.deliveryextra.com.br/secoes/C145/limpeza',
                 'despensa':'http://www.deliveryextra.com.br/secoes/C312/alimentos',
                 'bebidas':'http://www.deliveryextra.com.br/secoes/C76/bebidas',
                 'carnes':'http://www.deliveryextra.com.br/secoes/C975/carnes',
                 'hortifruti':'http://www.deliveryextra.com.br/secoes/C12/feira',
                 'Pet':'http://www.deliveryextra.com.br/secoes/C189/pet'}

products_urls = []

xml_path = 'products.xml'

def login():
        try:
                browser = mechanize.Browser()
                browser.open(login_url)
                browser.select_form(name="loginBox")
                browser["userLogin"] = "squiz.shama@gmail.com"
                browser["password"] = "rodrigo1997"
                browser.submit()
                return browser
        except Exception as e:
                print "ERROR: Internet access error!"
                print e

def write_xml(row):
	if os.path.exists(xml_path):
		tree = ET.parse(xml_path)
		xml_root = tree.getroot()
	else:
		xml_root = ET.Element("produtos")

	product = ET.SubElement(xml_root, "produto")
        ET.SubElement(product, "nome").text = row[0]
        ET.SubElement(product, "categoria").text = row[1]
        ET.SubElement(product, "imagem").text = row[2]
        ET.SubElement(product, "preco").text = row[3]

	tree = ET.ElementTree(xml_root)
	tree.write(xml_path)

def download_image(url, image_name):
    caminho = os.getcwd() + "/images/" + image_name
    image = urllib.urlretrieve(url, caminho)

def extract_product_link(content):
    parser = content.split('href="', 1)
    parser = parser[1].split('">', 1)
    products_urls.append(parser[0])

def extract_image_link(content):
    parser = content.split('src="', 1)
    parser = parser[1].split('" width', 1)
    return base_url+str(parser[0])

def extract_product_name(content):
    parser = content.split('"produto-nome":"', 1)
    parser = parser[1].split('","produto-sku"', 1)
    return str(parser[0])

def extract_product_price(content):
    try:
        parser = content.split('"produto-preco":"', 1)
        parser = parser[1].split('","itens-c', 1)
        return str(parser[0])
    except Exception as e:
        print e
        return None

# -- Scraping
browser = login()

for category, url in category_urls.items():
    counter = 0
    done = False
    page_url = url
    print 'Scraping category: ' + category
    while(not done):
        products_urls = []
        soup = BeautifulSoup(browser.open(page_url))
        lines = soup.findAll('a', class_='showcase-item__thumb')
        for line in lines:
            extract_product_link(str(line))

        if products_urls is None:
            done = True

        for url in products_urls:
            print url
            delay = random.randrange(25)
            if delay < 10:
                delay = 28
            time.sleep(delay)
            soup = BeautifulSoup(browser.open(url))
            find_result = soup.find('script')
            product_price = extract_product_price(str(find_result))

            if product_price is None:
                pass
            else:
                find_result = soup.find('script')
                product_name = extract_product_name(str(find_result))
                print product_name

                find_result = soup.find('img', {'class':'product-image__main-img'})
                image_link = extract_image_link(str(find_result))
                print image_link

                print 'writing xml'
                row = [product_name, category, image_link, product_price]
                write_xml(row)

        counter+=1
        page_url = page_url+'?&p='+ str(counter) + '&ftr='
