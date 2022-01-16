from player_model import Player
from tinydb import TinyDB, where



"""  TESTS player_model

# crée joueur (données choisies) et enregistre dans players_db
mon_joueur = Player(player_name='EEEE', player_first_name='5ePRENOM',
                    player_birth_date='07/01/2021', player_gender='H',
                    player_ranking=700, player_points_qty=0) 
# pour vérifier et visualiser
print(mon_joueur.__dict__)

# Contenu de players_db avant tests ci-dessous : 
{'p_name': 'AAAAAA', 'p_firstname': 'Jacques', 'p_birthdate': '05/04/1967', 'p_gender': 'H', 'p_rank': 3, 'p_total_points': 0}
{'p_name': 'AAAAAA', 'p_firstname': 'Jacques', 'p_birthdate': '05/04/1967', 'p_gender': 'H', 'p_rank': 3, 'p_total_points': 0}
{'p_name': 'AAAAAA', 'p_firstname': 'Jacques', 'p_birthdate': '05/04/1967', 'p_gender': 'H', 'p_rank': 3, 'p_total_points': 0}
{'p_name': 'BB', 'p_firstname': 'Jean', 'p_birthdate': '04/10/1981', 'p_gender': 'H', 'p_rank': 25, 'p_total_points': 0}
{'p_name': 'CCC', 'p_firstname': 'PRENOM3', 'p_birthdate': '01/01/2001', 'p_gender': 'H', 'p_rank': 5555, 'p_total_points': 0}
{'p_name': 'EEEE', 'p_firstname': '5ePRENOM', 'p_birthdate': '07/01/2021', 'p_gender': 'H', 'p_rank': 700, 'p_total_points': 0}
 avec id = 1 à 6
 
 """

#préalable - déclare table/DB
db = TinyDB('db.json')
Player.players_db = db.table('players_db')

