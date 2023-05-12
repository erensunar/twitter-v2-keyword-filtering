# Twitter API v2 Basic Tweet Scraper

This project is designed for Twitter API v2 Basic package or version. Users without full archive access can scrape tweets up to API limits using this script. All scraped and filtered tweets are saved to an Excel file.

## Installation

1. Install the requirements:

    ```
    pip install -r requirements.txt
    ```

2. Create your `.env` file and add your Twitter API keys:

    ```
    API_KEY=your_api_key
    API_SECRET=your_api_secret_key
    ACCESS_TOKEN=your_access_token
    ACCESS_TOKEN_SECRET=your_access_token_secret
    BEARER_TOKEN=your_bearer_token
    ```

## Usage

To run the program, enter the following command into the terminal:

    ```
    python3 scraper.py username keyword1,keyword2,keyword3 tweet_count
    ```

- `username`: the Twitter handle you want to scrape tweets from (e.g. elonmusk)
- `keywords`: a list of keywords to filter the tweets (separated by commas)
- `tweet_count`: the number of tweets you want to scrape

Example usage:

    ```
    python scraper.py elonmusk woman,women,"gender equality" 250
    ```

## License

This project is available under the [MIT License](LICENSE). Feel free to use and modify it for your own purposes.
