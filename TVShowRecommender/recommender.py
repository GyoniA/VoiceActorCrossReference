import yaml
from google import genai
import logging

from google.genai import types

from TVShowRecommender.ratings_loader import load_csv_tv_ratings

logger = logging.getLogger(__name__)

with open('config.yaml', 'r') as stream:
    config = yaml.safe_load(stream)
google_ai_studio_api_key = config["GOOGLE_AI_STUDIO_API_KEY"]


def recommend_shows(ratings):
    """
    Recommends new shows based on the user's ratings using the Google AI Studio API.
    :param ratings: A dictionary in the format: {title: rating}.
    :return: A list of recommended show titles.
    """
    prompt = "Here is a list of TV shows the user has watched and rated (out of 100), where 100 is the best:\n"
    for title, score in ratings.items():
        prompt += f"- {title}: {score}/100\n"
    prompt += ("\nBased on these preferences, recommend 20 similar TV shows they might enjoy. "
               )
    sys_instructions = ("You are a helpful assistant that recommends new TV shows based on the user's preferences." +
                        "Only list the show titles." +
                        "Do not recommend shows that are already in the user's list." +
                        "Only list the show titles without a - or anything preceding them, and separate them by line breaks.")

    try:
        client = genai.Client(api_key=google_ai_studio_api_key)
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=[prompt],
            config=types.GenerateContentConfig(
                system_instruction=sys_instructions,
            )
        )
        recommendations = response.text.split("\n")
        recommendations = [rec.strip() for rec in recommendations]
        # Remove already watched shows
        watched_shows = [title for title, score in ratings.items()]
        return [rec for rec in recommendations if rec not in watched_shows]
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        return []


if __name__ == "__main__":
    # Example usage:
    tv_ratings = load_csv_tv_ratings()

    recommendations = recommend_shows(tv_ratings)
    print("Recommended shows:", recommendations)
