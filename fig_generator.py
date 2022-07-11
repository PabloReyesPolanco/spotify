import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.dates as md
from scipy.stats import pearsonr #calculate correlation coefficient
from scipy import stats
import calendar

spotify_green = (29/255, 185/255, 84/255, 1)
spotify_black = (25/255, 20/255, 20/255, 1)
spotify_blue = (85/255, 156/255, 242/255, 1)
spotify_purple = (65/255, 0/255, 245/255, 1)
spotify_white = (1,1,1,1)

spotify_palette = [
                spotify_green,
                spotify_black,
                spotify_blue,
                spotify_purple,
                spotify_white
                ]
palette = sns.color_palette(spotify_palette, 5)

aa =  ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_s']
a2 = ['danceability', 'energy', 'loudness', 'speechiness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_s']

def heatmap(df, nombre, vars = aa):
    df = df[vars]
    cormat = df.corr()
    f, ax = plt.subplots(figsize=(10,8))
    sns.heatmap(cormat, vmax= .85, square=True)
    k = 10
    cols = cormat.nlargest(k,vars[2])[vars[2]].index
    cm = np.corrcoef(df[cols].values.T)
    sns.set(font_scale=1.25)
    hm = sns.heatmap(cm, cbar=False, annot=True, square=True, fmt=".2f", annot_kws={"size": 10}, yticklabels=cols.values, xticklabels=cols.values)
    # plt.show()
    plt.savefig(nombre, transparent = False)
    plt.close()

def pairplot(df, vars, nombre):
    sns.pairplot(df[vars]) # ,"valence"
    # plt.show()
    plt.savefig(nombre, transparent = False)
    plt.close()

def histogram(df, var, nombre):
    #set figure
    f, ax = plt.subplots(1,1, figsize = (10,8))#graph histogram
    plt.hist(df[var], bins=10, alpha=0.75, color = spotify_green , label=var.title())
    plt.legend(loc='upper right')#set title & axis titles
    ax.set_title(f'{var.title()} Histogram', fontsize=20)
    ax.set_xlabel(var.title())
    ax.set_ylabel('Frequency')#set x & y ranges
    # plt.xlim(0,1)
    # plt.ylim(0, len())
    # plt.show()
    plt.savefig(nombre, transparent = False)
    plt.close()

def reg_plot(df, var1, var2, nombre):
    f, ax = plt.subplots(figsize=(10,8))
    corr = pearsonr(df[var1], df[var2])
    corr = [np.round(c, 2) for c in corr] #add the coefficient to your graph
    text = 'r=%s' % (corr[0])
    sns.regplot(x=var1, y=var2, data=df, color = spotify_green)
    ax.legend([text])
    plt.savefig(nombre, transparent = False)
    plt.close()

def time_series(data, var, nombre ,trendline = False, rolling_average = False, IC = False,rolling_size = 4, aux = True):
    fig, ax = plt.subplots(figsize = (16,10))
    labels = []
    sns.lineplot(data = data, x = "start", y = var , color = spotify_green)
    labels.append(var)

    if rolling_average:
        data["media_movil"] = data[var].rolling(rolling_size).mean()
        sns.lineplot(data = data, x = "start", y = "media_movil", color = spotify_purple)
        labels.append("Media Móvil")
    if trendline: # como chucha hago la trendlin    
        data["x"] = [i for i in range(len(data))]
        slope, intercept, r_value, pv, se = stats.linregress(data["x"], data[var])
        data["reg"] = data["x"] * slope + intercept
        sns.lineplot(data = data, x = "start", y = "reg", color = spotify_blue)
        labels.append(f"Tendencia, r={r_value:.2f}")
        if IC:
            data["sup"] = data["reg"] + 1.96 * data[var].std()/np.sqrt(len(data[var]))
            data["inf"] = data["reg"] - 1.96 *data[var].std()/np.sqrt(len(data[var]))
            sns.lineplot(data = data, x = "start", y = "sup", color = "red")
            sns.lineplot(data = data, x = "start", y = "inf", color = "red")

    if aux:

        years = md.YearLocator()   # every year
        months = md.MonthLocator()  # every month
        years_fmt = md.DateFormatter('%Y-%m')

        ax.xaxis.set_major_locator(months)
        ax.xaxis.set_major_formatter(years_fmt)
        ax.xaxis.set_minor_locator(months)

    # ax.xaxis.label.set_color(spotify_white)
    # ax.yaxis.label.set_color(spotify_white)
    # ax.tick_params(axis='x', colors=spotify_white)
    # ax.tick_params(axis='y', colors=spotify_white)

    # for _,s in ax.spines.items():
    #     s.set_color(spotify_white)

    plt.xticks(rotation = 'vertical')
    plt.legend(labels=labels)
    # plt.show()
    plt.savefig(nombre, transparent = False)
    plt.close()

