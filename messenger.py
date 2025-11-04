from datetime import datetime
import random
import json

# Définition initiale du serveur
with open("server.json", "r", encoding="utf-8") as f:
    server = json.load(f)

#fonction de sauvegarde
def save():
    with open("server.json", "w", encoding = "utf-8") as f:
        json.dump(server, f, ensure_ascii=False, indent=2)


#Fonctions pour l'automatisation du choix des identifiants

def get_userid_available():
    userid_taken = {user['id'] for user in server['users']}
    return [i for i in range(50) if i not in userid_taken]


def get_channelid_available():
    channelid_taken = {channel['id'] for channel in server['channels']}
    return [i for i in range(50) if i not in channelid_taken]

##Fonctions de navigation

def menu_principal():
    print('=== Messenger ===')
    print('x. Leave')
    print('u. utilisateurs')
    print('c. channels')
    choice = input('Select an option: ')

    if choice == 'x':
        return('Bye!')

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
        ajout_utilisateur()
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
        return('Bye!')

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
        ajout_channel()
        channels()

    elif choice3=='r':
        menu_principal()

    else:
        print('Unknown option')
        channels()


##Fonctions d'ajout

def ajout_utilisateur():
    newid = random.choice(get_userid_available())
    newname = input("new user name?")
    server['users'].append({'id': newid, 'name': newname})
    save()


def ajout_channel():
    newname = input("new channel name?")
    newid = random.choice(get_channelid_available())
    newmembers = input("member names? Example: user_name1, user_name2, user_name3")
    newmembers = [name.strip() for name in newmembers.split(',')]
    existing_names=[user['name'] for user in server['users']]
    flag=True
    for newmember in newmembers:
        if newmember not in existing_names:
            print(f'{newmember} is not in the server')
            flag=False
    if flag:
        new_member_ids=[]
        for user in server['users']:
            if user['name'] in newmembers:
                new_member_ids.append(user['id'])
        server['channels'].append({'id': newid, 'name': newname, 'member_ids': new_member_ids})
        save()
    else:
        choice = input("voulez vous ajouter ce(s) utilisateurs (oui/non)?")
        if choice == "oui":
            ajout_utilisateur()
            utilisateurs()
        elif choice == "non":
            channels()


#on appelle la fonction globale
menu_principal()