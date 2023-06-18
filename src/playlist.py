from datetime import timedelta
import isodate

from src.channel import youtube_obj

class PlayList:

    def __init__(self, id):
        self.id = id

        playlist_response = youtube_obj.playlists().list(part='snippet', id=self.id).execute()

        playlist_videos = youtube_obj.playlistItems().list(playlistId=self.id,
                                                           part='contentDetails',
                                                           maxResults=50,
                                                           ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        self.video_response = youtube_obj.videos().list(part='contentDetails,statistics',
                                                   id=','.join(video_ids)
                                                   ).execute()

        self.title = playlist_response["items"][0]["snippet"]["title"]
        self.url = f"https://www.youtube.com/playlist?list={self.id}"

    @property
    def total_duration(self):
        total_duration = timedelta()
        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration


    def show_best_video(self):

        max_likes = 0
        max_likes_video_id = ""

        for video in self.video_response["items"]:
            if int(video["statistics"]["likeCount"]) > max_likes:
                max_likes = int(video["statistics"]["likeCount"])
                max_likes_video_id = video["id"]
        return f"https://youtu.be/{max_likes_video_id}"
