
import time
import tweepy

from lolinfo import *

def tweet_last_match():

    print("hello its me, your bot")

    CONSUMER_KEY = '' #your twitter API Key
    CONSUMER_SECRET = '' #your twitter API Secret
    ACCESS_KEY = '' #Access Token generated for your user
    ACCESS_SECRET = '' #Access Token Secret generated for your user

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    #me = api.me()._json['id']
    sr_nome = 'Mozan'#The riot account user you are searching
    my_region = 'br1'#The region from the riot account
    watcher = connect_riot()


    last_match_id = get_last_match_id(watcher, my_region, sr_nome)


    last_match_file = open("lastmatch.txt", "r") #read the last match that was tweeted
    last_match_file_id = last_match_file.read()
    last_match_file.close()

    if(last_match_file_id != last_match_id):
        link_to_match = "https://matchhistory.br.leagueoflegends.com/pt/#match-details/"+my_region.upper+"/"+str(last_match_id)

        last_match_stats = get_last_match_stats(watcher, sr_nome, my_region, 0)
        top_damage = format(last_match_stats['playerDamage'], ",")
        top_kills = str(last_match_stats['playerKills'])
        champion_name = str(last_match_stats['champion'])
        game_mode = str(last_match_stats['gameMode'])

        print(champion_name)

        killStats = ""
        if(last_match_stats['pentaKills'] > 0):
            killStats = "[PENTA KILL]"
        elif(last_match_stats['quadraKills'] > 0):
            killStats = "[QUADRA KILL]"

        champion_msg = sr_nome + " was playing "+champion_name+" in " + game_mode
        if(last_match_stats['top_damage_name'] == sr_nome):
            top_damage_msg = "Top damage to players? Yes! ("+top_damage+")"
        else:
            top_damage_msg = "Top damage to players? No! ("+top_damage+")"
        if(last_match_stats['top_kills_name'] == sr_nome):
            top_kills_msg = "Top kills? Yes! ("+top_kills+")"
        else:
            top_kills_msg = "Top kills? No! ("+top_kills+")"

        #api.send_direct_message(855200195654684672, champion_msg + "\n"+top_damage_msg + "\n" + top_kills_msg)
        tweet = killStats + "\n" + champion_msg + "\n" + \
            top_damage_msg + "\n" + top_kills_msg + "\n" + link_to_match
        print("Tweeting last match...")
        #api.send_direct_message(855200195654684672, link_to_match) #send a dm with the link
        api.update_status(tweet)
        print("Done!")
        last_match_file = open("lastmatch.txt", "w")
        last_match_file.write(str(last_match_id))
        last_match_file.close()
    else:
        print("Already tweeted last match!")

while True:
    tweet_last_match()
    time.sleep(60*2)
