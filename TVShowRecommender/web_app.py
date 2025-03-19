from flask import Flask, render_template, request, jsonify

from TVShowRecommender.cross_reference import find_known_shows
from TVShowRecommender.ratings_loader import load_csv_tv_ratings
from TVShowRecommender.recommender import recommend_shows

app = Flask(__name__)


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
    results = [f"{title} ({year}) - {role}" for title, role, year in results]
    return jsonify(results)


@app.route('/recommend', methods=['GET'])
def recommend():
    recommendations = recommend_shows(default_ratings)
    return jsonify(recommendations)


if __name__ == '__main__':
    app.run(debug=True)
