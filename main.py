from urllib.request import urlopen
from time import sleep
from bs4 import BeautifulSoup
from task_functions import task
import os.path

URL = 'https://www.avito.ru/moskva/kollektsionirovanie/monety'
file_path = 'ads.txt'


def get_html(url):
    """Collect HTML of a web page

    :param url: string, link to the page needed
    :return: string, HTML
    """
    response = urlopen(url)
    return response.read()


def get_number_of_pages(html):
    """Count the number of pages in the catalogue

    :param html: string, HTML of catalogue page
    :return: int, total number of pages
    """
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find('div', class_='pagination-pages clearfix')
    return int(pagination.find_all('a', href=True)[-1]['href'][-3:])


def parse(html):
    """Search the elements corresponding to the advertisements, process them and save to a list

    :param html: string, HTML of a page to be parsed
    :return: list, advertisement texts
    """
    soup = BeautifulSoup(html, 'html.parser')
    units = soup.find_all('div', class_='description')
    data = [unit.a.text.strip() for unit in units]
    return data


def main():
    if os.path.exists(file_path):
        pass
    else:
        pages_total = get_number_of_pages(get_html(URL))
        print('{} pages found'.format(pages_total))
        ads = []
        try:
            for page in range(1, pages_total + 1):
                print('Page {}/{}'.format(page, pages_total))
                ads.extend(parse(get_html(URL + '?p={}'.format(page))))
                sleep(5)
        finally:
            print('Saving...')
            with open(file_path, 'w') as f:
                f.writelines("{}\n".format(record) for record in ads)

    task(file_path)


if __name__ == '__main__':
    main()
