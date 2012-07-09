----------------------------------------
su postgres // This command need to be run as root.
psql -c "CREATE USER tf2ib WITH PASSWORD 'jw8s0F4'"
psql -c "CREATE DATABASE tf2ib"
psql tf2ib < database.sql
psql tf2ib < sample.sql // Run this command only if you want to populate your database with testing data.

2nd step: installing the necessary library and running the scripts. Before running those 2 scripts you need to change the value of some variabbles in the file "config.py"
----------------------------------------
aptitude install python-psycopg2 // You can use apt-get or yum, as long as you install properly the pyscopg2 library you are good to go.
./pug.py
./send.py PUG-MESSENGER // The second argument is the nickname of your messenger.

Files:
BeautifulSoup.py // Library used to parse HTLM, it's only used on the ESEA bot.
config.py // Configuration file used by some scripts, you will probably set the variable values to what you need.
data.sh // Script that is intended to run as a cron job on a TF2 server. It does copy the stats and STV files to the web server.
database.sql // File used to create the tables for the bot database.
irclib.py // Library used by the different bots to connect and communicate through the IRC protocol.
pug.py // Main bot, I is strongly recommended to analyze the code before doing any modifications.
run.sh // Wrapper script that automatically re-launch the bot when they crash (this will happen). You usually use the script as follow (arguments are optionnals): ./run.sh pug.py PUG-BOT
sample.sql // Data for the database, this is mostly for if you need to fill the tables with some testing data.
send.py // Messenger bot, you need at least one running.
SRCDS.py // Library used to send rcon commands and control the TF2 servers.