def barplot(df, var, nombre = "a"):

    fig, ax = plt.subplots(figsize = (16,10))

    sns.barplot(data = df, x = "start", y = var , color = spotify_green, estimator=np.mean, ci=95,capsize=.2)

    plt.xticks(rotation = 'vertical')
    # plt.legend(labels=labels)
    # plt.show()
    std = df[var].std()
    plt.ylim(min(df[var]-std), max[df[var]]+std)
    plt.savefig(nombre, transparent = False)
    plt.close()

def var_mensual(mensual, n):
    mensual["hue"] = [False]*n + [True]*(12-n)
    a1 = mensual[mensual.hue == False].drop(["start","hue"], axis = 1).transpose().reset_index()
    a2 = mensual[mensual.hue == True].drop(["start","hue"], axis = 1).transpose().reset_index()
    a1 = pd.melt(a1, id_vars='index', value_name='valor').drop(["variable"], axis = 1)
    a2 = pd.melt(a2, id_vars='index', value_name='valor').drop(["variable"], axis = 1)
    a1["periodo"] = "inicio"
    a2["periodo"] = "fin"

    aux = pd.concat([a1,a2], axis = 0)
    aux.columns = ["feature", "valor", "periodo"]

    fig, ax = plt.subplots(figsize = (16,10))
    sns.barplot(x='feature', y='valor', ci = "sd", data=aux, hue = "periodo", palette = [spotify_green, spotify_blue])
    plt.savefig(f"figuras/Primeros {n} meses vs el resto")
    plt.close()

def main():
    df = pd.read_csv("https://raw.githubusercontent.com/PabloReyesPolanco/spotify/master/Spotify%20Weekly.csv")
    df = df.drop(["url","time_signature","key","mode"], axis = 1)
    df = df[df.year > 2016]
    df = df.dropna(axis = 0)
    df["duration_s"] = df["duration_ms"]/1000
    df = df.sort_values(["start","position"])
    df['start'] = pd.to_datetime(df['start'], format = '%Y-%m-%d')
    #df.columns = ["posición", "año", "semana","semana_fin", "nombre_canción", "artista", "reproducciones", "danzabilidad", "energía", "volumen", "habladuría", "acusticidad", "instrumentalidad", "viveza", "valencia", "tempo", "duracion_ms", "duracion_s", "duracion_m,"]

    df.reset_index(drop=True, inplace=True)

    semanal = df.groupby("start", as_index = False).agg(
        danceability = ("danceability","mean"),
        energy = ("energy","mean"),
        loudness = ("loudness","mean"),
        speechiness = ("speechiness","mean"),
        acousticness = ("acousticness","mean"),
        instrumentalness = ("instrumentalness","mean"),
        liveness = ("liveness","mean"),
        valence = ("valence","mean"),
        tempo = ("tempo","mean"),
        duration_s = ("duration_s","mean")
        )

    semanal["id"] = [i for i in range(len(semanal))]

    mensual = semanal.groupby(semanal['start'].dt.month).mean()
    mensual = mensual.reset_index()
    mensual = mensual.drop(["id"], axis = 1)
    mensual['start'] = mensual['start'].apply(lambda x: calendar.month_abbr[x])

    aux = mensual.pop("start")
    mensual=(mensual-mensual.mean())/mensual.std()
    # (mensual-mensual.min())/(mensual.max()-mensual.min())
    mensual.insert(0, "start", aux)

    for i in range(9,12):
        var_mensual(mensual, i)

    for i in aa:
        time_series(mensual.reset_index(), i, nombre = f"figuras/series tiempo mensual/timeserie {i}", aux = False)

    heatmap(mensual, vars = aa, nombre = "figuras/mapas calor/heatmap semanal")
    heatmap(df, vars = aa + ["position"], nombre = "figuras/mapas calor/heatmap global")

    for i in aa:
        histogram(semanal, i, nombre = f"figuras/histogramas/hist {i}")

    for it, var1 in enumerate(aa):
        for var2 in aa[it+1:]:
            reg_plot(semanal, var1, var2, nombre = f"figuras/regresion semanal/reg_week {var1} vs {var2}")

    for it, var1 in enumerate(aa):
        for var2 in aa[it+1:]:
            reg_plot(df, var1, var2, nombre = f"figuras/regresion global/reg_global {var1} vs {var2}")

    for i in aa:
        time_series(semanal, i, trendline = True, rolling_average = True, rolling_size = 4, nombre = f"figuras/series tiempo semanal/timeseries {i}")

    for i in aa:
        time_series(df, i, trendline = "True", nombre = f"figuras/series tiempo global/timeserie_global {i}")
    acotados = ["danceability", "duration_s","energy","instrumentalness","tempo"]
    heatmap(semanal, vars = acotados, nombre = "figuras/mapas calor/heatmap acotado")

if __name__ == "__main__":
    main()