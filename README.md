# YouTube Data Scraper

This Python project is a tool to scrape data from YouTube videos based on a specified genre. It uses either the YouTube Data API v3 or web scraping techniques (via Selenium) to extract video information and save it into a CSV file.

## Features

-   **Dynamic Genre Input:** Allows the user to specify the genre of videos to search for.
-   **Data Extraction:** Extracts various data points from YouTube videos such as:
    -   Video URL
    -   Title
    -   Description
    -   Channel Title
    -   Keyword Tags
    -   YouTube Video Category
    -   Topic Details
    -   Video Published at
    -   Video Duration
    -   View Count
    -   Comment Count
    -   Captions Available (True/False)
    -   Caption Text (snippet if using the API or full if using Selenium).
    - Location of Recording.
-   **Output to CSV:** Saves the extracted data in a comma-separated values file for further analysis.
-   **Method Choice:** Offers the user the choice between using the YouTube Data API or web scraping for data extraction.
-   **Pagination:** Retrieves up to 500 video entries, utilizing pagination when using the API.
-   **API Key or OAuth Authentication (Optional):** You can use an API key or OAuth 2.0 authentication with your code.
-   **Web Scraping:** if using web scraping, selenium is used for dynamic pages.

## Project Structure


## Setup

1.  **Clone the Repository:**

    ```bash
    git clone <repository_url>
    cd data_scraping_project
    ```
    
2. **Install Chrome Driver:**
    * Since the code uses selenium, a compatible version of Chrome Driver should be installed for it to work correctly. If it is your first time using the application, then the webdriver library will automatically download a compatible version. Otherwise, check the chrome version you have installed and download the chrome driver corresponding to your version from [here](https://chromedriver.chromium.org/downloads).
3.  **Install Dependencies:** Make sure you have Python installed, and then use `pip` to install the required libraries:

    ```bash
    pip install -r requirements.txt
    ```

4.  **YouTube Data API Setup (if you are using the API method):**

    *   Go to the [Google Cloud Console](https://console.cloud.google.com/) and create or select a project.
    *   Enable the YouTube Data API v3 for your project.
    *   **Option 1 (API Key):** Obtain an API key. Then, replace `"YOUR_YOUTUBE_API_KEY"` in `scraper.py` with your actual key.
    *   **Option 2 (OAuth 2.0):** If you want to use OAuth 2.0. You will need to generate OAuth 2.0 client IDs (typically for a web application). This involves setting up a consent screen and authorized redirect URIs and downloading the `credentials.json` file in your `data_scraping_project` directory.
    
5.  **Web Scraping:**
    * No further setup is required if you are using this scraping approach.

## Usage

1.  **Run the Script:**

    ```bash
    python main.py
    ```

2.  **Provide Input:**
    *   When prompted, enter the genre you want to search for on YouTube.
    *   When prompted, select the method for scraping:
        * Type `api` to use the YouTube Data API method.
        * Type `web` to use the Selenium web scraping method.

3.  **Output:** A CSV file containing the scraped data will be generated in the `output` folder (or root folder if this doesn't exist). The file name will follow the format `genre_youtube_data.csv`.

## Important Considerations

*   **API Quota:** If you are using the API method, be aware that the YouTube Data API has daily usage limits. Check your quota usage in the Google Cloud Console.
*   **Web Scraping:** If using web scraping, keep in mind that changes to YouTube's website can break the scraper. Also, this method is slower and uses more resources than the API method.
*   **API Key vs. OAuth 2.0:** If you use the API, using OAuth 2.0, will give access to extra features, like the ability to download captions (although the default API quota is enough to test the other features). If using only API Keys, the application will only retrieve a snippet of the captions text.
*   **Error Handling:** The application includes some basic error handling, but you may see HTTP errors or connection problems depending on your environment.
*   **Rate Limiting:** The script incorporates `time.sleep` to prevent your IP from getting rate-limited or blocked when using the API or scraping. Please do not remove these sleeps, as this might get your IP address blocked or banned.

## Disclaimer

This code is for educational purposes and you should always respect the Terms of Service of the platform you are scraping, and you should check if your API use is aligned with the terms of service, and policy for the site owner.

## Support

For any issues, bugs, or feature requests please, contact the code author and they will assist.

This README.md should give users a good starting point to understand your project. Let me know if you have any other changes you'd like to make!
