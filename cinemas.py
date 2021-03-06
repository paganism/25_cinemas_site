import requests
from bs4 import BeautifulSoup
import re
import random
import queue
import threading


def fetch_proxy_list():
    payload = {'anonymity': 'false', 'token': 'demo'}
    proxy_url = 'http://freeproxy-list.ru/api/proxy'
    proxy_list = requests.get(proxy_url, params=payload).text.split('\n')
    return proxy_list


def fetch_afisha_page_data():
    response = requests.get('http://www.afisha.ru/msk/schedule_cinema/')
    return response.text


def fetch_cinema_count_and_titles_dict(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')
    cinemas = soup.find(class_='cards cards-grid')
    count_cinemas = []
    for cinema in cinemas.find_all('div', {'itemprop': "address"}):
        count = re.findall(r'\d+', str(cinema))
        count_cinemas.append(count[0])
    title_list = []
    for i in cinemas.find_all('h3', {'class': 'card__title'}):
        title_list.append(i.text.strip().replace('«', '').replace('»', ''))
    titles_and_cinema_count_dict = dict(zip(title_list, count_cinemas))
    return titles_and_cinema_count_dict


def get_movie_rating(movie_title, proxies):
    kp_url = 'https://www.kinopoisk.ru/index.php'
    payload = {'kp_query': movie_title, 'first': 'yes'}
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:45.0) '
            'Gecko/20100101 Firefox/42.0',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'
    }
    proxy = {"http": random.choice(proxies)}
    raw_movie_info = requests.get(
        kp_url,
        params=payload,
        headers=headers,
        proxies=proxy
    )
    try:
        soup = BeautifulSoup(raw_movie_info.text, 'html.parser')
        rating_ball = float(soup.find('span', class_='rating_ball').get_text())
        rating_count = soup.find(
            'span',
            class_='ratingCount'
        ).get_text().replace(' ', '')
        url_img = soup.find('a', class_='popupBigImage').img['src']
        movie_params = dict(rating_ball=rating_ball, rating_count=rating_count, img_url=url_img)
        return movie_params
    except AttributeError:
        movie_params = dict(rating_ball='0', rating_count='0', img_url='/static/img/default-image.png')
        return movie_params


def run_movie_rating_fetcher(movie_params):
    movie_params_queue = queue.Queue()
    movie_params_queue.put(movie_params)
    return movie_params_queue


def get_second_element(element):
    return float(element[2])


def output_movies_to_console(movie_list, top):
    sorted_list = sorted(movie_list, key=get_second_element, reverse=True)
    delimiter = '-' * 30
    for title, cinemas, rating, votes in sorted_list[:top]:
        print(delimiter)
        print('Movie name: {}'.format(title))
        print('Count of cinemas: {}'.format(cinemas))
        print('Rating: {}'.format(rating))
        print('Count of votes: {}'.format(votes))


def get_complete_info():
    afisha_content = fetch_afisha_page_data()
    cinema_count_and_titles_dict = fetch_cinema_count_and_titles_dict(afisha_content)
    proxies = fetch_proxy_list()
    full_movie_list = []
    for movie, count_of_cinema in cinema_count_and_titles_dict.items():
        movie_params_dict = get_movie_rating(movie, proxies)
        movie_params_queue = run_movie_rating_fetcher(movie_params_dict)
        movie_params = movie_params_queue.get()
        rating_ball = movie_params['rating_ball']
        rating_count = movie_params['rating_count']
        img_url = movie_params['img_url']
        movie_param_list = [movie, count_of_cinema, rating_ball, rating_count, img_url]
        full_movie_list.append(movie_param_list)
    sorted_list = sorted(full_movie_list, key=get_second_element, reverse=True)
    top_movies = 10
    return sorted_list[:top_movies]


if __name__ == '__main__':
    pass
