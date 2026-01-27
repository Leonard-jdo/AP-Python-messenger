from datetime import datetime
import json
import requests
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import time
import argparse

console = Console() # L'objet qui remplace print()



## Définition des classes d'objet

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

    def __repr__(self) -> str:
        return f'Message({self.mess})'  # Permet d'afficher avec des print


## Définition des classes storage

class RemoteStorage:
    def __init__(self, URL:str):
        self.url = URL

    def get_users(self)->list[User]:
        response = requests.get(f'{self.url}/users')
        data = response.json()
        user_list = [User(user['id'], user['name']) for user in data]
        return user_list


    def create_user(self, newname:str) -> int:
        newuser = {"name": newname}  
        # On envoie le dictionnaire au serveur
        response = requests.post(f'{self.url}/users/create', json=newuser).json()
        return response['id']

    
    def get_channels(self)->list[Channel]:
        response = requests.get(f'{self.url}/channels')
        data = response.json()
        for channel in data:
            member_list = requests.get(f"{self.url}/channels/{channel['id']}/members").json()
            member_ids = []
            for member in member_list:
                member_ids.append(member['id'])
            channel['member_ids'] = member_ids
        channel_list = [Channel(channel['id'], channel['name'], channel['member_ids'])  for channel in data]
        return channel_list
    

    def create_channel(self, newname:str) -> int:
        newchannel = {"name": newname}     
        # On envoie le dictionnaire au serveur
        response = requests.post(f'{self.url}/channels/create', json=newchannel).json()
        return response['id']

    def add_user_channel(self, user_id:int,channel:Channel):
        user = {'user_id': user_id}
        requests.post(f'{self.url}/channels/{channel.id}/join', json = user)

    def get_messages(self):
        response = requests.get(f'{self.url}/messages')
        data = response.json()
        message_list = [Message(message['id'], message['reception_date'], message['sender_id'], message['channel_id'], message['content']) for message in data]
        return message_list


    def post_message(self, user_id:int, channel_id:int, content:str):
        message = {"sender_id": user_id, "content": content}
        response = requests.post(f'{self.url}/channels/{channel_id}/messages/post', json = message).json()
    
class LocalStorage:

    def __init__(self, filename:str):
        self.filename = filename
    
    def load(self) -> dict:

        with open(self.filename, "r", encoding="utf-8") as f:
            server1 = json.load(f)
        server_local = {"users":[], "channels":[], "messages":[]} # Serveur utilisé en local pour l'utilisation des classes

        # On convertit ici le dictionnaire de listes de dictionnaire en un dictionnaire de listes contenant des objet des classes User, Channel et Message
        for user1 in server1['users']:
            server_local["users"].append(User(user1["id"], user1['name']))

        for channel1 in server1['channels']:
            server_local["channels"].append(Channel(channel1["id"], channel1['name'], channel1["member_ids"]))

        for message1 in server1['messages']:
            server_local["messages"].append(Message(message1["id"], datetime.strptime(message1["reception_date"], "%d/%m/%Y %H:%M"), message1["sender_id"], message1["channel"], message1["content"]))
        
        return server_local


    def save(self, newserver:dict):

        # il faut formater à nouveau pour avoir un server adapté au json
        server2={'users':[], 'channels':[], 'messages':[]}

        # On doit ici formater server2 pour le json, c'est à dire un dictionnaire de listes de dictionnaires

        for user in newserver['users']:
            server2['users'].append({"id": user.id, 
                                    "name": user.name})

        for channel in newserver['channels']:
            server2['channels'].append({"id": channel.id, 
                                        "name": channel.name, 
                                        "member_ids": channel.members})

        for message in newserver['messages']:
            server2['messages'].append({"id": message.id, 
                                        "reception_date": message.date.strftime("%d/%m/%Y %H:%M"),
                                        "sender_id": message.sender, 
                                        "channel": message.channel, 
                                        "content": message.mess})
        with open("server.json", "w", encoding = "utf-8") as f:
            json.dump(server2, f, ensure_ascii=False, indent=2)  # sauvegarde finale


    def get_users(self)->list[User]:
        return self.load()['users']


    def create_user(self, newname:str) -> int:
        server = self.load()
        newid = server['users'][-1].id + 1
        server['users'].append(User(newid, newname))
        self.save(server)
        return newid


    def get_channels(self) -> list[Channel]:
        return self.load()['channels']


    def create_channel(self, newname:str, memberids: list[int]) -> int:
        server = self.load()
        newid = server['channels'][-1].id + 1   
        server['channels'].append(Channel(newid, newname, memberids))
        self.save(server)
        return newid


    def get_messages(self):
        return self.load()['messages']
    
    def post_message(self, user_id:int, channel_id:int, content:str):
        server=self.load()
        if len(server['messages']) == 0:
            newid = 1
        else:
            newid = server['messages'][-1].id + 1
        server["messages"].append(Message(newid, datetime.now(), user_id, channel_id, content))
        self.save(server)
    
    def add_user_channel(self, user_id:int, channel:Channel):
        server = self.load()
        for chan in server['channels']:
            if chan.id == channel.id:
                if user_id not in chan.members:   # on ajoute pas un utilisateur déjà présent
                    chan.members.append(user_id)
                break  # on s'arête si on a ajouté qqlun ou si cette personne y était déjà
        self.save(server)
        

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
    for user in storage.get_users():
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
        for user in storage.get_users():
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
    for user in storage.get_users():
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
    
    for channel in storage.get_channels():
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
        exit()

    elif choice3=='c':
        channelid = int(input("id du channel désiré:"))
        # On va vérifier qu'on est dans ce salon
        for channel in storage.get_channels():
            if channel.id == channelid:
                in_channel(channel)
                break
            
    # Si on arrive ici c'est que l'ID n'existe pas ou qu'on est pas dans ce channel
        console.print("[bold red] Salon non trouvé.[/bold red]")
        channels()

    elif choice3 == 'a':
        ajout_channel()
        channels()

    elif choice3 == 'r':
        menu_principal()

    else:
        channels()


