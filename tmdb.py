import tmdbsimple as tm #Imports module
tm.API_KEY = '3e889fcfd527ae4c53b41103baebb8fc' # Needed for 
search = tm.Search()

def tmdbMovie(film, types): #Movie check from TMDb

    if film in types:
        try:
            n = int(types[types.index(film)-1])
        except:n=0
        if n == 3:
            film = types[types.index(film)+1]
        elif n == 1:
            return(tmdbTv(film,types))
        elif n == 5:
            try:
                return((tmdbTv(types[types.index(film)+1],types)))
            except:
                pass
        
    response = search.movie(query = film)
    oneFilm = []
    for s in search.results:
        ide = tm.Movies(s["id"])
        try:
            res = ide.info()
        except:
            res = {"title":""}
        if res["title"].lower() == film.lower():
            oneFilm.append([res["id"],res["title"], res["runtime"], res["release_date"],[x["name"] for x in res["genres"]]])
    return(oneFilm)

def tmdbTv(tvseries, types): #Tv series/episodes check from TMDb
    if tvseries in types:
        try:
            n = int(types[types.index(tvseries)-1])
        except:n=0
        if n == 3:
            try:
                tvseries = types[types.index(tvseries)+1]
            except:pass
        elif n == 2:
            return(tmdbMovie(tvseries,types))
        elif n == 4:
            try:
                return(tmdbMovie(types[types.index(tvseries)+1],types))
            except:
                pass
        
    response = search.tv(query = tvseries)
    oneTv = []
    for s in search.results:
        ide = tm.TV(s["id"])
        try:
            res = ide.info()
        except HTTPError:
            print("Api is broken")
        if res["name"].lower() == tvseries.lower():
            oneTv.append([res["id"], res["name"], res["episode_run_time"],res["first_air_date"],[x["name"] for x in res["genres"]]])
    return(oneTv)

if __name__ == "__main__": #Check for reliability
    soov = int(input("Soovid filmi(0) või tv sarja(1)? "))
    if soov == 0:
        movie = input("Sisesta filmi nimi: ")
        print(tmdbMovie(movie,types = []))
    else:
        series = input("Sisesta seriaali nimi: ")
        print(tmdbTv(series,types=[]))