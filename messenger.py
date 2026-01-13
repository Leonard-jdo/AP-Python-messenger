# à faire :
# finir l'interface d'affichage 
#pour résoudre le problème de la création de chnnel et de l'ajout de membres dans ce dernier, on va partir du principe qu'on peut pas rejoindre
#un channel dans lequel on est pas tout seul, il faut que un membre de ce channel nous ajoute (c'est déjà codé ça). 
#Ducoup il faut que lorsqu'on crée un channel, on entre les members qu'on veut y mettre (ça ça doit être fait en local dans les fonctions de navigation)


from datetime import datetime
import random
import json
import requests
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import time

console = Console() # L'objet qui remplace print()


## Définition des classes

class User:
    #Représente un utilisateur du serveur
    def __init__(self, user_id: int, name: str):
        self.id = user_id
        self.name = name

    def __repr__(self) -> str:
        return f'User(name={self.name})'  # Permet d'afficher avec des print


class Channel:
    #Représente un channel du serveur
    def __init__(self, channel_id: int, name: str, member_ids: list[int]):
        self.id = channel_id
        self.name = name
        self.members = member_ids
    
    def __repr__(self) -> str:
        return f'Channel(name={self.name}, members={self.members})'  # Permet d'afficher avec des print


class Message:
    #Représente un message du serveur
    def __init__(self, message_id: int, reception_date: datetime, sender_id: int,  channel: int, content: str):
        self.id = message_id   
        self.date = reception_date
        self.sender = sender_id
        self.channel = channel 
        self.mess = content

class RemoteStorage:
    def __init__(self):
        pass

    def get_users()->list[User]:
        response = requests.get('https://groupe5-python-mines.fr/users')
        data = response.json()
        user_list = [User(user['id'], user['name']) for user in data]
        return user_list


    def create_user(newname:str) -> int:
        newuser = {"name": newname}  
        # On envoie le dictionnaire au serveur
        response = requests.post('https://groupe5-python-mines.fr/users/create', json=newuser).json()
        return response['id']

    
    def get_channels()->list[Channel]:
        response = requests.get('https://groupe5-python-mines.fr/channels')
        data = response.json()
        for channel in data:
            member_list = requests.get(f"https://groupe5-python-mines.fr/channels/{channel['id']}/members").json()
            member_ids = []
            for member in member_list:
                member_ids.append(member['id'])
            channel['member_ids'] = member_ids
        channel_list = [Channel(channel['id'], channel['name'], channel['member_ids'])  for channel in data]
        return channel_list
    

    def create_channel(newname:str) -> int:
        newchannel = {"name": newname}     
        # On envoie le dictionnaire au serveur
        response = requests.post('https://groupe5-python-mines.fr/channels/create', json=newchannel).json()
        return response['id']

    def add_user_channel(user_id:int,channel_id:int):
        user = {'user_id': user_id}
        response = requests.post(f'https://groupe5-python-mines.fr/channels/{channel_id}/join', json = user)
        

## Définition initiale du serveur avec json

with open("server.json", "r", encoding="utf-8") as f:
    server1 = json.load(f)
    server = {"users":[], "channels":[], "messages":[]} # Serveur utilisé en local pour l'utilisation des classes

# On convertit ici le dictionnaire de listes de dictionnaire en un dictionnaire de listes contenant des objet des classes User, Channel et Message
for user1 in server1['users']:
    server["users"].append(User(user1["id"], user1['name']))

for channel1 in server1['channels']:
    server["channels"].append(Channel(channel1["id"], channel1['name'], channel1["member_ids"]))

for message1 in server1['messages']:
    server["messages"].append(Message(message1["id"], message1["reception_date"], message1["sender_id"], message1["channel"], message1["content"]))

server['users'] = RemoteStorage.get_users()
server['channels'] = RemoteStorage.get_channels()

## Fonction de sauvegarde du serveur json

def save():
    # il faut formater à nouveau pour avoir un server adapté au json
    server2={'users':[], 'channels':[], 'messages':[]}

