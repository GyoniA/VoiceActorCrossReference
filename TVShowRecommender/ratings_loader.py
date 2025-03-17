import yaml
import pandas as pd
import logging

logger = logging.getLogger(__name__)

with open('config.yaml', 'r') as stream:
    config = yaml.safe_load(stream)
google_sheets_url = config["GOOGLE_CSV_LINK"]


def load_csv_tv_ratings(sheet_url=google_sheets_url):
    """
    Loads TV show ratings from a public Google Sheets CSV link.
    :param sheet_url: The public CSV link to the Google Sheet.
    :return: A dictionary {title: rating}.
    """
    try:
        df = pd.read_csv(sheet_url)
        ratings = dict(zip(df.iloc[:, 0], df.iloc[:, 1]))  # Extract title and rating
        ratings = {k: v for k, v in ratings.items() if not pd.isna(v)}
        return ratings
    except Exception as e:
        logger.error(f"Error loading TV ratings: {e}")
        return {}


if __name__ == "__main__":
    # Example usage:
    tv_ratings = load_csv_tv_ratings()
    print("Loaded TV ratings:", tv_ratings)
