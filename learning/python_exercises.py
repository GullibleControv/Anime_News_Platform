"""
=============================================================================
PYTHON EXERCISES - Practice Without AI
=============================================================================

RULES:
    1. Do NOT use AI to solve these
    2. Struggle is learning - getting stuck is normal
    3. Use Google/docs if needed, but type the code yourself
    4. Run this file after each exercise to test: python python_exercises.py

HOW IT WORKS:
    - Each exercise has a function with 'pass' or '...'
    - Replace that with your code
    - Tests at the bottom will check your answers
    - Start with Exercise 1, don't skip ahead

YOUR STACK AT WORK: Python, JavaScript, PostgreSQL, Docker
These exercises focus on Python patterns you'll see daily.

=============================================================================
"""


# =============================================================================
# EXERCISE 1: Variables and Types
# =============================================================================
# At work, you'll constantly deal with different data types.
# Understanding them prevents bugs.

def exercise_1_variables():
    """
    Create these variables:
    - username: a string with value "admin"
    - login_count: an integer with value 5
    - is_active: a boolean with value True
    - score: a float with value 98.5

    Return them as a dictionary with these exact keys:
    {"username": ..., "login_count": ..., "is_active": ..., "score": ...}
    """
    # YOUR CODE HERE (replace pass)
    pass


# =============================================================================
# EXERCISE 2: String Operations
# =============================================================================
# Strings are everywhere: usernames, emails, URLs, error messages

def exercise_2_strings(email):
    """
    Given an email like "USER@Example.COM", return a cleaned version:
    - all lowercase
    - no leading/trailing spaces

    Example: "  USER@Example.COM  " -> "user@example.com"

    Hint: Look up .lower() and .strip() methods
    """
    # YOUR CODE HERE
    pass


def exercise_2b_extract_domain(email):
    """
    Extract the domain from an email.

    Example: "john@google.com" -> "google.com"

    Hint: Look up .split() method
    """
    # YOUR CODE HERE
    pass


# =============================================================================
# EXERCISE 3: Lists
# =============================================================================
# Lists store collections of items. You'll use them constantly.

def exercise_3_list_operations(numbers):
    """
    Given a list of numbers, return a dictionary with:
    - "count": how many numbers
    - "sum": total of all numbers
    - "first": first number
    - "last": last number

    Example: [1, 2, 3, 4, 5] -> {"count": 5, "sum": 15, "first": 1, "last": 5}

    Hint: len(), sum(), list indexing with [0] and [-1]
    """
    # YOUR CODE HERE
    pass


def exercise_3b_filter_positive(numbers):
    """
    Return only the positive numbers from the list.

    Example: [-1, 2, -3, 4, 0, 5] -> [2, 4, 5]

    Hint: Use a for loop, or look up list comprehensions
    """
    # YOUR CODE HERE
    pass


# =============================================================================
# EXERCISE 4: Dictionaries
# =============================================================================
# Dictionaries are KEY in Python (pun intended).
# API responses, database rows, configs - all use dicts.

def exercise_4_dict_operations(user):
    """
    Given a user dictionary like:
    {"name": "John", "age": 25, "email": "john@test.com"}

    Return a formatted string:
    "John (25) - john@test.com"

    Hint: Access dict values with user["key"] or user.get("key")
    """
    # YOUR CODE HERE
    pass


def exercise_4b_safe_get(user, key):
    """
    Safely get a value from the user dict.
    If the key doesn't exist, return "Unknown"

    Example:
        safe_get({"name": "John"}, "name") -> "John"
        safe_get({"name": "John"}, "age") -> "Unknown"

    Hint: .get() method with a default value
    """
    # YOUR CODE HERE
    pass


# =============================================================================
# EXERCISE 5: Functions with Logic
# =============================================================================
# Functions let you reuse code. These simulate real work scenarios.

def exercise_5_check_password(password):
    """
    Check if a password is valid. Rules:
    - At least 8 characters long
    - Contains at least one number

    Return True if valid, False otherwise.

    Example:
        "hello" -> False (too short)
        "helloworld" -> False (no number)
        "hello123" -> True

    Hint: len(), .isdigit(), loop through characters with 'for char in password'
    """
    # YOUR CODE HERE
    pass