# On doit ici formater server2 pour le json, c'est à dire un dictionnaire de listes de dictionnaires

    for user in server['users']:
        server2['users'].append({"id": user.id, 
                                 "name": user.name})

    for channel in server['channels']:
        server2['channels'].append({"id": channel.id, 
                                    "name": channel.name, 
                                    "member_ids": channel.members})

    for message in server['messages']:
        server2['messages'].append({"id": message.id, 
                                    "reception_date": message.date, 
                                    "sender_id": message.sender, 
                                    "channel": message.channel, 
                                    "content": message.mess})
    with open("server.json", "w", encoding = "utf-8") as f:
        json.dump(server2, f, ensure_ascii=False, indent=2)  # sauvegarde finale


## Fonctions pour l'automatisation du choix des identifiants

def get_userid_available():
    userid_taken = {user.id for user in server['users']}
    return [i for i in range(100) if i not in userid_taken]


def get_channelid_available():
    channelid_taken = {channel.id for channel in server['channels']}
    return [i for i in range(100) if i not in channelid_taken]

def get_messageid_available():
    messageid_taken = {message.id for message in server['messages']}
    return [i for i in range(100) if i not in messageid_taken]


##Fonctions de navigation


def acceuil():
    clear_screen()
    
    # Titre et Bienvenue
    console.print(
        Panel.fit(
            "[bold magenta] Bienvenue sur Python Messenger[/bold magenta]", 
            subtitle="[italic]Connectez-vous pour discuter[/italic]",
            padding=(1, 5),
            border_style="magenta"
        )
    )
    print("")
    # Affichage des profils existants (Tableau)
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("ID", style="dim", width=4)
    table.add_column("Nom d'utilisateur", style="bold green")

    # On remplit le tableau avec vos objets User
    for user in RemoteStorage.get_users():
        table.add_row(str(user.id), user.name)

    console.print(table)
    print("")

    # Instructions
    console.print("[yellow]Entrez votre [bold]Nom[/bold] pour vous connecter.[/yellow]")
    console.print("[dim]Tapez 'n' pour créer un nouveau compte ou 'q' pour quitter.[/dim]")
    
    choice = console.input("[bold blue]Votre choix : [/bold blue]")

    # Cas 1 : Créer un nouveau compte
    if choice == 'n':
        ajout_utilisateur()
        acceuil() # On recharge l'accueil après la création du nouveau compte

    # Cas 2 : Quitter
    elif choice == 'q':
        console.print("[bold red]Fermeture de l'application[/bold red]")
        exit() # Arrête tout le programme proprement

    # Cas 3 : Tentative de connexion (Recherche de l'utilisateur)
    else:
        found_user = None
        
        # On cherche l'utilisateur qui porte ce nom
        for user in RemoteStorage.get_users():
            if user.name == choice:
                found_user = user
                break 
        
        # Si on a trouvé quelqu'un
        if found_user:
            console.print(f"[bold green] Connexion réussie ! Bonjour {found_user.name}.[/bold green]")
            # Petite pause pour que l'utilisateur voie le message de succès
            time.sleep(1.5) 
            return found_user
            
        # Si on n'a trouvé personne
        else:
            console.print(Panel("[bold red] Utilisateur inconnu ![/bold red]", border_style="red"))
            input("Appuyez sur Entrée pour réessayer...")
            acceuil() # On recommence

    
def menu_principal():
    clear_screen()
    print('=== Messenger ===')
    print('u. utilisateurs')
    print('c. channels')
    print('x. Leave')
    choice:str = input('Select an option: ')

    if choice == 'x':
        print("[bold red]Fermeture de l'application[/bold red]")
        exit() # Arrête tout le programme proprement

    elif choice == 'u':
        utilisateurs()
 
    elif choice == 'c':
        channels()
        
    else:
        print('Unknown option')
        menu_principal()


def utilisateurs():
    clear_screen()  # Nettoyage de la console
    
    # Affichage de la liste des utilisateurs
    table = Table(title="[bold blue] Liste des Utilisateurs[/bold blue]", style="magenta")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Nom d'utilisateur", style="green")

    # On utilise l'objet 'User' à travers la liste server['users']
    for user in RemoteStorage.get_users():
        table.add_row(str(user.id), user.name)

    console.print(table)
    
    #Affichage des options (Panneau)
    console.print(
        Panel("[bold green]a[/bold green] : Ajouter un utilisateur\n"
              "[bold red]r[/bold red] : Retour au menu principal\n"
              "[bold yellow]x[/bold yellow] : Quitter l'application",
              title="[bold white] Options[/bold white]",
              border_style="yellow"))
    
    choice = console.input('[bold yellow]Votre choix (a/r/x) : [/]')

    if choice == 'a':
        ajout_utilisateur() 
        # On rappelle utilisateurs() pour afficher le tableau mis à jour
        utilisateurs()
    elif choice == 'r':
        menu_principal() 
    elif choice == 'x':
        console.print("[bold red]Messagerie fermée.[/bold red]")
        exit()
    else:
        # Choix invalide
        console.print("[bold red] Choix invalide. Veuillez réessayer.[/bold red]")
        time.sleep(1)
        utilisateurs() # On rappelle la fonction


