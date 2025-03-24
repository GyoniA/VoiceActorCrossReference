import logging

from TVShowRecommender.actor_search import get_actor_filmography, find_actor_by_role
from TVShowRecommender.ratings_loader import load_csv_tv_ratings


logger = logging.getLogger(__name__)


def find_known_shows(actor_name=None, show_title=None, role=None, ratings=None):
    """
    Finds which shows the user knows an actor from based on their rated TV shows.
    :param actor_name: The name of the actor.
    :param show_title: The name of the show.
    :param role: The role played by the actor.
    :param ratings: A dictionary {title: rating}.
    :return: A list of known shows from user ratings.
    """
    if ratings is None:
        logger.debug("No ratings provided, loading from CSV")
        ratings = load_csv_tv_ratings()

    known_shows = []
    if actor_name is None or actor_name == "":
        if show_title and role:
            actor_name, _ = find_actor_by_role(show_title, role, is_movie=False)
            if actor_name is None:
                actor_name, _ = find_actor_by_role(show_title, role, is_movie=True)
        else:
            logger.error('Either actor_name or show_title and role are required.')
            return []
    if actor_name:
        filmography = get_actor_filmography(actor_name)
        if filmography:
            known_shows = [(title, role, year) for title, role, year in filmography if title in ratings]
    # Sort by release date descending
    known_shows.sort(key=lambda x: x[2], reverse=True)
    return known_shows


if __name__ == "__main__":
    # Example usage for finding known shows:
    name = "Takehito Koyasu"
    known_shows = find_known_shows(actor_name=name)
    print(f"User knows {name} from:", known_shows)

    role = "Toji"
    show = "Jujutsu Kaisen"
    known_shows = find_known_shows(show_title=show, role=role)
    print(f"User knows {role} in {show} from:", known_shows)