def in_channel(channel: Channel):
    clear_screen()
    # Créer une table de correspondance ID -> Nom (pour l'affichage des expéditeurs)
    user_names = {user.id: user.name for user in storage.get_users()}

    # Affichage du titre du Salon
    console.print(
        Panel(f"[bold cyan]💬 Bienvenue dans le salon : {channel.name}[/bold cyan]",
              border_style="blue",
              padding=(1, 2)))
    
    console.print("-" * 70, style="dim") # Ligne de séparation
    
    # Affichage des messages
    
    messages_found = False
    for mess in storage.get_messages():
        if mess.channel == channel.id:
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
        ajout_message(channel)
        # On rappelle in_channel pour afficher le nouveau message
        in_channel(channel) 
    elif choice =='a':
        ajout_user_channel(channel)
    elif choice == 'r':
        channels() 
    elif choice == 'x':
        console.print("[bold red]Application fermée.[/bold red]")
        return
    else:
        console.print("[bold red] Choix invalide. Veuillez réessayer.[/bold red]")
        in_channel(channel)


## Fonctions d'ajout

def ajout_utilisateur():
    print("ajout d'un utilisateur")
    newname = input("new user name?")
    storage.create_user(newname)


def ajout_channel():
    print("ajout d'un channel")
    newname = input("new channel name?")

    print('Channel créé avec succès! Qui voulez vous ajouter à ce channel?')
    time.sleep(2.5)

    print("--- Liste des utilisateurs disponibles ---")
    for user in storage.get_users():
        print(f"[{user.id}] {user.name}")
    print("------------------------------")

    newmembers = input("member ids (other than you)? Example: user_id1, user_id2, user_id3")
    newmembers = [int(id) for id in newmembers.split(',')]
    newmembers.append(userlog.id) #on se rajoute nous même

    existing_ids=[user.id for user in storage.get_users()]
    for newmember in newmembers:
        if newmember not in existing_ids:
            print(f'{newmember} is not in the server')
            newmembers.pop(newmember)
    storage.create_channel(newname, newmembers)
    channels()


def ajout_message(channel:Channel):
    print('rentrez q pour annuler')
    newmessage:str = input('nouveau message:')
    if newmessage != 'q':
        storage.post_message(userlog.id, channel.id, newmessage)
    in_channel(channel)


def ajout_user_channel(channel:Channel):
    
    print("--- Liste des utilisateurs disponibles ---")
    # On affiche les utilisateurs
    for user in storage.get_users():
        print(f"[{user.id}] {user.name}")
    print("------------------------------")


    choix = input("Entrez le nom de l'utilisateur à ajouter (ou 'q' pour annuler) : ")
    
    if choix == 'q':
        in_channel(channel)
    
    # On vérifie que cet utilisateur existe vraiment dans la liste
    for user in storage.get_users():
        if user.name == choix:
            print(f"Sélectionné : {user.name}")
            time.sleep(1)
            storage.add_user_channel(user.id, channel) # On renvoie l'ID pour la fonction dans les classe storage
            in_channel(channel)

    print("utilisateur introuvable. Veuillez réessayer.")
    time.sleep(1.5)
    ajout_user_channel(channel)


## Fonctions d'affichage

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# Lancement et parsing initial
if __name__ == "__main__":
    print('On poursuit la lecture')
    parser = argparse.ArgumentParser(description='Client de messagerie')
        
    # On définit les deux arguments
    parser.add_argument("--local", "-l", help="Nom du fichier JSON pour le mode local")
    parser.add_argument("--remote", "-r", help="URL du serveur pour le mode distant")

    args = parser.parse_args()

    if args.local:
        console.print(f"Démarrage en mode LOCAL sur {args.local}")
        time.sleep(1)
        storage = LocalStorage(args.local)

    elif args.remote:
        console.print(f"Démarrage en mode REMOTE sur {args.remote}")
        time.sleep(1)
        storage = RemoteStorage(args.remote)

    else:
        console.print("Aucun mode spécifié.")
        console.print("Usage: python messenger.py --local filepath.json")
        console.print("   ou: python messenger.py --remote server_url")
        exit()


    # on appelle la fonction globale

    userlog = acceuil() # Userlog est un objet de la classe user
    menu_principal()