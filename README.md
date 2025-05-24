
# Odisha RERA Project Scraper

This Python script scrapes the first 6 projects listed under the **"Projects Registered"** section on the [Odisha RERA website](https://rera.odisha.gov.in/projects/project-list).

It collects detailed information for each project and saves it into a CSV file.

## Features

- Extracts the following details:
  - RERA Regd. No
  - Project Name
  - Promoter Name (Company Name under Promoter Details tab)
  - Address of the Promoter (Registered Office Address)
  - GST No
- Outputs data to a `rera_projects.csv` file
- Uses modern web scraping tools with automated ChromeDriver setup

## Technologies Used

- Python 3.x
- Selenium
- BeautifulSoup (bs4)
- pandas
- webdriver-manager

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/odisha-rera-scraper.git
   cd odisha-rera-scraper

Install dependencies:

bash

pip install -r requirements.txt
Usage
Run the scraper using:

bash
python scraper.py
After execution, the project details will be saved in rera_projects.csv.

Requirements
Create a requirements.txt file containing:

nginx

selenium
beautifulsoup4
pandas
webdriver-manager




