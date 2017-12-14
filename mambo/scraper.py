import urllib.request
import xml.etree.cElementTree as ET
from bs4 import BeautifulSoup
import requests
import os


CATEGORY_DICT = {'Mercearia': 1,
                 'Hortifrúti': 2,
                 'Carnes e Aves': 3,
                 'Frios e Laticínios': 4,
                 'Pescados': 5,
                 'Padaria': 6,
                 'Congelados': 7,
                 'Bebidas': 8,
                 'Utensílios Domésticos': 9,
                 'Limpeza': 10,
                 'Higiene e Beleza': 11,
                 'Petshop': 12,
                 'Suplementos': 13}

DEPARTMENT_DICT = {'Alimentos Básicos': 1,
                   'Doces & Sobremesas': 2,
                   'Biscoitos & Salgadinhos': 3,
                   'Bomboniete': 4,
                   'Massas & Molhos': 5,
                   'Temperos & Condimentos': 6,
                   'Conservas & Enlatados': 7,
                   'Grãos & Farináceos': 8,
                   'Matinais': 9,
                   'Verduras': 10,
                   'Frutas': 11,
                   'Legumes': 12,
                   'Temperos Frescos': 13,
                   'Ovos': 14,
                   'Pronto para Consumo': 14,
                   'Bovinas': 15,
                   'Suínas': 16,
                   'Aves': 17,
                   'Exóticas e Especiais': 18,
                   'Pescados': 19,
                   'Lácteos': 20,
                   'Queijos': 21,
                   'Frios & Embutidos': 22,
                   'Fondue': 23,
                   'Bacalhau': 24,
                   'Camarão': 25,
                   'Salmão': 26,
                   'Saint Peter': 27,
                   'Crustáceos': 28,
                   'Pães e Torradas': 29,
                   'Bolos': 30,
                   'Doces': 31,
                   'Sucos e Sobremesas': 32,
                   'Petiscos e Empanados': 33,
                   'Pratos Prontos': 34,
                   'Hambúrger': 35,
                   'Legumes Congelados': 36,
                   'Frutas Congeladas': 37,
                   'Pães': 38,
                   'Água, Enegéticos e Chás': 39,
                   'Sucos, Refrescos e Refrigerantes': 40,
                   'Cervejas': 41,
                   'Destilados': 42,
                   'Whisky': 43,
                   'Vinhos & Espumantes': 44,
                   'Acessórios': 45,
                   'Conveniências': 46,
                   'Embalagens': 47,
                   'Descartáveis': 48,
                   'Bar': 49,
                   'Cozinha': 50,
                   'Casa': 51,
                   'Artigos para Academia': 52,
                   'Limpeza e Organização': 53,
                   'Artigos Decorativos': 54,
                   'Casa Geral': 55,
                   'Roupas': 56,
                   'Cozinha': 57,
                   'Banheiro': 58,
                   'Calçados': 59,
                   'Higiene': 60,
                   'Corpo': 61,
                   'Cabelos': 62,
                   'Mãos e Pés': 63,
                   'Bebê': 64,
                   'Maquiagem': 65,
                   'Cães': 66,
                   'Gatos': 67,
                   'Aves': 68,
                   'Proteínas': 69,
                   'Energéticos': 70,
                   'Aminoácidos': 71,
                   'Hipercalóricos': 72,
                   'Pré-Treinos': 73,
                   'Vitaminas': 74,
                   'Emagrecedores': 75,
                   'Pós-treinos': 76,
                   'Nutricosméticos': 77}

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
    result = raw_data.partition(' - ')

    category = result[0].split('<title>')[1]
    department = result[2].partition(' - ')[0]

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

    for url in urls:
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

            print(category)
            print(department)
            for raw_url in div_list:
                product_url = get_product_url(str(raw_url))

                print(product_url)
                page = get_content(product_url)
                soup = BeautifulSoup(page, 'lxml')
                try:
                    price = get_attrib(str(soup.findAll('meta', {'property':'product:price:amount'})[0]))
                    product_name = get_attrib(str(soup.findAll('meta', {'name':'description'})[0]))
                    gtin_code = get_attrib(str(soup.findAll('meta', {'itemprop':'gtin13'})[0]))
                    image_link = get_attrib(str(soup.findAll('meta', {'property':'og:image'})[0]))
                    row = [product_name, gtin_code, price, str(category), str(department), image_link]

                    download_image(image_link, gtin_code + '.jpg')
                    write_xml(row)

                except IndexError:
                    print('Prduto indisponível - ' + product_url)


if __name__ == '__main__':
    scrape()