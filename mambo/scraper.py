import urllib.request
import xml.etree.cElementTree as ET
from bs4 import BeautifulSoup
import requests
import os
import random
import time


CATEGORY_DICT = {'Mercearia': 2,
                 'Hortifrúti': 3,
                 'Carnes, Aves e Peixes': 4,
                 'Frios e Laticínios': 5,
                 'Pescados': 6,
                 'Padaria': 7,
                 'Congelados': 8,
                 'Bebidas': 9,
                 'Utensílios Domésticos': 10,
                 'Limpeza': 11,
                 'Higiene e Beleza': 12,
                 'Petshop': 13,
                 'Suplementos': 14}

DEPARTMENT_DICT = {'Alimentos Básicos': 2,
                   'Doces & Sobremesas': 3,
                   'Biscoitos & Salgadinhos': 4,
                   'Bomboniere': 5,
                   'Massas & Molhos': 6,
                   'Temperos & Condimentos': 7,
                   'Conservas & Enlatados': 8,
                   'Grãos & Farináceos': 9,
                   'Matinais': 10,
                   'Verduras': 11,
                   'Frutas': 12,
                   'Legumes': 13,
                   'Temperos Frescos': 14,
                   'Ovos': 15,
                   'Pronto para Consumo': 16,
                   'Bovinas': 17,
                   'Suínas': 18,
                   'Aves': 19,
                   'Exóticas e Especiais': 20,
                   'Pescados': 21,
                   'Lácteos': 22,
                   'Queijos': 23,
                   'Frios & Embutidos': 24,
                   'Fondue': 25,
                   'Bacalhau': 26,
                   'Camarão': 27,
                   'Salmão': 28,
                   'Saint Peter': 29,
                   'Crustáceos': 30,
                   'Pães e Torradas': 31,
                   'Bolos': 32,
                   'Doces': 33,
                   'Sucos e Sobremesas': 34,
                   'Petiscos e Empanados': 35,
                   'Pratos Prontos': 36,
                   'Hambúrger': 37,
                   'Legumes Congelados': 38,
                   'Frutas Congeladas': 39,
                   'Pães': 40,
                   'Água, Enegéticos e Chás': 41,
                   'Sucos, Refrescos e Refrigerantes': 42,
                   'Cervejas': 43,
                   'Destilados': 44,
                   'Whisky': 45,
                   'Vinhos & Espumantes': 46,
                   'Acessórios': 47,
                   'Conveniências': 48,
                   'Embalagens': 49,
                   'Descartáveis': 50,
                   'Bar': 51,
                   'Cozinha': 52,
                   'Casa': 53,
                   'Artigos para Academia': 54,
                   'Limpeza e Organização': 55,
                   'Artigos Decorativos': 56,
                   'Casa Geral': 57,
                   'Roupas': 58,
                   'Cozinha': 59,
                   'Banheiro': 60,
                   'Calçados': 61,
                   'Higiene': 62,
                   'Corpo': 63,
                   'Cabelos': 64,
                   'Mãos e Pés': 65,
                   'Bebê': 66,
                   'Maquiagem': 67,
                   'Cães': 68,
                   'Gatos': 69,
                   'Aves': 70,
                   'Proteínas': 71,
                   'Energéticos': 72,
                   'Aminoácidos': 73,
                   'Hipercalóricos': 74,
                   'Pré-Treinos': 75,
                   'Vitaminas': 76,
                   'Emagrecedores': 77,
                   'Pós-treinos': 78,
                   'Nutricosméticos': 79}

XML_PATH = 'current_day.xml'

HEADERS = {'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'}

def get_content(url):
    req = requests.get(url, headers=HEADERS)
    if(req.status_code == 200):
        return req.text
    else:
        raise ConnectionError(req.status_code)


def download_image(url, image_name):
    caminho = os.getcwd() + "/images/" + image_name
    if not os.path.isfile(caminho):
        image = urllib.request.urlretrieve(url, caminho)


def write_xml(row):
    if os.path.exists(XML_PATH):
        tree = ET.parse(XML_PATH)
        xml_root = tree.getroot()
    else:
        xml_root = ET.Element("produtos")

    product = ET.SubElement(xml_root, "produto")
    ET.SubElement(product, "nome").text = row[0]
    ET.SubElement(product, "gtin").text = row[1]
    ET.SubElement(product, "preco").text = row[2]
    ET.SubElement(product, "categoria").text = row[3]
    ET.SubElement(product, "departamento").text = row[4]
    ET.SubElement(product, "imagem").text = row[5]

    tree = ET.ElementTree(xml_root)
    tree.write(XML_PATH)


def get_attrib(raw_data):
    result = raw_data.split('content="')
    result = result[1].split('"')[0]
    return result


def get_category_department(raw_data):
    raw_data = raw_data.replace('–', '-')
    result = raw_data.partition(' - ')

    category = result[0].split('<title>')[1]
    department = result[2].partition(' - ')[0].split(' ')[0]
    if department != 'Ovos' and department != 'Suínas':
        department = result[2].partition(' - ')[0]

    print(category)
    print(department)

    if '&amp;' in department:
        tmp = department.partition('&amp;')
        department = tmp[0] + '& ' + tmp[2].split(' ')[1]

    return (CATEGORY_DICT[category], DEPARTMENT_DICT[department])


def get_product_url(raw_data):
    result = raw_data.split('data-url="')[1]
    result = result.split(' ')[1]
    return result.split('"')[0]


def get_brand_url(raw_data):
    result = raw_data.split('href="')
    return result[1].split('"')[0]


def scrape():
    urls = open('category_urls', 'r')
    delay = 120

    for url in urls:
        while True:
            try:
                url = url.split('\n')[0]
                print(url)
                page = get_content(url)
                soup = BeautifulSoup(page, 'lxml')
                
                tmp = str(soup.findAll('ul', {'class': 'Marca'})[0])
                tmp_soup = BeautifulSoup(tmp, 'lxml')
                raw_data_list = tmp_soup.find_all('a')
                
                for a in raw_data_list:
                    brand_url = get_brand_url(str(a))

                    page = get_content(brand_url)
                    soup = BeautifulSoup(page, 'lxml')

                    category, department = get_category_department(str(soup.findAll('title')[0]))
                    div_list = soup.findAll('div', {'data-isinstock': True})

                    for raw_url in div_list:
                        product_url = get_product_url(str(raw_url))

                        print(product_url)
                        page = get_content(product_url)
                        soup = BeautifulSoup(page, 'lxml')

                        price = get_attrib(str(soup.findAll('meta', {'property':'product:price:amount'})[0]))
                        product_name = get_attrib(str(soup.findAll('meta', {'name':'description'})[0]))
                        gtin_code = get_attrib(str(soup.findAll('meta', {'itemprop':'gtin13'})[0]))
                        image_link = get_attrib(str(soup.findAll('meta', {'property':'og:image'})[0]))
                        row = [product_name, gtin_code, price, str(category), str(department), image_link]

                        download_image(image_link, gtin_code + '.jpg')
                        write_xml(row)
                break
            except ConnectionError:
                print('\n---- CONNECTION ERROR ----\n')
                time.sleep(delay)
                continue
            except IndexError:
                print('Prduto indisponível - ' + product_url)
                break


if __name__ == '__main__':
    scrape()