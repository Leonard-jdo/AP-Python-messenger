import numpy as np
import pandas as pd
from datetime import datetime
import random

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

taken = {user['id'] for user in server['users']}
userid_available = [i for i in range (50) if i not in taken]
print(random.choice(userid_available))