def channels():
    clear_screen()
    
    # Création du tableau
    table = Table(title="[bold blue] Vos Salons de Discussion[/bold blue]", style="magenta")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Nom du Salon", style="green")
    table.add_column("Membres", justify="center", style="white")

    # Remplissage du tableau
    # On parcourt tous les salons du serveur
    nb_salons_trouves = 0
    
    for channel in server["channels"]:
        # FILTRE : On n'affiche le salon que si l'ID de l'utilisateur est dans la liste des membres
        # Note : userlog.id est l'ID de l'utilisateur connecté
        if userlog.id in channel.members:   
            nb_salons_trouves += 1
            # On affiche l'ID, le Nom et le nombre de membres total dans ce salon
            table.add_row(
                str(channel.id), 
                channel.name, 
                str(len(channel.members))
            )

    # Si l'utilisateur n'a aucun salon, on affiche un petit message
    if nb_salons_trouves == 0:
        console.print(Panel("[italic yellow]Vous n'êtes membre d'aucun salon pour l'instant.[/italic yellow]"))
    else:
        console.print(table)
    
    # Menu des actions
    console.print(
        Panel(
            "[bold green]c[/bold green] : Choisir un salon\n"
            "[bold blue]a[/bold blue] : Créer un nouveau salon\n"
            "[bold yellow]r[/bold yellow] : Retour au menu principal\n"
            "[bold red]x[/bold red] : Quitter",
            title="[bold white] Actions[/bold white]",
            border_style="yellow"
        )
    )
    
    choice3 = console.input('[bold yellow]Votre choix : [/]')
    
    if choice3 == 'x':
        console.print("[bold red]Bye![/bold red]")
        return

    elif choice3=='c':
        channelid = int(input("id du channel désiré:"))
        if channelid not in get_channelid_available(): 
            in_channel(channelid)
        else:
            print("Ce groupe n'existe pas")
            channels()

    elif choice3 == 'a':
        ajout_channel()
        channels()

    elif choice3 == 'r':
        menu_principal()

    else:
        channels()


# Fonction de navigation dans un channel

def in_channel(channelid: int):
    clear_screen()
    # On va vérifier que le salon existe d'abord
    current_channel = None # On part du principe qu'on n'a rien trouvé pour l'instant
    
    for channel in server['channels']:
        if channel.id == channelid:
            current_channel = channel
            break # On a trouvé, on arrête la boucle inutilement
            
    # Si après la boucle, current_channel est toujours None, c'est que l'ID n'existe pas
    if current_channel is None:
        console.print("[bold red] Salon non trouvé.[/bold red]")
        channels()
        return

    # Créer une table de correspondance ID -> Nom (pour l'affichage des expéditeurs)
    user_names = {user.id: user.name for user in server['users']}

    # Affichage du titre du Salon
    console.print(
        Panel(f"[bold cyan]💬 Bienvenue dans le salon : {current_channel.name}[/bold cyan]",
              border_style="blue",
              padding=(1, 2)))
    
    console.print("-" * 70, style="dim") # Ligne de séparation
    
    # Affichage des messages
    
    messages_found = False
    for mess in server["messages"]: 
        if mess.channel == channelid:
            messages_found = True
            
            sender_name = user_names.get(mess.sender, "Utilisateur Inconnu")
            
            # Vérifier si l'expéditeur est l'utilisateur connecté
            if mess.sender == userlog.id:
                # Mon message (couleur verte, aligné à droite)
                message_style = "[bold green]Moi[/bold green]"
                alignment = "right"
            else:
                # Message des autres (couleur jaune, aligné à gauche)
                message_style = f"[bold yellow]{sender_name}[/bold yellow]"
                alignment = "left"

            # Affichage du message avec la date et le contenu
            console.print(
                f"[{mess.date}] {message_style} : {mess.mess}", 
                justify=alignment
            )

    if not messages_found:
        console.print("[italic dim]Aucun message dans ce salon.[/italic dim]", justify="center")

    console.print("-" * 70, style="dim") # Ligne de séparation
    
    # Menu des options de navigation
    console.print(
        Panel("[bold green]e[/bold green] : Écrire un nouveau message\n"
              "[bold blue]a[/bold blue] : Ajouter un utilisateur à ce channel\n"
              "[bold red]r[/bold red] : Retour aux salons\n"
              "[bold yellow]x[/bold yellow] : Quitter l'application",
              title="[bold white] Actions[/bold white]",
              border_style="yellow"))

    choice = console.input('[bold yellow]Votre choix (e/r/x) : [/]')

    if choice == 'e':
        ajout_message(channelid)
        # On rappelle in_channel pour afficher le nouveau message
        in_channel(channelid) 
    elif choice =='a':
        ajout_user_channel(channelid)
    elif choice == 'r':
        channels() 
    elif choice == 'x':
        console.print("[bold red]Application fermée.[/bold red]")
        return
    else:
        console.print("[bold red] Choix invalide. Veuillez réessayer.[/bold red]")
        in_channel(channelid)



