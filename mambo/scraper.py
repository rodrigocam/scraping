import requests
from bs4 import BeautifulSoup


CATEGORY_DICT = {'Mercearia': 1}
DEPARTMENT_DICT = {'Alimentos Básicos': 1}


def get_content(url):
    req = requests.get(url)
    if(req.status_code == 200):
        return req.text
    else:
        raise ConnectionError


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


def test():
    page = get_content('https://www.mambo.com.br/mercearia/alimentos-basicos/arroz')
    soup = BeautifulSoup(page, 'lxml')
    
    tmp = str(soup.findAll('ul', {'class': 'Marca'})[0])
    tmp_soup = BeautifulSoup(tmp, 'lxml')
    raw_data_list = tmp_soup.find_all('a')
    
    for a in raw_data_list:
        count = 1
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
            try:
                price = get_attrib(str(soup.findAll('meta', {'property':'product:price:amount'})[0]))
                product_name = get_attrib(str(soup.findAll('meta', {'name':'description'})[0]))
                gtin_code = get_attrib(str(soup.findAll('meta', {'itemprop':'gtin13'})[0]))
                image_link = get_attrib(str(soup.findAll('meta', {'property':'og:image'})[0]))
                print(product_name)
                count += 1
            except IndexError:
                print('Prduto indisponível - ' + product_url)

        
def scrape():
    urls = open('category_urls', 'r')
    
    category_number = 1
    department_number = 1

    for url in urls:
        page = get_content(url)
        soup = BeautifulSoup(page, 'lxml')

        product_name = get_attrib(str(soup.findAll('meta', {'name':'description'})[0]))
        gtin_code = get_attrib(str(soup.findAll('meta', {'itemprop':'gtin13'})[0]))
        price = get_attrib(str(soup.findAll('meta', {'property':'product:price:amount'})[0]))
        image_link = get_attrib(str(soup.findAll('meta', {'property':'og:image'})[0]))

        

if __name__ == '__main__':
    #page = get_content('https://www.mambo.com.br/arroz-polido-longo-e-fino-t1-blue-ville-pacote-5kg/p')
    # soup = BeautifulSoup(page, 'lxml')
    # test = str(soup.findAll('div', {'data-isinstock': True})[0])
    # print(get_product_url(test))
    test()