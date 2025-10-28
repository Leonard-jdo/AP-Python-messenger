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
def menu_principal():
    print('=== Messenger ===')
    print('x. Leave')
    print('u. utilisateurs')
    print('c. channels')
    choice = input('Select an option: ')

    if choice == 'x':
        print('Bye!')

    elif choice == 'u':
        utilisateurs()
 
    elif choice == 'c':
        channels()
        

    else:
        print('Unknown option')


def utilisateurs():
    print("===User list===")
    for user in server['users']:
        print(user['id'], user['name'])
    print('------------------')
    print("a :  ajouter un utilisateur")
    print("r :  revenir au menu principal")
    choice2 = input('Select an option: ')

    if choice2 == 'a':
        newid = int(input("new user id?"))
        newname = input("new user name?")
        server['users'].append({'id': newid, 'name': newname})
        utilisateurs()

    if choice2 == 'r':
        menu_principal()

    else:
        print('Unknown option')
        utilisateurs()

def channels():
    print("===Channel list===")
    for channel in server['channels']:
        print('id:',channel['id'],'| name:', channel['name'])
    print('------------------')
    print("m :  lire les messages")
    print("a :  ajouter un channel")
    print("r :  revenir au menu principal")
    print('x :  leave')
    choice3 = input('Select an option: ')
    
    if choice3 == 'x':
        print('Bye!')

    elif choice3=='m':
        groupid = int(input("id du groupe:"))
        for mess in server['messages']: 
            if mess['channel'] == groupid:
                sender_id = mess['sender_id']
                for user in server['users']:
                    if sender_id == user['id']:
                        sender = user['name']
                print(sender,':', mess['content'])
        channels()

    elif choice3 == 'a':
        print('pas encore codé ;)')

    elif choice3=='r':
        menu_principal()

    else:
        print('Unknown option')
        channels()




menu_principal()