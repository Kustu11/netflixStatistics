Made by: Kustu Künnapas
Program for Netflix data analyse based by viewing history.
Made for project to LTAT.TK.011
Needs tmdbsimple, matplotlib, pandas and numpy(included in pandas).
Default package contains of 7 files: tmdb.py, netflixToCSV.py and Statistics.py for code,
excepts.txt for exceptions, Readme.txt for info and NetflixViewingHistory.csv and RuntimeCSV.csv
for test cases. 

To start program, you need to download your NetflixViewingHistory.csv file to this folder(replace),
or try with given file. After program you can see your data. If you want to recreate this info,
just response like you have RuntimeCSV.csv file. Program doesn't save any data except RuntimeCSV.csv.
Other data is based on this file, and can be viewed with Statistics.py.

NetflixViewingHistory.csv to RuntimeCSV.csv takes a lot of time(high number of requests),
depends on different aspects, for example:
7300 lines ~1 hour
When you already have RuntimeCSV.csv, then the program time is minimal.

default setting in netflixToCSV.py are:
NetflixHis = 'NetflixViewingHistory.csv'
Output = "RuntimeCSV.csv"
fileExcept = "except.txt"
filmMed = 96
tvMed = 41
isAvg = True
autoChoose = True
You can change these in netflixToCSV.py(Lines 35-41).

Statistics.py reading data from RuntimeCSV.csv by default. 
You can change it at line 18. Keep in mind, that in netflixToCSV.py you need to change output too.

except.txt is needed for more precise statistics. You can add exceptions yourself, 
if you find mistakes in RuntimeCSV.csv. 
except.txt contains 5 different type of exceptions:
1_title: title, what is tv series, but program takes it as movie
2_title: same, but detected as tv series
3_title_newTitle: change title name for database request
4_title_newTitle: changes title and detected tv series to movie
5_title_newTitle: changes title and detected movie to tv series

If autoChoose = False, you can choose between movies/tv series,
which have same name, but different data, otherwise program choose the most likely outcome.
If isAvg = False, you can enter every undetected runtime for movies/tv series,
otherwise program uses Median
If both are True, the mistake is up to 1-2%, otherwise less. Depends on views.
After first run you see your average runtimes, and you can change filmMed and tvMed to more accurate data.