def exercise_5b_categorize_score(score):
    """
    Categorize a score (0-100) into grades:
    - 90-100: "A"
    - 80-89: "B"
    - 70-79: "C"
    - 60-69: "D"
    - Below 60: "F"

    Hint: Use if/elif/else
    """
    # YOUR CODE HERE
    pass


# =============================================================================
# EXERCISE 6: Loops
# =============================================================================
# Loops process collections. Essential for handling data.

def exercise_6_count_words(text):
    """
    Count how many words are in a text string.
    Words are separated by spaces.

    Example: "Hello world how are you" -> 5

    Hint: .split() turns string into list of words
    """
    # YOUR CODE HERE
    pass


def exercise_6b_find_longest_word(text):
    """
    Find the longest word in a text.
    If there's a tie, return the first one.

    Example: "The quick brown fox" -> "quick"

    Hint: Loop through words, track the longest one
    """
    # YOUR CODE HERE
    pass


# =============================================================================
# EXERCISE 7: Error Handling
# =============================================================================
# Code breaks. Good engineers handle errors gracefully.

def exercise_7_safe_divide(a, b):
    """
    Divide a by b, but handle division by zero.

    If b is 0, return None instead of crashing.
    Otherwise return the result.

    Example:
        safe_divide(10, 2) -> 5.0
        safe_divide(10, 0) -> None

    Hint: try/except ZeroDivisionError
    """
    # YOUR CODE HERE
    pass


def exercise_7b_parse_int(value):
    """
    Convert a string to integer safely.

    If it can't be converted, return 0.

    Example:
        parse_int("42") -> 42
        parse_int("hello") -> 0
        parse_int("3.14") -> 0

    Hint: try/except ValueError, int()
    """
    # YOUR CODE HERE
    pass


# =============================================================================
# EXERCISE 8: Working with Data (like API responses)
# =============================================================================
# At work, you process data from APIs and databases constantly.

def exercise_8_extract_titles(articles):
    """
    Given a list of article dictionaries, extract just the titles.

    Example:
        articles = [
            {"id": 1, "title": "News 1", "content": "..."},
            {"id": 2, "title": "News 2", "content": "..."}
        ]
        Result: ["News 1", "News 2"]

    Hint: Loop and append, or list comprehension
    """
    # YOUR CODE HERE
    pass


def exercise_8b_filter_by_category(articles, category):
    """
    Return only articles that match the given category.

    Example:
        articles = [
            {"title": "A", "category": "news"},
            {"title": "B", "category": "review"},
            {"title": "C", "category": "news"}
        ]
        filter_by_category(articles, "news") -> [{"title": "A", ...}, {"title": "C", ...}]
    """
    # YOUR CODE HERE
    pass


def exercise_8c_count_by_category(articles):
    """
    Count how many articles are in each category.

    Example:
        articles = [
            {"title": "A", "category": "news"},
            {"title": "B", "category": "review"},
            {"title": "C", "category": "news"}
        ]
        Result: {"news": 2, "review": 1}

    Hint: Create empty dict, loop through articles, increment counts
    """
    # YOUR CODE HERE
    pass


# =============================================================================
# EXERCISE 9: Classes (Object-Oriented Basics)
# =============================================================================
# Django models are classes. Understanding classes is crucial.

class Exercise9User:
    """
    Create a User class with:
    - __init__ that takes username and email
    - a method called 'greet' that returns "Hello, {username}!"
    - a method called 'is_valid_email' that returns True if email contains '@'

    Example:
        user = Exercise9User("john", "john@test.com")
        user.greet() -> "Hello, john!"
        user.is_valid_email() -> True
    """

    def __init__(self, username, email):
        # YOUR CODE HERE
        pass

    def greet(self):
        # YOUR CODE HERE
        pass

    def is_valid_email(self):
        # YOUR CODE HERE
        pass


# =============================================================================
# EXERCISE 10: Putting It Together
# =============================================================================
# This simulates a real task: processing API data

