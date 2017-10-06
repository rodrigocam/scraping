import requests
from dicttoxml import dicttoxml
from bs4 import BeautifulSoup
import xml.etree.cElementTree as ET
import time
import os

request_delay = 10
url_increment = 20
undesired_categories = ['Cama, mesa e banho', 'Automotivos', 'Utensílios domésticos',
                        'Telefonia', 'Eletrodomésticos', 'Eletrônicos']
base_url = 'https://carrefourwebview.arizona.global/webview/location/BAN/format/hiper/offers/destaque/destaque/order/priceASC/'
xml_path = 'carrefour' + '_' + time.strftime("%d-%m-%Y") + '.xml'

def get_content(url):
    req = requests.get(url, verify=False)
    result = req.json()
    xml = dicttoxml(result,custom_root='test', attr_type=False)
    return xml

def download_image(url):
    parse = url.split('homolog/', 1)
    image_name = parse[1]
    caminho = os.getcwd() + "/images/" + image_name

    image = urllib.request.urlretrieve(url, caminho)

def generate_xml(row):
    if os.path.exists(xml_path):
        tree = ET.parse(xml_path)
        xml_root = tree.getroot()
    else:
        xml_root = ET.Element("produtos")

    product = ET.SubElement(xml_root, "produto")
    ET.SubElement(product, "imagem").text = row[0]
    ET.SubElement(product, "categoria").text = row[1]
    ET.SubElement(product, "nome").text = row[2]
    ET.SubElement(product, "preco").text = row[3]

    tree = ET.ElementTree(xml_root)
    tree.write(xml_path)

def extract_product_name(string):
    aux = string.split('short_description>', 1)
    aux = aux[1].split('</', 1)
    aux2 = string.split('large_description>', 1)
    aux2 = aux2[1].split('</', 1)
    result = str(aux[0] + ' ' + aux2[0])
    return result

def extract_product_price(string):
    aux = string.split('<price>', 1)
    aux = aux[1].split('</', 1)
    return aux[0]

def extract_product_category(string):
    aux = string.split('<category>', 1)
    aux = aux[1].split('</', 1)
    return aux[0]

def extract_product_image_link(string):
    aux = string.split('<image>', 1)
    aux = aux[1].split('</', 1)
    return aux[0]

count = 0
product_count = 0
while (count < 380):
    if(count == 0):
        url = base_url
    else:
        url = str(base_url + 'offset/' + str(count) + '/')

    content = get_content(url)
    soup = BeautifulSoup(content, "lxml")
    lines = soup.findAll('item')

    for line in lines:
        try:
            category = extract_product_category(str(line))
            if category in undesired_categories:
                pass
            else:
                name = extract_product_name(str(line))
                print('Scraping ' + name)
                price = extract_product_price(str(line))
                image_link = extract_product_image_link(str(line))
                download_image(image_link)

                row = [image_link, category, name, price]
                generate_xml(row)

                product_count+=1
                print(product_count)
        except Exception as e:
            pass

    count += url_increment
    time.sleep(request_delay)
