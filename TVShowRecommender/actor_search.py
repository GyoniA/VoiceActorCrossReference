import requests
import yaml
import tmdbsimple as tmdb
import logging

logger = logging.getLogger(__name__)

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
        response = tmdb.Search().person(query=actor_name)
        if not response["results"]:
            logger.error(f"No actor found for name: {actor_name}, ID: {actor_id}")
            return None
        actor_id = response["results"][0]["id"]

    person = tmdb.People(actor_id)
    credits = person.combined_credits()
    filmography = []

    for item in credits.get("cast", []):
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
    search = tmdb.Search()
    response = search.movie(query=title) if is_movie else search.tv(query=title)
    if not response["results"]:
        logger.error(f"No show found for title: {title}, role: {role}, is_movie: {is_movie}")
        return None

    sorted_results = sorted(response["results"], key=lambda res: res.get("release_date" if is_movie else "first_air_date", ""),
                            reverse=True)
    show_id = sorted_results[0]["id"]

    role_lower = role.lower()
    if is_movie:
        credits = tmdb.Movies(show_id).credits()
        for item in credits.get("cast", []):
            character = item.get("character")
            if character and (character == role or role_lower in character.lower()):
                return item.get("name"), item.get("id")
    else:
        credits_url = f"{tmdb_base_url}/tv/{show_id}/aggregate_credits"
        response = requests.get(credits_url, params={"api_key": api_key})
        if response.status_code != 200:
            logger.error(f"Error fetching credits for title: {title}, role: {role}, is_movie: {is_movie}")
            return None
        credits = response.json()
        for item in credits.get("cast", []):
            roles = item.get("roles", [])
            for role in roles:
                character = role.get("character")
                if character and (character == role or role_lower in character.lower()):
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

    role = "Toji Fushiguro"
    show = "Jujutsu Kaisen"

    actor, a_id = find_actor_by_role(show, role, is_movie=False)
    print(f"{role} in {show} is played by {actor} ({a_id})")
