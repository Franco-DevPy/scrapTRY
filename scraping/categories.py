import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from scraping.singlebook import get_info_book
import csv



#FIND ALL URL CATEGORY 

def find_category(soup):
        url = "https://books.toscrape.com/"
        nmb = 0
        urls_absolutes = []
        aside = soup.find('aside')
        aside_category = aside.find('div', class_="side_categories")
        links = aside_category.find_all('a')
        #categories_title =  [category.text.strip() for category in links[1:]]
        categories_url =  [category['href'] for category in links[1:]]
        #for categorie_title ,category_url in zip(categories_title, categories_url):
        for category_url in  categories_url:
            url_absolut = urljoin(url, category_url)
            urls_absolutes.append(url_absolut)
            nmb += 1
            #print('URLS DES CATEGORIES: ', nmb )        
            #print(categorie_title, url_absolut)

        return urls_absolutes 





def all_book_for_category(urls_all_category):
        categories = urls_all_category
        for category_url in categories:
            # 2. Inicializar la lista de libros
            urls_books_single = []
            # 3. Mientras haya una página
            while category_url:
                # 3a. Buscar los libros en la página actual
                url = category_url
                response = requests.get(url)
                html_response = response.text
                soup = BeautifulSoup(html_response, "html.parser") 
                title_category = soup.find('div', class_="page-header")
                title_book_h = title_category.find('h1').text.strip()
                row = soup.find('ol', class_='row')
                title_h = row.find_all("h3")
                for title in title_h:
                    title_href = title.find('a').get('href')
                    final_url = urljoin(url, title_href )
                    urls_books_single.append(final_url)
                
                # 3b. Verificar si hay un botón "next"
                next_button = soup.find('li', class_="next")
                if next_button is not None:
                    href_button = next_button.find('a').get('href')
                    category_url = urljoin(url, href_button)
                else:
                    category_url = None       
            # 4. Guardar los libros en un archivo CSV
            with open(f"scraping/data/csv/{title_book_h}.csv", "w", newline="", encoding="utf-8") as fichier_csv:
                writer = csv.writer(fichier_csv, delimiter=',')
                # Escribir los encabezados si es necesario
                writer.writerow(["Title", "Category", "Rating", "Stock", "Description", "UPC", "Product Type", "Price (excl. tax)", "Price (incl. tax)", "Tax", "Availability", "Number of reviews", "Img url"])
                
                for url_book in urls_books_single:
                    books_all = get_info_book(url_book)
                    # Escribe cada valor del diccionario como una fila
                    writer.writerow(books_all.values())
