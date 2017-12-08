import pymysql.cursors
import xml.etree.ElementTree as ET

def extract_medium_price(string):
        parser = string.split("De ", 1)
        parser2 = parser[1].split(" a ", 2)

	first_price = list(parser2[0])
	f_index = first_price.index(',')
	first_price[f_index] = '.'

	second_price = list(parser2[1])
	s_index = second_price.index(',')
	second_price[s_index] = '.'
	
	n1 = "".join(first_price)
	n2 = "".join(second_price)

        result = (float(n1)+float(n2))/2
	return result



tree = ET.parse('products.xml')
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
		sql = "INSERT INTO `produto` (`id_grupo`,`id_familia`,`id_unidade_medida_venda`,`gtin`,`nome`,`ativo`,`disponivel`, `preco`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
		cursor.execute(sql, (1, 1,'UN', barcode, name, 1, 1, medium_price))
		connection.commit()
