import pymysql.cursors

connection = pymysql.connect(host='187.45.188.134',
			                 user='mesa_edmilson',
			                 password='s31TKx',	
			                 db='mesa_supermercado',
			                 charset='utf8mb4',
			                 cursorclass=pymysql.cursors.DictCursor)

with connection.cursor() as cursor:
    sql = "SELECT preco FROM `produto` WHERE nome = %s"
    cursor.execute(sql, '')
    a = cursor.fetchall()
    connection.commit()

print(len(a))
