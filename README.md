# my.Review

## Installation

To install relevant python dependencies, run `pip install -r requirements.txt`. A list of dependencies can be found in `requirements.txt`.

This project relies on the use of ChromeDriver and PyTesseract. The version of ChromeDriver must match your version of Chrome.

## Usage

Begin by running `courseScraper.py`. This will produce a list of courses saved in `courses.pkl`.

Running `driver.py` will initiate scraping. Two pickle files will be produced; `database4.pkl` will store the scraped course evaluations; `scraped2.pkl` keeps track of courses already scraped.  

## Roadmap

- Incorporate BIOS 2018-2019 reviews
- Generalize parsing to account for different review formats
- Automated updates with new reviews
- Train model to provide robust instructor metric

## Authors

Praveen Balakrishnan, Irina Lee, Rohan Voddhi, William Wang, Derek Zhu

