from lxml import etree
import xtdiff
import pymysql.cursors
import xml.etree.ElementTree as ET
import os
import scraper

file_base_path = '/home/scraping/diff/last_day.xml'
file_compare_path = '/home/scraping/diff/current_day.xml'
updated_xml_path = '/home/scraping/diff/updated.xml'


scraper.scrap()

file_base = open(file_base_path, 'r')
file_compare = open(file_compare_path, 'r')

xml__base = etree.XML(file_base.read())
xml_compare = etree.XML(file_compare.read())
 
diff = xtdiff.diff(xml__base, xml_compare)
new_xml = xtdiff.transform(xml__base, diff)
updated_xml = open(updated_xml_path, 'wb')
updated_xml.write(etree.tostring(new_xml))

tree = ET.parse('updated.xml')
root = tree.getroot()

connection = pymysql.connect(host='187.45.188.134',
			                 user='mesa_edmilson',
			                 password='s31TKx',	
			                 db='mesa_supermercado',
			                 charset='utf8mb4',
			                 cursorclass=pymysql.cursors.DictCursor)

for product in root.findall('produto'):
    name = product.find('nome').text
    price = product.find('preco').text
	
    with connection.cursor() as cursor:
        sql = "SELECT preco FROM `produto` WHERE `nome` = %s"
        cursor.execute(sql, name)
        a = cursor.fetchall()
        
        if len(a) == 0:
            sql = "INSERT INTO `produto` (`id_grupo`,`id_familia`,`id_unidade_medida_venda`,`gtin`,`nome`,`ativo`,`disponivel`, `preco`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (1, 1, 'UN', None, name, 1, 1, price))
        else:
            sql = "UPDATE `produto` SET `preco` = %s WHERE `nome` = %s"
            cursor.execute(sql, (price, name))

        connection.commit()

os.remove('last_day.xml')
os.rename('current_day.xml', 'last_day.xml')