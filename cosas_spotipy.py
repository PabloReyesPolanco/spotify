import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth
import datetime
import os
import time

def login():
    scope = "user-library-read"
    with open("datos.txt") as f: usuario, cont = map(lambda x: x.rstrip(), f.readlines())
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        scope=scope,
        client_id = usuario,
        client_secret = cont,
        redirect_uri = "http://localhost:8888/callback"))
    return sp

def graficar(df_out,name, type = "streams"):
    sng = df_out[df_out.track_name == name]
    sng.index = sng.start
    ax = sng[type].plot(title = name, grid = True, figsize = (20,6))
    ax.set_xlabel("date")
    ax.set_ylabel(type)

def crear_base():
    weeks = os.listdir("global semanal 2017-2021")
    dfs = []
    for week in weeks:
        start = week[23:33]
        end = week[35:45]
        df  = pd.read_csv("global semanal 2017-2021/" + week)
        df.columns = ["position","track_name","artist","streams","url"]
        df["start"] = start
        df["end"] = end
        df["start"] = pd.to_datetime(df["start"], format='%Y-%m-%d')
        df["end"] = pd.to_datetime(df["end"], format='%Y-%m-%d')
        df["year"] = df.start.map(lambda x: x.year)
        df = df.drop(0)
        df = df[["position","year","start","end","track_name","artist","streams","url"]]
        dfs.append(df)

    df_out = pd.concat(dfs, axis = 0, ignore_index = True)
    df_out.streams = pd.to_numeric(df_out.streams) 
    df_out.position = pd.to_numeric(df_out.position) 
    df_out = df_out.sort_values("start")
    df_out.index = [i for i in range(len(df_out))]
    sp = login()

    df_aux = df_out[["track_name","artist","url"]]

    for i in range(len(df_aux)//100+1):
        inicio = 0 + i*100
        final = min(99+i*100, len(df_aux)-1)
        print(f"{inicio}-{final}/{len(df_aux)}")
        df_aux.loc[inicio:final,"features"] = sp.audio_features(df_aux.loc[inicio:final,"url"].tolist())

    params = [
        "danceability",
        "energy",
        "key",
        "loudness",
        "mode",
        "speechiness",
        "acousticness",
        "instrumentalness",
        "liveness",
        "valence",
        "tempo",
        "duration_ms",
        "time_signature"
        ]

    for p in params:
        df_aux.loc[:,p] = df_aux["features"].map( lambda x: x[p])
    
    tracks = df_aux["track_name"].to_list()
    total = len(tracks)

    for i, track in enumerate(tracks):
        print(f"{i+1}/{total}")
        df_out.loc[df_out["track_name"] == track, params] = df_aux.loc[df_aux["track_name"] == track, params].mode()
    return df_out

def main():
    df_out = crear_base()
    df_out.to_csv("Spotify Weekly.csv", index = False)

if __name__ == "__main__":
    print("comenzando")
    main()