def exercise_10_process_anime_data(raw_data):
    """
    Process raw anime API data into a clean format.

    Input (list of dicts from API):
    [
        {"mal_id": 1, "title": "Anime A", "score": 8.5, "episodes": 24},
        {"mal_id": 2, "title": "Anime B", "score": None, "episodes": 12},
        {"mal_id": 3, "title": "Anime C", "score": 9.0, "episodes": None}
    ]

    Output (cleaned list):
    [
        {"id": 1, "name": "Anime A", "rating": 8.5, "eps": 24},
        {"id": 2, "name": "Anime B", "rating": 0, "eps": 12},
        {"id": 3, "name": "Anime C", "rating": 9.0, "eps": 0}
    ]

    Rules:
    - Rename keys: mal_id->id, title->name, score->rating, episodes->eps
    - If score is None, use 0
    - If episodes is None, use 0

    This is EXACTLY what you do when processing API responses!
    """
    # YOUR CODE HERE
    pass


# =============================================================================
# TEST RUNNER - Don't modify below this line
# =============================================================================

def run_tests():
    """Run all exercise tests and show results."""

    print("\n" + "=" * 60)
    print("       PYTHON EXERCISES - TEST RESULTS")
    print("=" * 60 + "\n")

    passed = 0
    failed = 0

    # Test Exercise 1
    try:
        result = exercise_1_variables()
        expected = {"username": "admin", "login_count": 5, "is_active": True, "score": 98.5}
        assert result == expected, f"Got {result}"
        print("[PASS] Exercise 1: Variables")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Exercise 1: Variables - {e}")
        failed += 1

    # Test Exercise 2
    try:
        result = exercise_2_strings("  USER@Example.COM  ")
        assert result == "user@example.com", f"Got {result}"
        print("[PASS] Exercise 2: String cleaning")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Exercise 2: String cleaning - {e}")
        failed += 1

    # Test Exercise 2b
    try:
        result = exercise_2b_extract_domain("john@google.com")
        assert result == "google.com", f"Got {result}"
        print("[PASS] Exercise 2b: Extract domain")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Exercise 2b: Extract domain - {e}")
        failed += 1

    # Test Exercise 3
    try:
        result = exercise_3_list_operations([1, 2, 3, 4, 5])
        expected = {"count": 5, "sum": 15, "first": 1, "last": 5}
        assert result == expected, f"Got {result}"
        print("[PASS] Exercise 3: List operations")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Exercise 3: List operations - {e}")
        failed += 1

    # Test Exercise 3b
    try:
        result = exercise_3b_filter_positive([-1, 2, -3, 4, 0, 5])
        assert result == [2, 4, 5], f"Got {result}"
        print("[PASS] Exercise 3b: Filter positive")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Exercise 3b: Filter positive - {e}")
        failed += 1

    # Test Exercise 4
    try:
        result = exercise_4_dict_operations({"name": "John", "age": 25, "email": "john@test.com"})
        assert result == "John (25) - john@test.com", f"Got {result}"
        print("[PASS] Exercise 4: Dict operations")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Exercise 4: Dict operations - {e}")
        failed += 1

    # Test Exercise 4b
    try:
        result1 = exercise_4b_safe_get({"name": "John"}, "name")
        result2 = exercise_4b_safe_get({"name": "John"}, "age")
        assert result1 == "John" and result2 == "Unknown", f"Got {result1}, {result2}"
        print("[PASS] Exercise 4b: Safe get")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Exercise 4b: Safe get - {e}")
        failed += 1

    # Test Exercise 5
    try:
        assert exercise_5_check_password("hello") == False
        assert exercise_5_check_password("helloworld") == False
        assert exercise_5_check_password("hello123") == True
        assert exercise_5_check_password("hi1") == False
        print("[PASS] Exercise 5: Password check")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Exercise 5: Password check - {e}")
        failed += 1

    # Test Exercise 5b
    try:
        assert exercise_5b_categorize_score(95) == "A"
        assert exercise_5b_categorize_score(85) == "B"
        assert exercise_5b_categorize_score(75) == "C"
        assert exercise_5b_categorize_score(65) == "D"
        assert exercise_5b_categorize_score(55) == "F"
        print("[PASS] Exercise 5b: Categorize score")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Exercise 5b: Categorize score - {e}")
        failed += 1

    # Test Exercise 6
    try:
        result = exercise_6_count_words("Hello world how are you")
        assert result == 5, f"Got {result}"
        print("[PASS] Exercise 6: Count words")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Exercise 6: Count words - {e}")
        failed += 1

    # Test Exercise 6b
    try:
        result = exercise_6b_find_longest_word("The quick brown fox")
        assert result == "quick", f"Got {result}"
        print("[PASS] Exercise 6b: Longest word")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Exercise 6b: Longest word - {e}")
        failed += 1

    # Test Exercise 7
    try:
        assert exercise_7_safe_divide(10, 2) == 5.0
        assert exercise_7_safe_divide(10, 0) is None
        print("[PASS] Exercise 7: Safe divide")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Exercise 7: Safe divide - {e}")
        failed += 1

    # Test Exercise 7b
    try:
        assert exercise_7b_parse_int("42") == 42
        assert exercise_7b_parse_int("hello") == 0
        assert exercise_7b_parse_int("3.14") == 0
        print("[PASS] Exercise 7b: Parse int")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Exercise 7b: Parse int - {e}")
        failed += 1

    # Test Exercise 8
    try:
        articles = [
            {"id": 1, "title": "News 1", "content": "..."},
            {"id": 2, "title": "News 2", "content": "..."}
        ]
        result = exercise_8_extract_titles(articles)
        assert result == ["News 1", "News 2"], f"Got {result}"
        print("[PASS] Exercise 8: Extract titles")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Exercise 8: Extract titles - {e}")
        failed += 1

    # Test Exercise 8b
    try:
        articles = [
            {"title": "A", "category": "news"},
            {"title": "B", "category": "review"},
            {"title": "C", "category": "news"}
        ]
        result = exercise_8b_filter_by_category(articles, "news")
        assert len(result) == 2, f"Got {len(result)} items"
        assert all(a["category"] == "news" for a in result)
        print("[PASS] Exercise 8b: Filter by category")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Exercise 8b: Filter by category - {e}")
        failed += 1

    # Test Exercise 8c
    try:
        articles = [
            {"title": "A", "category": "news"},
            {"title": "B", "category": "review"},
            {"title": "C", "category": "news"}
        ]
        result = exercise_8c_count_by_category(articles)
        assert result == {"news": 2, "review": 1}, f"Got {result}"
        print("[PASS] Exercise 8c: Count by category")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Exercise 8c: Count by category - {e}")
        failed += 1

    # Test Exercise 9
    try:
        user = Exercise9User("john", "john@test.com")
        assert user.username == "john"
        assert user.email == "john@test.com"
        assert user.greet() == "Hello, john!"
        assert user.is_valid_email() == True

        user2 = Exercise9User("jane", "invalid")
        assert user2.is_valid_email() == False
        print("[PASS] Exercise 9: User class")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Exercise 9: User class - {e}")
        failed += 1

    # Test Exercise 10
    try:
        raw_data = [
            {"mal_id": 1, "title": "Anime A", "score": 8.5, "episodes": 24},
            {"mal_id": 2, "title": "Anime B", "score": None, "episodes": 12},
            {"mal_id": 3, "title": "Anime C", "score": 9.0, "episodes": None}
        ]
        result = exercise_10_process_anime_data(raw_data)
        expected = [
            {"id": 1, "name": "Anime A", "rating": 8.5, "eps": 24},
            {"id": 2, "name": "Anime B", "rating": 0, "eps": 12},
            {"id": 3, "name": "Anime C", "rating": 9.0, "eps": 0}
        ]
        assert result == expected, f"Got {result}"
        print("[PASS] Exercise 10: Process anime data")
        passed += 1
    except Exception as e:
        print(f"[FAIL] Exercise 10: Process anime data - {e}")
        failed += 1

    # Summary
    print("\n" + "=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed out of {passed + failed}")
    print("=" * 60)

    if failed == 0:
        print("\nCONGRATULATIONS! All exercises complete!")
        print("You now understand the Python basics used in your work.")
    elif passed == 0:
        print("\nAll exercises are waiting for you to solve them.")
        print("Start with Exercise 1 and work your way down.")
        print("Remember: NO AI - struggle through it yourself!")
    else:
        print(f"\nGood progress! {failed} exercises remaining.")
        print("Keep going - each one teaches something important.")

    print()


if __name__ == "__main__":
    run_tests()
