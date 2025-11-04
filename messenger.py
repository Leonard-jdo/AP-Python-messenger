from datetime import datetime
import random

#Définition initiale du serveur
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

##Définitions initiales des id

#id des membres
userid_taken = {user['id'] for user in server['users']}
userid_available = [i for i in range (50) if i not in userid_taken]

#id des channels
channelid_taken = {channel['id'] for channel in server['channels']}
channelid_available = [i for i in range (50) if i not in channelid_taken]



##Fonctions de navigation

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
        menu_principal()


def utilisateurs():
    print("===User list===")
    for user in server['users']:
        print(user['id'], user['name'])
    print('------------------')
    print("a :  ajouter un utilisateur")
    print("r :  revenir au menu principal")
    choice2 = input('Select an option: ')

    if choice2 == 'a':
        newid = random.choice(userid_available)
        newname = input("new user name?")
        server['users'].append({'id': newid, 'name': newname})
        userid_available.pop(newid)
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
        print()
        channels()

    elif choice3 == 'a':
        newname = input("new channel name?")
        newid = random.choice(channelid_available)
        newmembers = input("member names? Example: user_name1, user_name2, user_name3")
        newmembers = [name.strip() for name in newmembers.split(',')]
        server['channels'].append({'id': newid, 'name': newname, 'member_ids': []})
        channelid_available.pop(newid)
        channels()

    elif choice3=='r':
        menu_principal()

    else:
        print('Unknown option')
        channels()



#on appelle la fonction globale
menu_principal()