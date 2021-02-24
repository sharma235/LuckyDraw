# LuckyDraw
API to take part in lucky Draw

# Required Dependencies 
This website is built using Flask so you have to build flask environment</br>
Refer to this - https://flask.palletsprojects.com/en/master/installation/ </br>
under pip3 install-</br>
uuid, MySQLdb , random </br>
Required mysql for database </br>

# Compilation
1. Enter user and password for the sql database connection in dbKey.py file </br>
2. Now to create database run python3 createdb.py command </br>
3. Now run python3 main.py command </br>
 
# API info

1. /draw/ticket - Allows users to get the raffle tickets. </br>
2. /draw/takepart/<token> - Allows users to participate in the game. </br>
3. /draw/winners - Lists all the winners of all the events in the last one week </br>
4. /draw/reward - Shows Lucky Draw Event timing & the
corresponding reward. </br>
5. /draw/compute - Compute the winner for the event and announce the winner. </br>
