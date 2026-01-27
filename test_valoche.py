from messenger import User, Channel, Message
from messenger import LocalStorage
import json


class TestLocalStorage:
    def test_get_user(self):
        storage = LocalStorage('server.json')
        for user in storage.get_users():
            assert type(user) == User
    def test_get_channel(self):
        storage = LocalStorage('server.json')
        for channel in storage.get_channels():
            assert type(channel) == Channel

    def test_post_message(self):
        test = {"users": [{"id" : 1, "name" : "test"}],"channels" :[{"id": 1,"name": "Groupe Test","member_ids": [1]}], "messages" : []}
        fichier_fictif = "fichier_test.json"
        with open(fichier_fictif, "w", encoding = "utf-8") as f:
            f.write(json.dumps(test))
        storage = LocalStorage(fichier_fictif)
        storage.post_message(1,1,'Test')
        message_ecrit = 'Test'
        for message in storage.get_messages():
            assert message.mess == message_ecrit

        


