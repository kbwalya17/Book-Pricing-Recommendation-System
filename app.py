
from flask import Flask, render_template, request, abort
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd

app = Flask(__name__)

# Handling requests for favicon.ico
@app.route('/favicon.ico')
def favicon():
    abort(404)  # Return 404 for favicon requests

# Define the book genre URLs
genres = {
    "travel": "https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
    "mystery": [
        "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        "https://books.toscrape.com/catalogue/category/books/mystery_3/page-2.html"
    ],
    "historical_fiction": [
        "https://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html",
        "https://books.toscrape.com/catalogue/category/books/historical-fiction_4/page-2.html"
    ],
    "classics": "https://books.toscrape.com/catalogue/category/books/classics_6/index.html",
    "philosophy": "https://books.toscrape.com/catalogue/category/books/philosophy_7/index.html",
    "romance": [
        "https://books.toscrape.com/catalogue/category/books/romance_8/index.html",
        "https://books.toscrape.com/catalogue/category/books/romance_8/page-2.html"
    ],
    "poetry": "https://books.toscrape.com/catalogue/category/books/poetry_23/index.html",
    "religion": "https://books.toscrape.com/catalogue/category/books/religion_12/index.html",
    "music": "https://books.toscrape.com/catalogue/category/books/music_14/index.html",
    "science_fiction": "https://books.toscrape.com/catalogue/category/books/science-fiction_16/index.html",
    "history": "https://books.toscrape.com/catalogue/category/books/history_32/index.html",
    "politics": "https://books.toscrape.com/catalogue/category/books/politics_48/index.html",
    "spirituality": "https://books.toscrape.com/catalogue/category/books/spirituality_39/index.html",
    "womens_fiction": "https://books.toscrape.com/catalogue/category/books/womens-fiction_9/index.html",
    "children": [
        "https://books.toscrape.com/catalogue/category/books/childrens_11/index.html",
        "https://books.toscrape.com/catalogue/category/books/childrens_11/page-2.html"
    ],
    "fantasy": "https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html",
    "new_adult": "https://books.toscrape.com/catalogue/category/books/new-adult_20/index.html",
    "science": "https://books.toscrape.com/catalogue/category/books/science_22/index.html",
    "humor": "https://books.toscrape.com/catalogue/category/books/humor_30/index.html",
    "psychology": "https://books.toscrape.com/catalogue/category/books/psychology_26/index.html",
    "autobiography": "https://books.toscrape.com/catalogue/category/books/autobiography_27/index.html",
    "business": "https://books.toscrape.com/catalogue/category/books/business_35/index.html",
    "crime": "https://books.toscrape.com/catalogue/category/books/crime_51/index.html",
    "parenting": "https://books.toscrape.com/catalogue/category/books/parenting_28/index.html",
    "suspense": "https://books.toscrape.com/catalogue/category/books/suspense_44/index.html",
    "sports_and_games": "https://books.toscrape.com/catalogue/category/books/sports-and-games_17/index.html",
    "thriller": "https://books.toscrape.com/catalogue/category/books/thriller_37/index.html",
    "health": "https://books.toscrape.com/catalogue/category/books/health_47/index.html",
    "academic": "https://books.toscrape.com/catalogue/category/books/academic_40/index.html",
    "self_help": "https://books.toscrape.com/catalogue/category/books/self-help_41/index.html"
}


# Function to scrape prices and titles from the book pages
def scrape_books(url):
    print(f"Scraping URL: {url}")
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    books = []
    for book in soup.find_all('article', class_='product_pod'):
        title = book.find('h3').find('a').get('title')
        price = book.find('p', class_='price_color').text.strip('Â')
        try:
            price = float(price[1:])  # Removing currency symbol and converting to float
            books.append((title, price))
        except ValueError:
            continue
    print(f"Found books: {books}")
    return books

# Function to find the closest book price to the user's input
def find_closest_book(genre_urls, target_price):
    closest_book = None
    closest_price = None
    closest_title = None
    for url in genre_urls:
        books = scrape_books(url)
        for title, price in books:
            if closest_price is None or abs(price - target_price) < abs(closest_price - target_price):
                closest_price = price
                closest_title = title
                closest_book = url  # Store the book URL for reference
    return closest_book, closest_title, closest_price

# Main route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Get user input
            user_price = float(request.form['price'])
            selected_genres = request.form.getlist("genres")

            # Ensure genres are selected
            if not selected_genres:
                print("No genres selected.")
                return render_template('index.html', genres=genres.keys(), error="Please select at least one genre.")

            print(f"User price: {user_price}")
            print(f"Selected genres: {selected_genres}")

            # Calculate average prices and find the closest book
            average_prices = {}
            closest_genre = None
            closest_price = None
            closest_book_url = None
            closest_title = None

            for genre in selected_genres:
                genre_urls = genres[genre] if isinstance(genres[genre], list) else [genres[genre]]
                prices = []
                for url in genre_urls:
                    books = scrape_books(url)
                    prices.extend([price for title, price in books])

                # Calculate the average price for the genre
                average_prices[genre] = sum(prices) / len(prices) if prices else 0

            # Find the genre with the closest average price
            closest_genre = min(average_prices, key=lambda g: abs(average_prices[g] - user_price))
            closest_price = average_prices[closest_genre]

            # Find the book closest to the user's price in the closest genre
            closest_book_url, closest_title, closest_book_price = find_closest_book(
                genres[closest_genre] if isinstance(genres[closest_genre], list) else [genres[closest_genre]],
                user_price
            )

            return render_template(
                'result.html',
                selected_genres=selected_genres,
                average_prices=average_prices,
                closest_genre=closest_genre,
                closest_price=closest_price,
                user_price=user_price,
                closest_book=closest_book_url,
                closest_title=closest_title,
                closest_book_price=closest_book_price
            )
        except ValueError:
            return render_template('index.html', genres=genres.keys(), error="Please enter a valid numeric price.")
    return render_template('index.html', genres=genres.keys())

if __name__ == '__main__':
    app.run(debug=True)