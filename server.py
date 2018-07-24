from flask import Flask, render_template
from cinemas import get_complete_info
# from flask_caching import Cache
from werkzeug.contrib.cache import FileSystemCache
import tempfile


app = Flask(__name__)
# cache = Cache(app, config={'CACHE_TYPE': 'simple'})
# tmpfile = tempfile.gettempdir()
cache = FileSystemCache(cache_dir=tempfile.gettempdir())


@app.route('/')
# @cache.cached(timeout=1200)
def films_list():
    movie_list = cache.get('movie_list')
    if movie_list is None:
        movie_list = get_complete_info()
        #movie_list = sorted(raw_movie_list, key=get_element, reverse=True)
        cache.set('movie_list', movie_list, timeout=30 * 30)
    return render_template('films_list.html', movie_list=movie_list[:10])


if __name__ == "__main__":
    app.run()
