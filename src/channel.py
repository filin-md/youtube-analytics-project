# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
import json
import os

from googleapiclient.discovery import build


# получение YT_API_KEY из переменных окружения с помощью os
api_key: str = os.getenv('YT_API_KEY')
# создать специальный объект для работы с API
youtube_obj = build('youtube', 'v3', developerKey=api_key)

class Channel:
    """Класс для ютуб-канала"""
    youtube = youtube_obj
    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.channel["items"][0]["snippet"]["title"]
        self.description = self.channel["items"][0]["snippet"]["description"]
        self.url = f"https://www.youtube.com/channel/{self.__channel_id}"
        self.subscribers = int(self.channel["items"][0]['statistics']['subscriberCount'])
        self.video_count = self.channel["items"][0]['statistics']['videoCount']
        self.views = self.channel["items"][0]['statistics']['viewCount']

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        return self.subscribers + other.subscribers

    def __sub__(self, other):
        return self.subscribers - other.subscribers

    def __gt__(self, other):
        return self.subscribers > other.subscribers

    def __ge__(self, other):
        return self.subscribers >= other.subscribers

    def __lt__(self, other):
        return self.subscribers < other.subscribers

    def __le__(self, other):
        return self.subscribers <= other.subscribers

    def __eq__(self, other):
        return self.subscribers == other.subscribers

    @classmethod
    def get_service(cls):
        return cls.youtube

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        dict_to_print = json.dumps(self.channel, indent=2, ensure_ascii=False)
        print(dict_to_print)

    def to_json(self, file_name):
        attr_dict = {
            "__channel_id": self.__channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscribers": self.subscribers,
            "video_count": self.video_count,
            "views": self.views,
        }
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(attr_dict, file, ensure_ascii=False)
