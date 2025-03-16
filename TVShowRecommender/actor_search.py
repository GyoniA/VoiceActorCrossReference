import requests
import yaml

with open('config.yaml', 'r') as stream:
    config = yaml.safe_load(stream)
api_key = config["TMDB_API_KEY"]


def get_actor_filmography(actor_name):
    """
    Fetches the filmography of an actor using the TMDb API.
    :param actor_name: The name of the actor.
    :return: a list of tuples containing the title, role, and year of the film/TV show.
    """
    base_url = "https://api.themoviedb.org/3"
    search_url = f"{base_url}/search/person"

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
    filmography_url = f"{base_url}/person/{actor_id}/combined_credits"

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


if __name__ == "__main__":
    # Example usage:
    name = "Takehito Koyasu"
    entries = get_actor_filmography(name)
    # Sort by year
    entries.sort(key=lambda x: x[2])
    if entries:
        for title, role, year in entries:
            print(f"{title} ({year}) - {role}")
