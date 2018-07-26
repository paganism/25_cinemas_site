from flask import Flask, render_template
from cinemas import get_complete_info
from werkzeug.contrib.cache import FileSystemCache
import tempfile


app = Flask(__name__)
cache = FileSystemCache(cache_dir=tempfile.gettempdir())


@app.route('/')
def films_list():
    movie_list = cache.get('movie_list')
    if movie_list is None:
        movie_list = get_complete_info()
        cache.set('movie_list', movie_list, timeout=30 * 30)
    return render_template('films_list.html', movie_list=movie_list)


if __name__ == "__main__":
    app.run()
