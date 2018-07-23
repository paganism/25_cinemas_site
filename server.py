from flask import Flask, render_template
from cinemas import get_movie_rating, fetch_afisha_page_data, fetch_cinema_count_and_titles_dict, fetch_proxy_list

app = Flask(__name__)

@app.route('/')
def films_list():
    afisha_content = fetch_afisha_page_data()
    cinema_count_and_titles_dict = fetch_cinema_count_and_titles_dict(afisha_content)
    proxies = fetch_proxy_list()
    movie_list = []
    for movie, count_of_cinema in cinema_count_and_titles_dict.items():
        rating_ball, rating_count, img_url = get_movie_rating(movie, proxies)
        movies = [movie, count_of_cinema, rating_ball, rating_count, img_url]
        movie_list.append(movies)
    top = 5
    # title, cinemas, rating, votes
    print(movie_list)
    return render_template('films_list.html', movie_list=movie_list[:10])


if __name__ == "__main__":
    app.run()
