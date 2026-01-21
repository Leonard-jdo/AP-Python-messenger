import numpy as np
import pandas as pd
from datetime import datetime
import random
import json

server = {
    'users': [
        {'id': 41, 'name': 'Alice'},
        {'id': 23, 'name': 'Bob'}
    ],
    'channels': [
        {'id': 12, 'name': 'Town square', 'member_ids': [41, 23]}
    ],
    'messages': [
        {
            'id': 18,
            'reception_date': datetime.now(),
            'sender_id': 41,
            'channel': 12,
            'content': 'Hi 👋'
        }
    ]
}
with open("server.json", "r", encoding="utf-8") as f:
            server1 = json.load(f)

date_objet = datetime.now() 

# Conversion en texte (Formatage)
# On réutilise exactement les mêmes codes
#date_str = date_objet.strftime("%d/%m/%Y %H:%M")
#print(date_str, type(date_str))


