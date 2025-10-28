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
def messenger():
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
        print('------------------')
        print("a :  ajouter un utilisateur")
        print("r :  revenir au menu principal")
        choice2 = input('Select an option')

        if choice2 == 'a':
            newid = int(input("new user id?"))
            newname = input("new user name?")
            server['users'].append({'id': newid, 'name': newname})
            messenger()

        if choice2 == 'r':
            messenger()

    elif choice == 'c':
        print("===Channel list===")
        for channel in server['channels']:
            print('id:',channel['id'],'| name:', channel['name'])
        print('------------------')
        print("m :  lire les messages")
        print("a :  ajouter un channel")
        print("r :  revenir au menu principal")
        choice3 = input('Select an option')
        
        if choice3=='m':
            groupid = int(input("id du groupe:"))
            for mess in server['messages']: 
                if mess['channel'] == groupid:
                    sender_id = mess['sender_id']
                    for user in server['users']:
                        if sender_id == user['id']:
                            sender = user['name']
                    print(sender,':', mess['content'])
                else:
                    print(groupid, "Ce channel n'existe pas")

        elif choice3 == 'a':
            print('pas encore codé')

        elif choice3=='r':
            messenger()


    else:
        print('Unknown option')

messenger()