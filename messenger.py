from datetime import datetime

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

print('=== Messenger ===')
print('x. Leave')
print('y. utilisateurs')
print('z. channels')
choice = input('Select an option: ')
if choice == 'x':
    print('Bye!')
if choice == 'y':
    print(server['users'])
if choice == 'z':
    print(server['channels'])
else:
    print('Unknown option:', choice)
