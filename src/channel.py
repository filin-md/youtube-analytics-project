# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    # получение YT_API_KEY из переменных окружения с помощью os
    api_key: str = os.getenv('YT_API_KEY')


    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.channel["items"][0]["snippet"]["title"]
        self.description = self.channel["items"][0]["snippet"]["description"]
        self.url = f"https://www.youtube.com/channel/{self.__channel_id}"
        self.subscribers = self.channel["items"][0]['statistics']['subscriberCount']
        self.video_count = self.channel["items"][0]['statistics']['videoCount']
        self.views = self.channel["items"][0]['statistics']['viewCount']

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
        with open(file_name, "w") as file:
            json.dump(self.channel, file)

