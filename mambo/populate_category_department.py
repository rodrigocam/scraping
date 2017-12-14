import pymysql.cursors
from scraper import CATEGORY_DICT, DEPARTMENT_DICT


connection = pymysql.connect(host='187.45.188.134',
			                 user='mesa_edmilson',
			                 password='s31TKx',	
			                 db='mesa_supermercado',
			                 charset='utf8mb4',
			                 cursorclass=pymysql.cursors.DictCursor)

for key in CATEGORY_DICT:
    sql = "INSERT INTO `familia` (`id_familia`, `nome`, `ativo`) VALUES (%s %s %s)"

    print(CATEGORY_DICT[key])
    print(key)
    with connection.cursor() as cursor:
        cursor.execute(sql, (CATEGORY_DICT[key], key, 1))
        connection.commit()