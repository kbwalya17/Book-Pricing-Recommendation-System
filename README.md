# Bookstore Pricing and Recommendation System

This project is a web-based tool designed to help users find books within their budget. By comparing prices across various user preferred genres, the system identifies the most affordable options and provides direct links to purchase them. Built with Python and Flask, the application scrapes data from the [Books to Scrape](https://books.toscrape.com) website and provides recommendations based on user inputs.

## Key Features:
- **Genre Selection**: Users can choose from a variety of genres including Travel, Mystery, Historical Fiction, Romance, Science Fiction, and many more.
- **Price Comparison**: Users enter a price range, and the app compares their budget to the average price of books in the selected genre.
- **Closest Book Match**: The system identifies the book that is closest to the user's specified price range and provides the title, price, and a direct link to purchase the book on the bookstore website.
- **Dynamic Data**: Book data (title, price, and URL) is scraped directly from the Books to Scrape website. The data is saved in Excel sheets for easy future access.
- **Excel File Management**: The system automatically saves or updates genre-specific Excel sheets that store the book data, so users don’t have to scrape data repeatedly.

## Technologies Used:
- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS
- **Web Scraping**: BeautifulSoup (bs4)
- **Data Storage**: Excel sheets (openpyxl)
- **Additional Libraries**: Requests, Pandas

## How It Works:
1. **User Input**: The user selects a book genre and inputs their budget.
2. **Genre Data Management**: 
    - If an Excel sheet containing book data for the chosen genre already exists, the app will load the data from the sheet.
    - If no data is found, the app scrapes the latest book information for that genre from the Books to Scrape website and stores it in a new Excel sheet.
3. **Price Matching**: The system compares the user's budget against the average price of books in the selected or preferred genre.
4. **Closest Book**: The system finds the book with the closest price to the user's budget and displays the title, price, and a direct link to the bookstore website where the book can be purchased.
5. **User Interface**: The system features a simple web interface where users can interact with the application and view their results.

## Example Use Case:
A user selects the "Historical Fiction" genre and enters a budget of £45. The app finds the book that is priced closest to their budget, displays its title (e.g., **"Glory over Everything: Beyond The Kitchen House"**), shows the price (£45.84), and provides a direct link to the book's page on the bookstore website.

## Concept Expansion for Real Estate:
The same concept of this project can be adapted for real estate applications, helping users find affordable places to live based on rental prices. By fetching data from real estate websites, users can enter their area preferences and budget, and the system will find the most affordable areas and exact rental properties that match their criteria. 

### Steps:
1. **User Input**: Users input their preferred area and budget.
2. **Scraping Real Estate Data**: The system scrapes rental listings from real estate websites based on the user's preferences.
3. **Price Comparison**: The system compares the rental prices in the selected areas with the user's budget.
4. **Affordable Area Identification**: The system identifies the most affordable area and the exact rental properties that fit within the user’s budget.
5. **Results Display**: The user is presented with a list of affordable rental options and links to the listings.