"""
# Test GET/READ  player / player_id (id = inconnu)
  ---------------------------------
# Récupère les données d'un joueur prénommé Jean puis affiche son id [4 = OK]
el = Player.players_db.get(where('p_firstname') == 'Jean')
print(el)
# Affiche son id
print(el.doc_id)


# Affiche tous les joueurs stockés ds DB
  --------------------------------------
for item in Player.players_db:
    print(item.doc_id)


# Test READ_PLAYER pour player_id=5
  ---------------------------------
joueur_id5 = Player.players_db.get(doc_id=5)
print(joueur_id5)


# Test DELETE (remove) player pour doc_id =2 puis 3 (doublons de 1 jacques)
  -------------------------------------------------------------------------
Player.players_db.remove(where(doc_id=2))
Player.players_db.remove(where(doc_id=3))

    # controle post-suppression : 
    for item in Player.players_db:
        print(item)
        print(item.doc_id)


# Test DELETE (remove) plusieurs joueurs à la fois : id 5 à 8
  -----------------------------------------------------------
# au départ :
{'p_id': 1, 'p_name': 'ABADIE', 'p_firstname': 'Jacques', 'p_birthdate': '05/04/1967', 'p_gender': 'H', 'p_rank': 3, 'p_total_points': 0}
{'p_id': 2, 'p_name': 'BALMONT', 'p_firstname': 'Jean', 'p_birthdate': '04/10/1981', 'p_gender': 'H', 'p_rank': 25, 'p_total_points': 0}
{'p_id': 3, 'p_name': 'CHENU', 'p_firstname': 'Jeff', 'p_birthdate': '04/04/1977', 'p_gender': 'H', 'p_rank': 90, 'p_total_points': 0}
{'p_id': 4, 'p_name': 'DEBRIEUX', 'p_firstname': 'Jeremy', 'p_birthdate': '01/08/2003', 'p_gender': 'H', 'p_rank': 15, 'p_total_points': 0}
{'p_id': 1, 'p_name': 'ABADIE', 'p_firstname': 'Jacques', 'p_birthdate': '05/04/1967', 'p_gender': 'H', 'p_rank': 3, 'p_total_points': 0}
{'p_id': 2, 'p_name': 'BALMONT', 'p_firstname': 'Jean', 'p_birthdate': '04/10/1981', 'p_gender': 'H', 'p_rank': 25, 'p_total_points': 0}
{'p_id': 3, 'p_name': 'CHENU', 'p_firstname': 'Jeff', 'p_birthdate': '04/04/1977', 'p_gender': 'H', 'p_rank': 90, 'p_total_points': 0}
{'p_id': 4, 'p_name': 'DEBRIEUX', 'p_firstname': 'Jeremy', 'p_birthdate': '01/08/2003', 'p_gender': 'H', 'p_rank': 15, 'p_total_points': 0}

Player.players_db.remove(doc_ids=[5, 6, 7, 8])
Player.players_db.all()
for item in Player.players_db:
    print(item)

# résultat: 
{'p_id': 1, 'p_name': 'ABADIE', 'p_firstname': 'Jacques', 'p_birthdate': '05/04/1967', 'p_gender': 'H', 'p_rank': 3, 'p_total_points': 0}
{'p_id': 2, 'p_name': 'BALMONT', 'p_firstname': 'Jean', 'p_birthdate': '04/10/1981', 'p_gender': 'H', 'p_rank': 25, 'p_total_points': 0}
{'p_id': 3, 'p_name': 'CHENU', 'p_firstname': 'Jeff', 'p_birthdate': '04/04/1977', 'p_gender': 'H', 'p_rank': 90, 'p_total_points': 0}
{'p_id': 4, 'p_name': 'DEBRIEUX', 'p_firstname': 'Jeremy', 'p_birthdate': '01/08/2003', 'p_gender': 'H', 'p_rank': 15, 'p_total_points': 0}


# Test UPDATE_player_ranking pour player_id = 4, avec ranking : 25 -->44
----------------------------
# joueur concerné : {'p_name': 'BB', 'p_firstname': 'Jean', 
                       'p_birthdate': '04/10/1981', 'p_gender': 'H',
                       'p_rank': 25, 'p_total_points': 0}

# visualisation du joueur player_id = 4
joueur_id4 = Player.players_db.get(doc_id=4)
print(joueur_id4)
                        
# update_ranking (25  devient 44) du joueur player_id = 4
joueur_id4 = Player.players_db.update({'p_rank': 44}, doc_ids=[4])

# visualisation après update :
joueur_id4 = Player.players_db.get(doc_id=4)
print(joueur_id4)
{'p_name': 'BB', 'p_firstname': 'Jean', 'p_birthdate': '04/10/1981',
'p_gender': 'H', 'p_rank': 44, 'p_total_points': 0}


# Test fonction  update_player_ranking avec player_id = 4, ranking : 44 -->34
 ----------------------------------------------------------------------------
# visualisation du joueur player_id = 4
joueur_id4 = Player.players_db.get(doc_id=4)
print(joueur_id4)
                        
# update_ranking (44  devient 34) du joueur player_id = 4
def update_player_ranking(player_ranking, player_id):
    Player.players_db.update({'p_rank': player_ranking}, doc_ids=[player_id])

joueur_id4 = update_player_ranking(34, 4)

#visualisation
joueur_id4 = Player.players_db.get(doc_id=4)
print(joueur_id4)


# Test fonction CREATE_PLAYER()
# -----------------------------
def create_player(player_id, player_name, player_first_name, 
                  player_birth_date, player_gender, player_ranking,
                  player_points_qty):
    # create (and save to a database) a player 
    Player.players_db.insert(
        {
            'p_id': player_id,
            'p_name': player_name,
            'p_firstname': player_first_name,
            'p_birthdate': player_birth_date,
            'p_gender': player_gender,
            'p_rank': player_ranking,
            'p_total_points': player_points_qty
        }
    )
new_player = create_player(1111, 'ABADIE', 'Jacques', '05/04/1967', 'H', 3, 0)

# Récupère l'id du joueur 'ABADIE'
el = Player.players_db.get(where('p_name') == 'ABADIE')
print(el)
# Affiche son id
print(el.doc_id)

# résultat id = 7

# màj de son id (5 sur-identation pour lecture)
  -------------
                    # visualisation du joueur player_id = 7
                    joueur_id7 = Player.players_db.get(doc_id=7)
                    print(joueur_id7)
                                            
                    # update_player_id (1111 devient 7)
                    def update_player_id( player_id, player_name):
                        Player.players_db.update({'p_id': player_id}, where('p_name') == player_name)

                    joueur_id7 = update_player_id(7, 'ABADIE')

                    #visualisation
                    joueur_id7 = Player.players_db.get(doc_id=7)
                    print(joueur_id7)

==================================================================================
==================================================================================
"""
def read_player(player_id):  # 'read' équivaut à 'get' + doit retourner un objet PLAYER (pas uniqmt ID)
    Player.players_db.get(doc_id=player_id)
    return Player()


el = read_player(1)
print(el.__dict__)