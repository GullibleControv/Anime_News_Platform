import requests # This is the tool that lets Python surf the web
import json     # This helps Python read the data format

def get_anime_news():
    # 1. THE ENDPOINT: This is the specific URL that gives us news
    url = "https://api.jikan.moe/v4/anime/1/news" 
    # (Note: '1' is the ID for Cowboy Bebop. Later we can change this to get general news)

    print(f"Connecting to {url}...")

    # 2. THE REQUEST: We knock on the door
    response = requests.get(url)

    # 3. THE CHECK: Did the server say "OK" (Status 200)?
    if response.status_code == 200:
        print("Success! Data received.\n")
        
        # 4. THE PARSING: Convert raw text into a Python Dictionary
        data = response.json()
        news_list = data['data'] # The API puts the actual news inside a 'data' box

        # 5. THE LOOP: Go through the first 3 news items
        for news_item in news_list[:3]:
            print("------------------------------------------------")
            print(f"TITLE: {news_item['title']}")
            print(f"DATE:  {news_item['date']}")
            print(f"LINK:  {news_item['url']}")
            print("------------------------------------------------")
            
    else:
        print(f"Failed to connect. Error code: {response.status_code}")

# Run the function
if __name__ == "__main__":
    get_anime_news()