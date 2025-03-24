import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
                             QPushButton, QTextEdit)
from PyQt6.QtGui import QFont
from qt_material import apply_stylesheet

from TVShowRecommender.cross_reference import find_known_shows
from TVShowRecommender.ratings_loader import load_csv_tv_ratings
from TVShowRecommender.recommender import recommend_shows

# Load TV ratings from Google Sheets
tv_ratings = load_csv_tv_ratings()


class VoiceActorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Voice Actor Finder & Recommender")
        self.setGeometry(100, 100, 500, 400)

        layout = QVBoxLayout()

        # Input for actor name
        self.actor_label = QLabel("Enter Actor Name:")
        self.actor_label.setFont(QFont("Arial", 12))
        self.actor_input = QLineEdit()
        self.actor_input.setStyleSheet("color: white")

        # Input for show title & role
        self.show_label = QLabel("Or Enter Show Title & Role:")
        self.show_label.setFont(QFont("Arial", 12))
        self.show_input = QLineEdit()
        self.show_input.setStyleSheet("color: white")
        self.role_input = QLineEdit()
        self.role_input.setStyleSheet("color: white")

        # Search button
        self.search_button = QPushButton("Find Where You Know Them From")
        self.search_button.clicked.connect(self.find_known_appearances)

        # Recommendations button
        self.recommend_button = QPushButton("Get Recommendations")
        self.recommend_button.clicked.connect(self.get_recommendations)

        # Results area
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)

        # Adding widgets to layout
        layout.addWidget(self.actor_label)
        layout.addWidget(self.actor_input)
        layout.addWidget(self.show_label)
        layout.addWidget(self.show_input)
        layout.addWidget(self.role_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.recommend_button)
        layout.addWidget(self.results_text)

        self.setLayout(layout)

    def find_known_appearances(self):
        actor_name = self.actor_input.text().strip()
        show_title = self.show_input.text().strip()
        role = self.role_input.text().strip()

        results = find_known_shows(actor_name=actor_name, show_title=show_title, role=role, ratings=tv_ratings)

        if results:
            output_text = "\n".join([f"{title} ({year}) - {role}" for title, role, year in results])
        else:
            output_text = "No known shows found."

        self.results_text.setText(output_text)

    def get_recommendations(self):
        recommendations = recommend_shows(tv_ratings)
        output_text = "\n".join(recommendations) if recommendations else "No recommendations available."
        self.results_text.setText(output_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_blue.xml')  # Apply Material Design theme
    window = VoiceActorApp()
    window.show()
    sys.exit(app.exec())
