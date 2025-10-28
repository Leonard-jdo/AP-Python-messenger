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
print('u. utilisateurs')
print('c. channels')
choice = input('Select an option: ')

if choice == 'x':
    print('Bye!')

elif choice == 'u':
    print("===User list===")
    for user in server['users']:
        print(user['id'], user['name'])

elif choice == 'c':
    print("===Channel list===")
    for channel in server['channels']:
        print(channel['id'], channel['name'])
    
    groupid = int(input("Pour voir les messages d'un groupe, donnez son id:"))
    for mess in server['messages']: 
        if mess['channel'] == groupid:
            print(mess['content'])

else:
    print('Unknown option:', choice)