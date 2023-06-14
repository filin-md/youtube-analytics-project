from src.channel import youtube_obj


class Video:
    def __init__(self, video_id):
        self.video_id = video_id
        video_response = youtube_obj.videos().list(part='snippet,statistics,contentDetails,topicDetails', id=video_id).execute()

        self.title = video_response['items'][0]['snippet']['title']
        self.view_count = video_response['items'][0]['statistics']['viewCount']
        self.like_count = video_response['items'][0]['statistics']['likeCount']
        self.url = f'https://youtu.be/{self.video_id}'

    def __str__(self):
        return self.title

class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

