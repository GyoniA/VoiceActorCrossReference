from flask import Flask, render_template, request, jsonify

from cross_reference import find_known_shows
from ratings_loader import load_csv_tv_ratings

app = Flask(__name__, static_folder='templates')

default_ratings = load_csv_tv_ratings()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    data = request.json
    actor_name = data.get('actor_name')
    show_title = data.get('show_title')
    role = data.get('role')
    results = find_known_shows(actor_name, show_title, role, default_ratings)
    results = [{"title": title, "character": role, "year": year} for title, role, year in results]
    return jsonify(results)


@app.route('/reload', methods=['POST'])
def reload():
    data = request.json
    csv_url = data.get('csv_url')
    global default_ratings
    if not csv_url or csv_url == 'None' or csv_url == '':
        default_ratings = load_csv_tv_ratings()
        return jsonify({"message": "Reloaded default ratings"})
    else:
        default_ratings = load_csv_tv_ratings(csv_url)
        return jsonify({"message": f"Reloaded ratings from {csv_url}"})


if __name__ == '__main__':
    app.run(debug=True)
