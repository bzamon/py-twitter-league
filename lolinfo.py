from os import stat
from riotwatcher import LolWatcher, ApiError
import pandas as pd

# golbal variables
def connect_riot():
    api_key = 'RGAPI-XXXXXX'#your riot api key should go here
    watcher = LolWatcher(api_key)

    return watcher


def gamemode(queueId):
    queueId = str(queueId)
    return {
        '400': 'Normal Game',
        '420': 'Ranked Solo/Duo',
        '440': 'Ranked Flex',
        '450': 'ARAM'
    }[queueId]

def get_last_match_stats(watcher, sr_nome, my_region, match_pos):
    me = watcher.summoner.by_name(my_region, sr_nome)
    #print(me)

    my_matches = watcher.match.matchlist_by_account(my_region, me['accountId'])

    # fetch last match detail
    last_match = my_matches['matches'][match_pos]
    match_detail = watcher.match.by_id(my_region, last_match['gameId'])
    # check league's latest version
    latest = watcher.data_dragon.versions_for_region(my_region)['n']['champion']
    # Lets get some champions static information
    static_champ_list = watcher.data_dragon.champions(latest, False, 'en_US')
    #print(static_champ_list)

    champ_dict_id = {}
    champ_dict = {}
    for key in static_champ_list['data']:
        row = static_champ_list['data'][key]
        champ_dict_id[row['key']] = row['id']
        champ_dict[row['key']] = row['name']

    #print(champ_dict)
    #print(match_detail)
    top_damage_dealt = 0
    top_kills = 0
    stats = {}

    queueId = match_detail['queueId']
    stats['gameMode'] = gamemode(queueId)

    for row in match_detail['participants']:
        participants_row = {}
        user_id = row['participantId'] - 1

        summoner_name = match_detail['participantIdentities'][user_id]['player']['summonerName']

        participants_row['user'] = summoner_name
        participants_row['champion'] = champ_dict[str(row['championId'])]
        if(summoner_name == sr_nome):
            stats['champion'] = participants_row['champion']
            stats['playerKills'] = row['stats']['kills']
            stats['playerDamage'] = row['stats']['totalDamageDealtToChampions']
            stats['quadraKills'] = row['stats']['quadraKills']
            stats['pentaKills'] = row['stats']['pentaKills']

        participants_row['win'] = row['stats']['win']

        kills = row['stats']['kills']
        if(kills > top_kills):
            top_kills = kills
            stats['top_kills_name'] = summoner_name

        damage_dealt = row['stats']['totalDamageDealtToChampions']

        if(damage_dealt > top_damage_dealt):
            top_damage_dealt = damage_dealt
            stats['top_damage_name'] = summoner_name

    stats['top_kills'] = top_kills
    stats['top_damage'] = top_damage_dealt

    return stats

def search_user():
    sr_nome = input("Who are you looking for? ")
    my_region = input("What is the region? Ex: br1, na1...")

    watcher = connect_riot()
    if(get_last_match_stats(watcher,sr_nome,my_region)):
        print("The top damage player was "+sr_nome)
    else:
        print("The searched player was not the top damage")


def get_last_match_id(watcher,my_region,sr_nome):
    me = watcher.summoner.by_name(my_region, sr_nome)
    my_matches = watcher.match.matchlist_by_account(my_region, me['accountId'])

    # fetch last match detail
    last_match = my_matches['matches'][0]
    return str(last_match['gameId'])
