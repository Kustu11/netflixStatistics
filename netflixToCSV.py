"""
Program for making CSV with runtime and other info from NetflixViewingHistory.csv
"""


#imports modules
from tmdb import tmdbMovie, tmdbTv
import pandas as pd
import numpy as np
import time
from csv import *



def askWhich(inList, isAvg = False): # Asks which info is right about show
    if not isAvg:
        print("Which one is your watched?")
        for i in range(len(inList)):
            try:
                print(str(i), inList[i][1], inList[i][2][0], inList[i][3], inList[i][4])
            except:
                print(str(i), inList[i][1], inList[i][2], inList[i][3], inList[i][4])
        n = int(input("Choose 0 to "+str(len(inList)-1)+": "))
    else:n =0
    return inList[n]





def NetflixCsv():# Main cycle


    #Settings
    NetflixHis = 'NetflixViewingHistory.csv'
    Output = "RuntimeCSV.csv"
    fileExcept = "except.txt"
    filmMed = 96
    tvMed = 41
    isAvg = True
    autoChoose = True
    
    f = open(fileExcept,"r",encoding = "UTF-8") #Read excepts information from file
    types = []
    for a in f:
        try:
            n,org,new = a.rstrip().split("_")
            types.append(n)
            types.append(org)
            types.append(new)
        except:
            n,org = a.rstrip().split("_")
            types.append(n)
            types.append(org)
    f.close()
    # Starts csv file
    fe = open(Output,"w",encoding = "UTF-8", newline = '')
    fieldnames = ["Title","Tv","Runtime","Date","isMovie","Genre"]
    writer = DictWriter(fe,fieldnames=fieldnames)
    writer.writeheader()

    # Imports Netflix history
    df_iter = pd.read_csv(NetflixHis, iterator=True)
    for iter_num, df in enumerate(df_iter, 1):
        pass
    valja = df.to_numpy()
    TvHistory = {}
    ids = []
    for i in range(len(valja)): #Checks every Title
        isMovie = False
        isTv = False
        isHook = False
        print(str(i) + "/"+str(len(valja)))
        view = valja[i][0]
        date = valja[i][1]
        vir = view.split(":")
        check = []
        hookers = []
        runTime = 0
        avgUsed = False
        try:
            hookers += vir[0].split("_")
            hookers += vir[0].split(" ")
            check += vir[1].split()
            hookers += vir[1].split("_")
            check += (vir[2].split())
            hookers += (vir[2].split("_"))
        except:
            pass
        if "hook" in hookers or "primary" in hookers or "Trailer" in hookers: # Checks if title is hook or trailer
            isHook = True
            runTime = 0
            
        if ("Season" in check or "Series" in check or "Part" in check or "Volume" in check or " Season" in check or "Episode" in check or "Chapter" in check) and isHook == False:
            #If title most likely is tv episode
            if vir[0] in TvHistory:
                runTime = TvHistory[vir[0]] 
            isTv = True
            if runTime == 0: # Take information from database
                Tv = vir
                TV = tmdbTv(Tv[0], types)
                if TV == []:
                    name = (Tv[0]+":"+Tv[1])
                    try:
                        TV = tmdbTv(name, types)
                        if TV == []:
                            try:
                                TV = tmdbTv(view, types)
                            except:
                                pass
                    except:
                        pass
                    
                out = TV
                try:
                    if type(out[0][2]) != type([]): #Checks if title is still tv
                        isTv = False
                        isMovie = True
                except: pass

        elif isHook == False: # If title is movie
            isMovie = True
            Movie = vir
            Movies = tmdbMovie(view, types)
            if len(Movies) == 0: # Finds information
                try:
                    Movies = tmdbMovie(Movie[0], types)
                    if len(Movies) == 0:
                        try:
                            name = (Movie[0]+":"+Movie[1])
                            Movies = tmdbMovie(name, types)
                        except:
                            pass
                except:
                    pass
            out = Movies
            try:
                if type(out[0][2]) == type([]):# Checks if it is still movie
                    isTv = True
                    isMovie = False
            except: pass
            
                
        if not isHook: #Starts to save information
            if len(out) == 0 and runTime == 0: # If no information in Db
                if not isAvg: 
                    seq = "Didn't find: "+ view+" in TMDB\n"
                    print(seq)
                    new = input("Please enter this movie/Tvshow name from Tmdb or \n0 if you didn't find it: ")
                    if new != 0:
                        fa = open(fileExcept,"a",encoding = "UTF-8")
                        seq1 = "\n3_"+vir[0]+"_"+new
                        fa.write(seq1)
                        fa.close()
                        if isMovie:
                            Movies = tmdbMovie(name, types)
                            out = Movies
                        elif isTv:
                            TV = tmdbTv(new, types)
                            out = TV
                else:
                    avgUsed = True
                    if isMovie:
                        runTime = filmMed
                    elif isTv:
                        runTime = tvMed
            if len(out) == 1: #If one title in DB
                if isTv:
                    if out[0][2] == [] and runTime == 0: # if no runtime information in DB
                        if not isAvg:
                            try:print("Database doesn't have runtime info about "+vir[0]+":"+vir[1])
                            except: print("Database doesn't have runtime info about "+vir[0])
                            runTime = int(input("Please enter this show average runtime: "))
                        else:
                            avgUsed = True
                            runTime = tvMed
                        TvHistory[vir[0]] = runTime
                        
                    elif runTime != 0: pass
                        
                    
                    else:
                        runTime = int(sum(out[0][2])/len(out[0][2]))
                        if runTime > 90:
                            if not isAvg: #If runtime is illogical
                                print('Is '+view+' runtime really '+str(runTime)+'?')
                                newRun = int(input('Enter right runtime or 0, if it is right: '))
                                if newRun != 0:
                                    runTime = newRun
                            else:
                                avgUsed = True
                                runTime = tvMed
                        TvHistory[vir[0]] = runTime
                        
                elif out[0][2] == None:
                    if not isAvg: # if no runtime information in DB
                        print("Database doesn't have runtime info about "+view)
                        runTime = int(input("Please enter "+view+" runtime: "))
                        
                    else:
                        avgUsed = True
                        runTime = filmMed
                else:
                    if runTime == 0:
                        try: runTime = int(out[0][2])
                        except: runTime = int(out[0][2][0])
            elif len(out) >= 2: # If too many same name titles.
                if isMovie or runTime == 0:
                    out = askWhich(out, autoChoose)
                    if out[2] != []:
                        try: num = int(out[2][0])
                        except:
                            try: num = int(out[2])
                            except: num = out[2]
                    else: num = 0
                    if num > 90 and isTv:
                        if not isAvg:
                            print('Is '+view+' runtime really '+str(num)+'?')
                            newRun = int(input('Enter right runtime or 0, if it is right: '))
                            if newRun != 0:
                                runTime = newRun
                                TvHistory[vir[0]] = runTime
                        else:
                            avgUsed = True
                            runTime = tvMed
                    if num == 0:
                        if isAvg:
                            avgUsed = True
                            num = tvMed
                        else:
                            print("Database doesn't have runtime info about "+view)
                            num = int(input("Please enter "+view+" runtime: "))
                            
                    if isTv: TvHistory[vir[0]] = num
                    runTime = int(num)
        
        # Outputs information
        if len(out) == 1:out = out[0]
        try:
            sID = out[0]
            if sID not in ids:
                typesa = out[4]
                ids.append(out[0])
            else: typesa = ""
        except:
            typesa = ""
        # Saves to fail e
        if isTv:
            writer.writerow({"Title":view, "Tv":vir[0], "Runtime":runTime, "Date": date, "isMovie": isMovie, "Genre":",".join(typesa)})
        else:
            writer.writerow({"Title":view, "Runtime":runTime, "Date": date, "isMovie": isMovie, "Genre":",".join(typesa)})
        
        

    fe.close()
        
        
