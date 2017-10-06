# usar o link https://api.gpa.digital/pa/products/list/secoes/C4233/limpeza?storeId=501&qt=36&s=&ftr=null&p=3&rm=&gt=list

#limpeza?storeId=501&qt=36&s=&ftr=null&p=&rm=&gt=list
#adicionar numero da página antes do &rm

#fazer join &rm=&gt=list

import requests
import urllib.request
from dicttoxml import dicttoxml
from bs4 import BeautifulSoup
import xml.etree.cElementTree as ET
import time
import os
import random


xml_path = 'paodeacucar' + '_' + time.strftime("%d-%m-%Y") + '.xml'


def get_content(url):
    req = requests.get(url)
    if(req.status_code == 200):
        result = req.json()
        xml = dicttoxml(result,custom_root='test', attr_type=False)
        return xml
    else:
        raise ConnectionError


def download_image(url):
    parse = url.split('uploads/', 1)
    parse = parse[1].split('/', 1)
    parse = parse[1].split('/', 1)
    image_name = parse[1]
    caminho = os.getcwd() + "/images/" + image_name

    image = urllib.request.urlretrieve(url, caminho)


def extract_product_name(string):
    parse1 = string.split('/produto/', 1)
    parse2 = parse1[1].split('/', 1)
    parse3 = parse2[1].split('<',1)

    result = parse3[0].replace('-', ' ')
    return result.upper()


def extract_product_price(string):
    parse1 = string.split('>', 1)
    parse2 = parse1[1].split('<', 1)

    result = parse2[0]
    return result


def extract_product_image_link(string):
    parse1 = string.split('big>', 1)
    parse2 = parse1[1].split('<', 1)

    result = 'https://www.paodeacucar.com' + parse2[0]
    return result


def write_xml(row):
    if os.path.exists(xml_path):
        tree = ET.parse(xml_path)
        xml_root = tree.getroot()
    else:
        xml_root = ET.Element("produtos")

    product = ET.SubElement(xml_root, "produto")
    ET.SubElement(product, "imagem").text = row[0]
    ET.SubElement(product, "nome").text = row[1]
    ET.SubElement(product, "preco").text = row[2]

    tree = ET.ElementTree(xml_root)
    tree.write(xml_path)


# ------- Scraping --------

file_dir = os.getcwd() + '/category_urls'
category_urls = open(file_dir, 'r')
category_done = False

products = []

for category in category_urls:
    page_count = 0
    category_done = False

    while not category_done:
        delay = random.randrange(7)

        if(page_count > 0):
            url = category + str(page_count) + '&rm=&gt=list'
        else:
            url = category + '&rm=&gt=list'

        time.sleep(delay)
        page = get_content(url)
        soup = BeautifulSoup(page, 'lxml')

        names_unc = soup.findAll('urldetails')
        prices_unc = soup.findAll('sellprice')
        image_link_unc = soup.findAll('n0')

        if(len(names_unc) > 0 and len(prices_unc) > 0 and len(image_link_unc) > 0):
            print('---------------' + 'Pagina: ' + str(page_count) + '---------------')
            products_unc = zip(names_unc, prices_unc, image_link_unc)

            for name, price, image_l in products_unc:
                product_name = extract_product_name(str(name))
                product_price = extract_product_price(str(price))
                image_link = extract_product_image_link(str(image_l))
                try:
                    download_image(image_link)
                except Exception as e:
                    pass
                    
                print(product_name)
                row = [image_link, product_name, product_price]
                write_xml(row)
            page_count += 1
        else:
            time.sleep(15)
            category_done = True

category_urls.close()
