import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time
import re
import random
import json

def get_video_urls(genre, num_videos=500):
    """Searches YouTube for videos of a specific genre and returns a list of URLs."""
    urls = []
    page = 1
    options = Options()
    options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--disable-gpu")  # Disable GPU acceleration (optional)
    driver_path = ChromeDriverManager().install()
    driver = webdriver.Chrome(options=options)

    while len(urls) < num_videos:
        search_url = f"https://www.youtube.com/results?search_query={genre.replace(' ', '+')}&page={page}"
        driver.get(search_url)
        time.sleep(random.uniform(2,4))  # Adjust as needed
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        video_results = soup.find_all('ytd-video-renderer', class_='style-scope ytd-item-section-renderer')
        
        if not video_results:
             break
        
        for video_result in video_results:
           link = video_result.find('a', id='thumbnail')
           if link and 'href' in link.attrs: # Check if the 'href' attribute exists
              video_url = "https://www.youtube.com" + link["href"]
              if video_url not in urls:
                    urls.append(video_url)
              if len(urls) >= num_videos:
                  break

        page += 1

    driver.quit()
    return urls[:num_videos]


def extract_video_data(video_url):
    """Extracts data from a YouTube video page."""
    video_data = {}
    
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(options=options)
        
        driver.get(video_url)
        time.sleep(random.uniform(2,4))

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        video_data['Video URL'] = video_url
        video_data['Title'] = soup.find("h1", class_="title").text.strip()
        video_data['Description'] = soup.find("div", id="description").text.strip() if soup.find("div", id="description") else ''
        video_data['Channel Title'] = soup.find("yt-formatted-string", class_="ytd-channel-name").text.strip()
        keywords = soup.find('meta', attrs={'name': 'keywords'})
        video_data['Keyword Tags'] = keywords['content'] if keywords else ''
        video_data['YouTube Video Category'] = soup.find('meta', attrs={'itemprop': 'genre'})['content'] if soup.find('meta', attrs={'itemprop': 'genre'}) else ''
        topic_details = soup.find('meta', attrs={'itemprop': 'keywords'})
        video_data['Topic Details'] = topic_details['content'] if topic_details else ''

        #Extracting video published date from string like "Published Nov 11, 2023"
        try:
            pub_date_str = soup.find('span', class_='date').text.strip()
            match = re.search(r'Published (.+)', pub_date_str)
            if match:
               video_data['Video Published at'] = match.group(1)
            else:
              video_data['Video Published at'] = ''
        except:
            video_data['Video Published at'] = ''

        duration = soup.find('meta', attrs={'itemprop': 'duration'})
        video_data['Video Duration'] = duration['content'] if duration else ''
        view_count = soup.find('meta', attrs={'itemprop': 'interactionCount'})
        video_data['View Count'] = view_count['content'] if view_count else ''
        comment_count = soup.find('yt-formatted-string', id='count')
        video_data['Comment Count'] = comment_count.text.strip() if comment_count else ''
        captions_track = soup.find('link', attrs={'itemprop': 'caption'})
        video_data['Captions Available'] = "true" if captions_track else "false"

        video_data['Caption Text'] = ''
        if video_data['Captions Available'] == 'true':
            caption_url = captions_track.get('href')
            caption_text = extract_captions(caption_url)
            video_data['Caption Text'] = caption_text
        location = soup.find('yt-formatted-string',class_="ytd-video-primary-info-renderer",id="location")
        video_data['Location of Recording'] = location.text.strip() if location else ''
        driver.quit()
    except Exception as e:
       print(f"Error during data extraction for {video_url}: {e}")
       driver.quit()
       video_data = {} # Return an empty dictionary for error cases
       
    return video_data

def extract_captions(caption_url):
  """Extracts captions from a .vtt file."""
  try:
     response = requests.get(caption_url)
     response.raise_for_status()
     vtt_content = response.text
     caption_text = ""
     for line in vtt_content.splitlines():
        if not line.startswith('WEBVTT') and not line.strip().isdigit() and "-->" not in line:
              caption_text += line.strip() + " "
     return caption_text.strip()
  except Exception as e:
      print(f"Error while fetching/processing captions: {e}")
      return ''


def write_to_csv(data, filename="youtube_data.csv"):
    """Writes the extracted data to a CSV file."""
    if not data:
        print("No data to write to CSV.")
        return
    header = data[0].keys() if data else []
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        writer.writerows(data)
    print(f"Data written to {filename}")


def main(genre):
    """Main function to orchestrate data scraping."""
    video_urls = get_video_urls(genre)
    all_data = []

    for i, url in enumerate(video_urls):
        print(f"Extracting data for video {i + 1}/{len(video_urls)}")
        video_data = extract_video_data(url)
        if video_data:
           all_data.append(video_data)
        time.sleep(2)  # Be respectful to YouTube's servers
   
    write_to_csv(all_data)

if __name__ == "__main__":
    genre = input("Enter the genre to search for: ")
    main(genre)