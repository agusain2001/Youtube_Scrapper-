from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import HttpRequest
import os
import google_auth_httplib2
import google.oauth2.credentials

# Replace with your API key
YOUTUBE_API_KEY = "AIzaSyCUY8Xh0pTiRxAEALyHXddCshcN4UIgMaU"

def youtube_api_scrape(genre, max_results=500):
    """
    Scrapes YouTube data using the YouTube Data API.
    """
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    all_videos = []
    
    try:
        request = youtube.search().list(
            part='id,snippet',
            q=genre,
            type='video',
            maxResults=max_results,
        )
        response = request.execute()
        
        for search_result in response.get('items', []):
            if search_result['id']['kind'] == 'youtube#video':
                video_id = search_result['id']['videoId']
                
                # Get video details
                video_details_request = youtube.videos().list(part='snippet,contentDetails,statistics,recordingDetails', id=video_id)
                video_details_response = video_details_request.execute()
                
                video_data = {}
                
                if video_details_response.get('items',[]):
                    video = video_details_response['items'][0]
                    
                    video_data['Video URL'] = f"https://www.youtube.com/watch?v={video_id}"
                    video_data['Title'] = video['snippet']['title']
                    video_data['Description'] = video['snippet']['description']
                    video_data['Channel Title'] = video['snippet']['channelTitle']
                    video_data['Keyword Tags'] = video['snippet'].get('tags', '')
                    video_data['YouTube Video Category'] = video['snippet']['categoryId']
                    video_data['Topic Details'] = video['snippet'].get('tags', '') # Topic Details are the same as keyword tags for youtube API
                    video_data['Video Published at'] = video['snippet']['publishedAt']
                    video_data['Video Duration'] = video['contentDetails']['duration']
                    video_data['View Count'] = video['statistics']['viewCount']
                    video_data['Comment Count'] = video['statistics'].get('commentCount', '0')
                    
                    #Check if caption is available
                    caption_request = youtube.captions().list(part='snippet', videoId = video_id)
                    caption_available_response = caption_request.execute()
                    
                    video_data['Captions Available'] =  bool(caption_available_response.get('items', []))
                    
                    #get captions if available
                    if video_data['Captions Available']:
                        try:
                            caption_id = caption_available_response.get('items', [])[0].get('id')
                            caption_download_request = youtube.captions().download(id=caption_id)
                            caption_text = caption_download_request.execute()
                            video_data['Caption Text'] = caption_text
                        except Exception as caption_error:
                             video_data['Caption Text'] = f"Error Downloading Captions: {caption_error}"
                    else:
                        video_data['Caption Text'] = "No Caption"
                        
                    video_data['Location of Recording'] = video['recordingDetails'].get('locationDescription', '') if 'recordingDetails' in video and 'locationDescription' in video['recordingDetails'] else ''
                        
                    all_videos.append(video_data)
                
    except HttpError as e:
         print (f"An HTTP error {e} occurred, please check your API key")
    except Exception as e:
         print (f"An error occurred during the YouTube API process: {e}")
    
    return all_videos