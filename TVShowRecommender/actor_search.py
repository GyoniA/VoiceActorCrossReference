import requests
import yaml
import tmdbsimple as tmdb

with open('config.yaml', 'r') as stream:
    config = yaml.safe_load(stream)
api_key = config["TMDB_API_KEY"]
tmdb.API_KEY = api_key
tmdb.REQUESTS_TIMEOUT = 5
tmdb_base_url = "https://api.themoviedb.org/3"


def get_actor_filmography(actor_name: str = None, actor_id=None):
    """
    Fetches the filmography of an actor using the TMDb API. Either actor_name or actor_id is required.
    :param actor_name: The optional name of the actor.
    :param actor_id: The optional ID of the actor.
    :return: a list of tuples containing the title, role, and year of the film/TV show.
    """
    if actor_id is None:
        search_url = f"{tmdb_base_url}/search/person"

        params = {
            "api_key": api_key,
            "query": actor_name,
        }

        response = requests.get(search_url, params=params)
        if response.status_code != 200:
            print("Error fetching data from TMDb API")
            return None

        data = response.json()
        if "results" not in data or not data["results"]:
            print("No actor found")
            return None
        actor_id = data["results"][0]["id"]

    filmography_url = f"{tmdb_base_url}/person/{actor_id}/combined_credits"

    response = requests.get(filmography_url, params={"api_key": api_key})
    if response.status_code != 200:
        print("Error fetching filmography")
        return None

    filmography_data = response.json()
    filmography = []

    for item in filmography_data.get("cast", []):
        title = item.get("title") or item.get("name", "Unknown Title")
        year = item.get("release_date") or item.get("first_air_date", "Unknown Year")
        role = item.get("character")
        filmography.append((title, role, year))

    return filmography


def find_actor_by_role(title: str, role: str, is_movie=False):
    """
    Finds an actor in a show by their role.
    :param title: The name of the show/movie to search in.
    :param role: The role of the actor to find.
    :param is_movie: Whether to search for movies.
    :return: The actor's name, and id.
    """
    search_url = f"{tmdb_base_url}/search/movie" if is_movie else f"{tmdb_base_url}/search/tv"

    params = {
        "api_key": api_key,
        "query": title,
    }

    response = requests.get(search_url, params=params)
    if response.status_code != 200:
        print("Error fetching data from TMDb API")
        return None

    data = response.json()
    if "results" not in data or not data["results"]:
        print("No show found")
        return None

    if is_movie:
        sorted_results = sorted(data["results"], key=lambda res: res["release_date"], reverse=True)
    else:
        sorted_results = sorted(data["results"], key=lambda res: res["first_air_date"], reverse=True)
    show_id = sorted_results[0]["id"]
    credits_url = f"{tmdb_base_url}/movie/{show_id}/credits" if is_movie else f"{tmdb_base_url}/tv/{show_id}/credits"

    response = requests.get(credits_url, params={"api_key": api_key})
    if response.status_code != 200:
        print("Error fetching credits")
        return None

    credits_data = response.json()
    role_lower = role.lower()
    for item in credits_data.get("cast", []):
        character = item.get("character")
        if character == role or role_lower in character.lower():
            return item.get("name"), item.get("id")

    return None, None


if __name__ == "__main__":
    # Example usage:
    name = "Takehito Koyasu"
    entries = get_actor_filmography(name)
    # Sort by year
    entries.sort(key=lambda x: x[2])
    if entries:
        for actor_title, actor_role, actor_year in entries:
            print(f"{actor_title} ({actor_year}) - {actor_role}")

    role = "Toji"
    show = "Jujutsu Kaisen"

    actor, a_id = find_actor_by_role(show, role, is_movie=False)
    print(f"{role} in {show} is played by {actor} ({a_id})")
