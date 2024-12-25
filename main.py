import os
from scraper import youtube_api_scrape  # Import your scraping functions
from utils import save_to_csv

def main():
    """Main function to run the data scraping process."""
    genre = input("Enter the genre to search for: ")
    
    # Choose to scrape via API or using web scraping.
    # choice = input("Do you want to use the API or web scraping? (api/web): ").lower()

    data = youtube_api_scrape(genre)
    
    if data:
        headers = [
            "Video URL", "Title", "Description", "Channel Title", "Keyword Tags",
            "YouTube Video Category", "Topic Details", "Video Published at",
            "Video Duration", "View Count", "Comment Count", "Captions Available",
            "Caption Text", "Location of Recording"
        ]
        # Construct CSV filepath
        output_dir = 'output'
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{genre.replace(' ', '_')}_youtube_data.csv"
        filepath = os.path.join(output_dir, filename)
        
        save_to_csv(filepath, data, headers)
    else:
        print("No data to save.")
    
if __name__ == "__main__":
    main()