"""
=============================================================================
MINI ANIME TRACKER - Python Fundamentals Learning Script
=============================================================================

PURPOSE:
    This standalone script teaches Python basics that you'll need for Django.
    It does NOT connect to your Django project - it's completely independent.

HOW TO RUN:
    python learn_python.py

WHAT YOU'LL LEARN:
    1. Variables & Data Types
    2. Functions
    3. Classes & Objects
    4. Modules & Imports
    5. Control Flow (if/else, loops)
    6. Working with APIs

=============================================================================
"""

# =============================================================================
# SECTION 1: IMPORTS
# =============================================================================
# 'import' brings code from other files (modules) into your script
# 'requests' is a library for making HTTP calls (same one your Django ETL uses)

import requests

# =============================================================================
# SECTION 2: CLASSES
# =============================================================================
# A class is a blueprint for creating objects
# Django Models are classes! (e.g., your Article model)
#
# ANATOMY OF A CLASS:
#   - class ClassName:        --> Defines the class
#   - def __init__(self):     --> Constructor, runs when object is created
#   - self.variable           --> Instance variable, unique to each object
#   - def method(self):       --> Function inside a class

class Anime:
    """
    Represents a single anime.

    Compare this to your Django model:

        class Article(models.Model):
            title = models.CharField(...)

    Same concept! But Django adds database powers.
    """

    def __init__(self, mal_id, title, episodes, score, status):
        """
        Constructor - called when you create a new Anime object.

        Example:
            anime = Anime(1, "Cowboy Bebop", 26, 8.75, "Finished")
                    ↑ This triggers __init__

        'self' refers to the object being created.
        """
        self.mal_id = mal_id        # Unique ID from MyAnimeList
        self.title = title          # Anime title (string)
        self.episodes = episodes    # Episode count (int or "?")
        self.score = score          # Rating (float or "N/A")
        self.status = status        # Airing status (string)

    def display_short(self):
        """
        Method - a function that belongs to the class.
        Returns a short one-line description.
        """
        return f"{self.title} ({self.episodes} eps) - Score: {self.score}"

    def display_full(self):
        """Returns detailed information."""
        return f"""
        Title:    {self.title}
        MAL ID:   {self.mal_id}
        Episodes: {self.episodes}
        Score:    {self.score}
        Status:   {self.status}
        """


# =============================================================================
# SECTION 3: FUNCTIONS
# =============================================================================
# Functions are reusable blocks of code
# Django views are functions! (e.g., your home() and detail() views)
#
# ANATOMY OF A FUNCTION:
#   - def function_name(parameters):
#   - """docstring""" (optional but recommended)
#   - code to execute
#   - return value (optional)

def fetch_top_anime(limit=5):
    """
    Fetches top-rated anime from the Jikan API.

    Parameters:
        limit (int): How many anime to fetch. Default is 5.

    Returns:
        list: List of anime data dictionaries, or empty list on error.

    WORKFLOW:
        1. Build the API URL
        2. Make HTTP GET request
        3. Check if successful (status code 200)
        4. Parse JSON response
        5. Return the data

    This is similar to your get_anime_news.py management command!
    """
    # API endpoint - Jikan is a free MyAnimeList API
    url = "https://api.jikan.moe/v4/top/anime"

    # Parameters sent with the request (becomes ?limit=5 in URL)
    params = {"limit": limit}

    try:
        # Make the HTTP request (like visiting a URL in browser)
        response = requests.get(url, params=params)

        # Check if request was successful
        # 200 = OK, 404 = Not Found, 500 = Server Error
        if response.status_code == 200:
            # .json() converts JSON string to Python dict/list
            data = response.json()
            return data["data"]  # API returns {"data": [...]}
        else:
            print(f"API Error: Status {response.status_code}")
            return []

    except requests.exceptions.RequestException as e:
        # Handle network errors (no internet, timeout, etc.)
        print(f"Network Error: {e}")
        return []


def fetch_anime_by_id(anime_id):
    """
    Fetches a single anime by its MyAnimeList ID.

    Parameters:
        anime_id (int): The MAL ID of the anime.

    Returns:
        dict or None: Anime data if found, None otherwise.
    """
    url = f"https://api.jikan.moe/v4/anime/{anime_id}"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()["data"]
        elif response.status_code == 404:
            print(f"Anime with ID {anime_id} not found.")
            return None
        else:
            print(f"API Error: Status {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Network Error: {e}")
        return None


def create_anime_object(data):
    """
    Converts raw API data (dict) into an Anime object.

    This is like a mini "serializer" - transforming data from one format
    to another. Django REST Framework uses serializers for this!

    Parameters:
        data (dict): Raw anime data from API

    Returns:
        Anime: An Anime object
    """
    # .get() safely gets a value, returns default if key doesn't exist
    # This prevents KeyError crashes
    return Anime(
        mal_id=data["mal_id"],
        title=data["title"],
        episodes=data.get("episodes", "?"),      # Default "?" if missing
        score=data.get("score", "N/A"),          # Default "N/A" if missing
        status=data.get("status", "Unknown")
    )