#Extra code
"""
        f = open(Output,"a",encoding = "UTF-8")
        if not isHook:  
            if len(out) == 0:
                seq = ("Didn't find: "+ view+" in TMDB\n")
                print(seq)
                new = input("Please enter this movie/Tvshow name from Tmdb or \n0 if you didn't find it: ")
                if new != 0:
                    fa = open("except.txt","w",encoding = "UTF-8")
                    seq1 = "3_"+vir[0]+"_"+new
                    fa.write(seq1)
                    fa.close()
                    if isMovie: Movies = tmdbMovie(name)
                    elif isTv:
                        TV = tmdbTv(new)
                        out = TV
                        if len(out) == 1:
                            runTime = (str(int(sum(out[0][2])/len(out[0][2])))+"\n")
                            TvHistory[new] = runTime
                        
                    
                
                f.write(seq)
            if len(out) == 1:
                if isMovie:
                    if out[0][2] is list:
                        seq = (str(out[0][2][0])+"\n")
                    seq = (str(out[0][2])+"\n")
                    f.write(seq)
                elif isTv:
                    if runTime == "[]\n":
                        print("Database doesn't have runtime info about "+vir[0])
                        num = int(input("Please enter this show average runtime: "))
                        TvHistory[vir[0]] = num
                        runTime = str(int(str(num).rstrip()))+"\n"
                    else:
                        runTime = str(int(str(runTime).rstrip()))+"\n"
                    f.write(str(runTime))
            else:
                if runTime == 0: 
                    num = askWhich(out)
                    if isTv: TvHistory[vir[0]] = num
                    seq = str(int(str(num).rstrip()))+"\n"
                else: seq = str(int(str(runTime).rstrip()))+"\n"
                    
                f.write(seq)
            
        else:
            seq = "0\n"
            f.write(seq)
        f.close()
        """
      

"""
                if out != [] and isTv:
                    if out[0][2] != [] and type(out[0][2]) == type([]):
                        runTime = int(sum(out[0][2])/len(out[0][2]))
                        TvHistory[vir[0]] = runTime
                    elif out[0][2] != [] and type(out[0][2])  != type([]):
                        runTime = int(out[0][2][0])
                        TvHistory[vir[0]] = runTime
                    else:
                        runTime = 0
                    if runTime > 90:
                        if not isAvg:
                            print('Is '+view+' runtime really '+str(runTime)+'?')
                            newRun = int(input('Enter right runtime or 0, if it is right: '))
                            if newRun != 0:
                                runTime = newRun
                                TvHistory[vir[0]] = runTime
                        else:
                            avgUsed = True
                            runTime = tvMed
                            TvHistory[vir[0]] = runTime
                            
                        

                elif isMovie:
                    try:
                        runTime = out[0][2]
                    except: runTime = 0
                else:
                    runTime = 0
"""