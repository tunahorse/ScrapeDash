# ScrapeDash

This is a Python Flask application designed for web scraping data and saving/managing scraped data as txt. This is meant as a simple solution, to keep track of scraped data. I used text as a catch-all, in my situation I don't care about the formatting. 

## Features

- **Scraping Data**: Utilizes BeautifulSoup and Playwright to scrape data from given URLs.
- **Manual Data Input**: Supports file uploads and text input for manual data entry.
- **Data Organization**: Stores scraped data in organized directories.
- **Data Management Dashboard**: Provides a dashboard for viewing and managing stored data.

## Prerequisites

- Python 3.x
- Flask
- BeautifulSoup
- Playwright

## Installation

1. **Clone the repository**:
2. **Install required dependencies**:
3. You really only need BS and PW.


2. **Access the application**:
Open your web browser and navigate to `http://localhost:5000` to start using the application.

## App Structure

- `app.py`: The main Flask application file.
- `templates/`: Directory containing HTML templates.
- `input.html`: Template for inputting a URL to scrape.
- `dashboard.html`: Template for the data dashboard.
- `data.html`: Template for displaying data files in a directory.
- `manual_input.html`: Template for manually inputting data.
- `view_data.html`: Template for viewing the contents of a data file.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

MIT




### Project Screenshots

### Input Form
![Input Form Screenshot](https://github.com/tunahorse/ScrapeDash/blob/main/input.png "Input Form")

### Dashboard View
![Dashboard Screenshot](https://github.com/tunahorse/ScrapeDash/blob/main/dash.png "Dashboard")

### Scraped List
![List of Scraped Items Screenshot](https://github.com/tunahorse/ScrapeDash/blob/main/scraped_list.png "Scraped List")

### Scraped Text
![Scraped Text Screenshot](https://github.com/tunahorse/ScrapeDash/blob/main/scraped_text.png "Scraped Text")