def create_anime_list(data_list):
    """
    Converts a list of API data into a list of Anime objects.

    WORKFLOW:
        1. Create empty list to store results
        2. Loop through each item in data_list
        3. Convert each item to Anime object
        4. Add to results list
        5. Return the list
    """
    anime_list = []

    for item in data_list:
        anime = create_anime_object(item)
        anime_list.append(anime)

    return anime_list


def search_anime(query):
    """
    Searches for anime by name.

    Parameters:
        query (str): Search term

    Returns:
        list: List of matching anime data
    """
    url = "https://api.jikan.moe/v4/anime"
    params = {"q": query, "limit": 5}

    try:
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json()["data"]
        return []

    except requests.exceptions.RequestException:
        return []


# =============================================================================
# SECTION 4: USER INTERFACE FUNCTIONS
# =============================================================================
# These functions handle displaying information and getting user input

def display_menu():
    """
    Displays the main menu and returns user's choice.

    Returns:
        str: The user's menu selection
    """
    print("\n" + "=" * 50)
    print("       ANIME TRACKER - Learn Python")
    print("=" * 50)
    print("  1. View Top 5 Anime")
    print("  2. Search Anime by ID")
    print("  3. Search Anime by Name")
    print("  4. Exit")
    print("=" * 50)

    choice = input("Enter your choice (1-4): ").strip()
    return choice


def display_anime_list(anime_list):
    """
    Displays a list of Anime objects in a formatted way.

    Parameters:
        anime_list (list): List of Anime objects
    """
    if not anime_list:
        print("No anime to display.")
        return

    print("\n" + "-" * 50)
    for i, anime in enumerate(anime_list, start=1):
        # enumerate() gives us both index (i) and value (anime)
        print(f"  {i}. {anime.display_short()}")
    print("-" * 50)


# =============================================================================
# SECTION 5: MAIN PROGRAM LOGIC
# =============================================================================
# The main() function orchestrates everything
# This is the "controller" - Django views serve a similar purpose

def main():
    """
    Main program loop.

    WORKFLOW:
        1. Display menu
        2. Get user choice
        3. Execute corresponding action
        4. Repeat until user exits

    This pattern is similar to how web apps work:
        1. User makes request (clicks link)
        2. Server processes request (view function)
        3. Server returns response (template)
        4. Repeat
    """
    print("\nWelcome to Anime Tracker!")
    print("This script teaches Python basics for Django development.")

    # Main program loop - keeps running until user chooses to exit
    while True:
        choice = display_menu()

        # === OPTION 1: View Top Anime ===
        if choice == "1":
            print("\nFetching top anime from MyAnimeList...")

            # Step 1: Fetch raw data from API
            raw_data = fetch_top_anime(limit=5)

            # Step 2: Convert to Anime objects
            anime_list = create_anime_list(raw_data)

            # Step 3: Display to user
            display_anime_list(anime_list)

        # === OPTION 2: Search by ID ===
        elif choice == "2":
            anime_id = input("\nEnter MAL anime ID (e.g., 1 for Cowboy Bebop): ").strip()

            # Validate input is a number
            if not anime_id.isdigit():
                print("Please enter a valid number.")
                continue  # Skip to next loop iteration

            print(f"\nFetching anime with ID {anime_id}...")

            # Fetch and display
            raw_data = fetch_anime_by_id(anime_id)

            if raw_data:
                anime = create_anime_object(raw_data)
                print(anime.display_full())

        # === OPTION 3: Search by Name ===
        elif choice == "3":
            query = input("\nEnter anime name to search: ").strip()

            if not query:
                print("Please enter a search term.")
                continue

            print(f"\nSearching for '{query}'...")

            raw_data = search_anime(query)
            anime_list = create_anime_list(raw_data)
            display_anime_list(anime_list)

        # === OPTION 4: Exit ===
        elif choice == "4":
            print("\nThank you for using Anime Tracker!")
            print("Now you're ready to understand Django better.")
            print("Goodbye!\n")
            break  # Exit the while loop

        # === Invalid Choice ===
        else:
            print("\nInvalid choice. Please enter 1, 2, 3, or 4.")


# =============================================================================
# SECTION 6: SCRIPT ENTRY POINT
# =============================================================================
# This is a Python convention for scripts

if __name__ == "__main__":
    """
    This block only runs when you execute this file directly:
        python learn_python.py

    It does NOT run when the file is imported:
        from learn_python import Anime  # __name__ would be "learn_python"

    Django uses this pattern in manage.py!
    """
    main()
