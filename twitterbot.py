
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
        last_match_file = open("lastmatch.txt", "w") #write the new 'last match'
        last_match_file.write(str(last_match_id))
        last_match_file.close()

        link_to_match = "https://matchhistory.br.leagueoflegends.com/pt/#match-details/"+my_region.upper+"/"+str(last_match_id)

        last_match_stats = get_last_match_stats(watcher, sr_nome, my_region)
        top_damage = format(last_match_stats['top_damage'],",")
        top_kills = str(last_match_stats['top_kills'])
        champion_name = str(last_match_stats['champion'])

        champion_msg = sr_nome + " was playing "+champion_name
        if(last_match_stats['top_damage_name']==sr_nome):
            top_damage_msg = sr_nome + " did the most damage to champions? Yes! ("+top_damage+")"
        else:
            top_damage_msg = sr_nome +" did the most damage to champions? No! ("+top_damage+")"
        if(last_match_stats['top_kills_name']==sr_nome):
            top_kills_msg = sr_nome + " had the most kills? Yes! ("+top_kills+")"
        else:
            top_kills_msg = sr_nome + " had the most kills? No! ("+top_kills+")"

        #this part of the code was used for debugging only
        #twitter_user_id = 855200195654684672 #you can get it from your 
        #api.send_direct_message(twitter_user_id, champion_msg + "\n"+top_damage_msg + "\n" + top_kills_msg)
        #api.send_direct_message(twitter_user_id, link_to_match) #send a dm with the link

        tweet = champion_msg +"\n"+top_damage_msg + "\n" + top_kills_msg + "\n" + link_to_match
        print("Tweeting last match...")
        api.update_status(tweet)
        print("Done!")
    else:
        print("Already tweeted last match!")

while True:
    tweet_last_match()
    time.sleep(60*2)
