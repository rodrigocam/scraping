from lxml import etree
import xtdiff
import pymysql.cursors
import xml.etree.ElementTree as ET
import os
import scraper


scraper.scrape()

tree = ET.parse('current_day.xml')
root = tree.getroot()

connection = pymysql.connect(host='177.234.146.66',
			                 user='mesa_edmilson',
			                 password='s31TKx',	
			                 db='mesa_supermercado',
			                 charset='utf8mb4',
			                 cursorclass=pymysql.cursors.DictCursor)

for product in root.findall('produto'):
    name = product.find('nome').text
    price = product.find('preco').text
    barcode = product.find('gtin').text
    category = product.find('categoria').text
    department = product.find('departamento').text
    if name:
        with connection.cursor() as cursor:
            sql = "SET FOREIGN_KEY_CHECKS=0"
            cursor.execute(sql)

            sql = "SELECT `preco` FROM `produto` WHERE `gtin` = %s"
            cursor.execute(sql, barcode)
            result = cursor.fetchall()

            if result:
                result = '%.2f' % float(result[0]['preco'])
                print('DATABASE PRICE %s --- XML PRICE %s' % (result, price))
                if result != price:
                    sql = "UPDATE `produto` SET `preco` = %s WHERE `gtin` = %s"
                    cursor.execute(sql, (price, barcode))
                    print('\n ---- PRODUCT UPDATED ----\n')
                    print('\n OLD PRICE : %s ---- NEW PRICE : %s\n' % (result, price))
                    connection.commit()
            else:
                sql = "INSERT INTO `produto` (`id_grupo`,`id_familia`,`id_unidade_medida_venda`,`gtin`,`nome`,`ativo`,`disponivel`, `preco`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (department, category, 'UN', barcode, name, 1, 1, price))
                print('\n ---- PRODUCT INSERTED ----\n')
                connection.commit()

print('\n ---- FINISHED ROUTINE ----')
if os.path.isfile('last_day.xml'):
    os.remove('last_day.xml')
os.rename('current_day.xml', 'last_day.xml')