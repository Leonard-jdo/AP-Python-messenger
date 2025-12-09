## Se renseigner pour les classes pour ne pas être perdu
# Les 3 trucs à faire au niveau de json à modifier pour utiliser les classes:

# Le chargement des données
# L'utilisation des données
# La sauvegarde des données


from datetime import datetime
import random
import json

# Définition initiale du serveur avec json
with open("server.json", "r", encoding="utf-8") as f:
    server = json.load(f)

#fonction de sauvegarde du json
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

def get_messageid_available():
    messageid_taken = {message['id'] for message in server['messages']}
    return [i for i in range(50) if i not in messageid_taken]

##Fonctions de navigation


def acceuil():
    login:bool = False
    print('=== Bienvenue dans la messagerie ===')
    print('liste des utilisateurs:')
    for user in server['users']:
        print(user['id'], user['name'])
    print('---------------------------------')
    print('Renseignez votre nom pour vous connecter.')
    print("n: je n'ai pas encore de profil")
    choice = input("Nom (ou 'n'):")
    if choice == 'n':
        ajout_utilisateur()
        acceuil()
    else:
        for user in server['users']:
            if choice == user['name']:
                login = True
                print(f"Connecté en tant que {user['name']}!")
                return(user)
        if not login:
            print("Cet utilisateur n'existe pas, veuillez corriger son nom ou l'ajouter comme nouvel utilisateur")
            acceuil()

    
def menu_principal():
    print('=== Messenger ===')
    print('u. utilisateurs')
    print('c. channels')
    print('x. Leave')
    choice:str = input('Select an option: ')

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
        if userlog['id'] in channel['member_ids']:   #On affiche les channels dans lequel on est seulement
            print('id:',channel['id'],'| name:', channel['name'])
    print('------------------')
    print("c :  accéder à un channel")
    print("a :  ajouter un channel")
    print("r :  revenir au menu principal")
    print('x :  leave')
    choice3 = input('Select an option: ')
    
    if choice3 == 'x':
        return('Bye!')

    elif choice3=='c':
        channelid = int(input("id du channel désiré:"))
        if channelid not in get_channelid_available(): 
            in_channel(channelid)
        else:
            print("Ce groupe n'existe pas")
            channels()
        
        
    elif choice3 == 'e':
        ajout_message()

    elif choice3 == 'a':
        ajout_channel()
        channels()

    elif choice3=='r':
        menu_principal()

    else:
        print('Unknown option')
        channels()

# Fonction de navigation dans un channel

def in_channel(channelid:int):
    for mess in server['messages']: 
            if mess['channel'] == channelid:
                sender_id = mess['sender_id']
                for user in server['users']:
                    if sender_id == user['id']:
                        sender = user['name']
                print(mess['reception_date'], sender, ':', mess['content'])
    print('-----------------------')
    print('e : écrire un message')
    print('r : revenir aux channels')
    choice4 = input('Select an option: ')

    if choice4 == 'r':
        channels()
    
    elif choice4 == 'e':
        ajout_message(channelid)

    else:
        print('Unknown option')
        channels()
    
    channels()


##Fonctions d'ajout

def ajout_utilisateur():
    print("ajout d'un utilisateur")
    newid = random.choice(get_userid_available())
    newname = input("new user name?")
    server['users'].append({'id': newid, 'name': newname})
    save()


def ajout_channel():
    print("ajout d'un channel")
    newname = input("new channel name?")
    newid = random.choice(get_channelid_available())
    newmembers = input("member names (other than you)? Example: user_name1, user_name2, user_name3")
    newmembers = [name.strip() for name in newmembers.split(',')]
    newmembers.append(userlog['name'])
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

def ajout_message(channelid):
    newmessage:str = input('nouveau message:')
    server['messages'].append({"id":random.choice(get_messageid_available()),
                                "reception_date": str(datetime.now().strftime("%d/%m/%Y %H:%M")),
                                "sender_id": userlog['id'],
                                "channel": channelid,
                                "content": newmessage})
    save()
    in_channel(channelid)


#on appelle la fonction globale
userlog = acceuil()
menu_principal()