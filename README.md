# Southwark Houses Scraper
This project is part of Project Upwork. This is the job [link](https://www.upwork.com/jobs/~01c861c72b750458ce).

## Job Description
We are looking for a skilled web scraping expert to scrape data of all sold houses (terraced, detached, and semi-detached properties) in Southwark over the last year from the rightmove website. The data should include details such as property address, sale price and any other relevant information. The scraped data should be organized and delivered in a structured format (e.g., CSV or Excel). The ideal candidate should have experience in web scraping, proficiency in Python or any other preferred language for web scraping, and knowledge of using scraping tools such as BeautifulSoup or Scrapy. Attention to detail and the ability to meet deadlines are essential.

https://www.rightmove.co.uk/house-prices-in-Southwark.html?showMapView=showMapView

## Result Schema
- **area** - the Southwark area e.g. Peckam.
- **address** - address of the sold house.
- **type** - property type e.g. Semi-Detached.
- **last_known_price** - the price when it was last sold.
- **last_known_tenure** - the tenure when it was last sold
- **transaction_history** - information of all sales
    - **date_sold**
    - **price**
    - **tenure**

### Example Data (in JSON)
```json
{
    "area": "Bermondsey",
    "address": "7, Surrey Water Road, London, Greater London SE16 5BW",
    "type": "Terraced",
    "last_known_price": "£865,000",
    "last_known_tenure": "Freehold",
    "transaction_history": [
        {
            "date_sold": "27 Mar 2024",
            "price": "£865,000",
            "tenure": "Freehold"
        },
        {
            "date_sold": "8 May 1998",
            "price": "£128,000",
            "tenure": "Freehold"
        }
    ]
}
```

## Evolution
I created 4 [spiders](https://docs.scrapy.org/en/latest/topics/spiders.html):

### [PeckamSpider](./southwark_houses/southwark_houses/spiders/peckham.py)
This was based on my initial understanding of the website.

I discovered 4 actions that I assumed could only be handled by JavaScript:
- accepting or rejecting cookies.
- changing the time frame to the past year for each area.
- expanding the transaction history table for each house.
- moving to the next page for each area.

I decided to use Selenium to perform these actions before handling the html source to Scrapy.

I also limited the scraping to only the [Peckham](https://www.rightmove.co.uk/house-prices/peckham.html?showMapView=showMapView) area to temporarily reduce the problem difficulty. There was no need to think about crawling and I could focus on the Selenium actions and item XPath queries.

### [PeckamNoSeleniumSpider](./southwark_houses/southwark_houses/spiders/peckam_no_selenium.py)
On further exploration of the website, I discovered that it made XHR requests to get the house data. This meant I could request the data directly and get a JSON response. The last 3 JavaScript actions were immediately irrelevant.

The first action (cookies) was irrelevant for this particular spider since I was still dealing only with the [Peckham](https://www.rightmove.co.uk/house-prices/peckham.html?showMapView=showMapView) area. However, it was still important for the final spider where I have to scrape the initial page. Thankfully, the action is non-blocking and the areas can be scraped regardless.

The operation was successful and exploitation of the XHR requests the website makes became my standard for the last 2 spiders.

### [HousesSpider](./southwark_houses/southwark_houses/spiders/houses.py)
I set out to crawl sold houses for all areas in Southwark. I was faced with 2 technical decisions:
- Should I use a basic [Spider](https://docs.scrapy.org/en/latest/topics/spiders.html#scrapy-spider) or the [CrawlSpider](https://docs.scrapy.org/en/latest/topics/spiders.html#crawlspider)? I decided to do both. This spider uses the basic one and the last spider uses CrawlSpider.
- The XHR request URL structure was different from the website URL structure. An example:
    ```python
    # Peckam
    website_url = "https://www.rightmove.co.uk/house-prices/peckham.html?showMapView=showMapView"
    xhr_url = "https://www.rightmove.co.uk/house-prices/result?soldIn=1&filterName=Sold%20in&locationType=REGION&locationId=85428&page=1"
    # locationId will be different for other areas
    ``` 
    I needed a way to extract the IDs from the main page for each area.

The second decision was relatively easy for this spider. The IDs were contained in the class attributes of the `li` tags that contained the area links. For each area, I:
- extracted the ID.
- formatted a url template I had earlier created with the ID.
- created a new request with the new url and a different callback function.

### [HousesCrawlSpider](./southwark_houses/southwark_houses/spiders/houses_crawl.py)
I had to do some more exploration for this one. The [LinkExtractor](https://docs.scrapy.org/en/latest/topics/link-extractors.html) returns a list of URLs to the CrawlSpider [Rule](https://docs.scrapy.org/en/latest/topics/spiders.html#crawling-rules). Therefore, I could not get the `li` tags through the extractor.

Through the docs, I discovered the `process_request` attribute of the Rule class. It accepts a callback function that will be called for every Request extracted. More importantly, the callback function accepts the Response which generated the Request as a second argument. I was able to extract the ID from the Response object and return a new Request.

## Reproducing the Environment
### Requirements
- Python (>= 3.10)
- [Google Chrome](https://www.google.com/chrome/)
- [chromedriver](https://developer.chrome.com/docs/chromedriver/downloads) corresponding to your browser version. The driver executable file must be in `PATH`.
### Setup
- Clone the repository
    ```bash
    git clone https://github.com/toludaree/southwark-houses-scraper.git
    ```
- Create a python virtual environment and activate it. You can use the `venv` package.
    ```bash
    python -m venv .venv

    # Activate
    .venv/Scripts/activate     # Windows
    source .venv/bin/activate  # Linux
    ```
- Install `scrapy`, `selenium` and other associated libraries through `requirements.txt`
    ```bash
    pip install -r requirements.txt
    ```
### Scrape away
- Navigate to the [southwark_houses](./southwark_houses/) directory.
    ```bash
    cd southwark_houses/
    ```
- Choose the spider you want to use. The names of all available spiders are:
    - peckam (uses selenium, not in headless mode yet)
    - peckam_no_selenium
    - houses
    - houses_crawl
- Use `scrapy crawl` to activate spider
    ```bash
    scrapy crawl houses -O houses.json
    ```
    - You can choose JSON, CSV or XML file formats for now.