## Fonctions d'ajout

def ajout_utilisateur():
    print("ajout d'un utilisateur")
    newid = random.choice(get_userid_available())
    newname = input("new user name?")
    server['users'].append(User(newid, newname))


def ajout_channel():
    print("ajout d'un channel")
    newname = input("new channel name?")
    RemoteStorage.create_channel(newname)
    print('Channel créé avec succès! Qui voulez vous ajouter à ce channel?')
    time.sleep(3)
    print("--- Liste des utilisateurs disponibles ---")
    for user in RemoteStorage.get_users():
        print(f"[{user.id}] {user.name}")
    print("------------------------------")
    newmembers = input("member ids (other than you)? Example: user_id1, user_id2, user_id3")
    newmembers = [id for id in newmembers.split(',')]
    newmembers.append(userlog.id) #on se rajoute nous même
    existing_ids=[user.id for user in RemoteStorage.get_users()]
    for newmember in newmembers:
        flag = True
        if newmember not in existing_ids:
            print(f'{newmember} is not in the server')
            newmembers.pop(newmember)
            flag = False
        if flag:
            RemoteStorage.add_user_channel(newmember, channel_id)  #A CODER UNE FOIS QUE REMOTESTORAGE.CREATE_CHANNEL RENVOIE UN TRUC ET PAS RIEN
            server['channels'].append(Channel(newid, newname, newmembers))
        save()
    else:
        choice = input("voulez vous ajouter ce(s) utilisateurs (oui/non)?")
        if choice == "oui":
            ajout_utilisateur()
            utilisateurs()
        elif choice == "non":
            channels()

def ajout_message(channelid:int):
    newmessage:str = input('nouveau message:')
    newid = random.choice(get_messageid_available())
    server['messages'].append(Message(newid, str(datetime.now().strftime("%d/%m/%Y %H:%M")), userlog.id, channelid, newmessage))
    save()
    in_channel(channelid)

def ajout_user_channel(channel_id):
    users_list = RemoteStorage.get_users()
    
    print("--- Liste des utilisateurs disponibles ---")
    # On affiche les utilisateurs
    for user in users_list:
        print(f"[{user.id}] {user.name}")
    print("------------------------------")
    flag = True
    while flag:
        choix = input("Entrez l'ID de l'utilisateur à ajouter (ou 'q' pour annuler) : ")
        
        if choix == 'q':
            in_channel(channel_id)
        
        # 4. On vérifie que l'ID existe vraiment dans la liste
        # On compare des strings pour éviter les erreurs de type (int vs str)
        for user in users_list:
            if str(user.id) == choix:
                print(f"Sélectionné : {user.name}")
                user_id = user.id # On renvoie l'ID pour la requête API
                flag = False
            if not flag:
                print("ID introuvable. Veuillez réessayer.")
    RemoteStorage.add_user_channel(user_id, channel_id)
    in_channel(channel_id)


## Fonctions d'affichage

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# on appelle la fonction globale
#userlog = acceuil() #attention: userlog est un objet de la classe user
#menu_principal()