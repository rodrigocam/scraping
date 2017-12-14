import pymysql.cursors
from scraper import CATEGORY_DICT, DEPARTMENT_DICT


connection = pymysql.connect(host='177.234.146.66',
			                 user='mesa_edmilson',
			                 password='s31TKx',	
			                 db='mesa_supermercado',
			                 charset='utf8mb4',
			                 cursorclass=pymysql.cursors.DictCursor)

for key in DEPARTMENT_DICT:
    sql = "INSERT INTO `grupo` (`id_grupo`, `id_familia`, `nome`, `ativo`) VALUES (%s, %s, %s, %s)"

    print(DEPARTMENT_DICT[key])
    if DEPARTMENT_DICT[key] >= 2 and DEPARTMENT_DICT[key] < 11:
        family_id = 2
    elif DEPARTMENT_DICT[key] >= 11 and DEPARTMENT_DICT[key] < 17:
        family_id = 3
    elif DEPARTMENT_DICT[key] >= 17 and DEPARTMENT_DICT[key] < 21:
        family_id = 4
    elif DEPARTMENT_DICT[key] >= 21 and DEPARTMENT_DICT[key] < 25:
        family_id = 5
    elif DEPARTMENT_DICT[key] >= 25 and DEPARTMENT_DICT[key] < 30:
        family_id = 6
    elif DEPARTMENT_DICT[key] >= 30 and DEPARTMENT_DICT[key] < 33:
        family_id = 7
    elif DEPARTMENT_DICT[key] >= 33 and DEPARTMENT_DICT[key] < 40:
        family_id = 8
    elif DEPARTMENT_DICT[key] >= 40 and DEPARTMENT_DICT[key] < 47:
        family_id = 9
    elif DEPARTMENT_DICT[key] >= 47 and DEPARTMENT_DICT[key] < 56:
        family_id = 10
    elif DEPARTMENT_DICT[key] >= 56 and DEPARTMENT_DICT[key] < 61:
        family_id = 11
    elif DEPARTMENT_DICT[key] >= 61 and DEPARTMENT_DICT[key] < 67:
        family_id = 12
    elif DEPARTMENT_DICT[key] >= 67 and DEPARTMENT_DICT[key] < 70:
        family_id = 13
    elif DEPARTMENT_DICT[key] >= 70 and DEPARTMENT_DICT[key] < 80:
        family_id = 14

    with connection.cursor() as cursor:
        cursor.execute(sql, (DEPARTMENT_DICT[key], family_id, key, 1))
        connection.commit()