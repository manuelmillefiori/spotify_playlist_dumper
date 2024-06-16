# Autore: Manuel Millefiori

from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

# Definisci gli scope necessari per la creazione di playlist
scope = "playlist-modify-public playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# Funzione per ottenere gli id delle tracce
# della playlist da dumpare (gestendo il limite di 100 tracce imposto dalle API di spotify)
def ottieni_tracce_da_playlist(origin_playlist_id):
   offset = 0
   limit = 100
   track_ids = []

   while True:
      # Ottieni le tracce dalla playlist di origine con l'offset corrente
      origin_tracks = sp.playlist_tracks(origin_playlist_id, offset=offset, limit=limit)['items']

      # Se non ci sono più tracce, esci dal ciclo
      if not origin_tracks:
         break

      # Estrai gli ID delle tracce dalla playlist di origine
      track_ids += [track['track']['id'] for track in origin_tracks if track['track'] is not None and track['track']['id'] is not None]

      # Incrementa l'offset per ottenere le tracce successive
      offset += limit

   return track_ids

def copia_tracce_da_playlist(origin_playlist_url, new_playlist_name, new_playlist_description):
   # Ottieni l'ID della playlist di origine dall'URL
   origin_playlist_id = origin_playlist_url.split('/')[-1]

   try:
      # Ottieni le tracce dalla playlist di origine
      origin_tracks = sp.playlist_tracks(origin_playlist_id)['items']

      # Crea una nuova playlist
      new_playlist = sp.user_playlist_create(sp.me()['id'], new_playlist_name, public=False, collaborative=False, description=new_playlist_description)

      # Estrai gli ID delle tracce dalla playlist di origine
      track_ids = ottieni_tracce_da_playlist(origin_playlist_id)
      
      # Aggiungo le tracce alla nuova playlist dividendole in gruppi di 100 tracce
      for i in range(0, len(track_ids), 100):
         sp.user_playlist_add_tracks(sp.me()['id'], new_playlist['id'], track_ids[i:i+100])

      # Stampa di successo
      print("Dump effettuato correttamente")
   
   except spotipy.SpotifyException as e:
      print(f"Errore Spotify: {e}")
   except Exception as e:
      print(f"Errore sconosciuto: {e}")

# Link playlist da dumpare
playlist_url = input("Inserisci il link della playlist di dumpare: ")

# Nome nuova playlist
new_playlist_name = input("Inserisci il nome della nuova playlist: ")

# Descrizione nuova playlist
new_playlist_description = input("Inserisci la descrizione della nuova playlist(invio per omettere la descrizione): ")

copia_tracce_da_playlist(playlist_url, new_playlist_name, new_playlist_description)