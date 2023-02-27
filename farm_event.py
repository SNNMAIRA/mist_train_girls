from mist_train_girls_requests import post_req
from mist_train_girls_requests import post_jsonstring
from mist_train_girls_requests import get_req
from battle_extension import getfile
from battle import get_party_list
import datetime
import time
import battle
import json
import battle_extension


def farm_event(event_world_id, token):    
    getfile('https://assets.mist-train-girls.com/production-client-web-static/MasterData/MDeckViewModel.json','./MDeckViewModel.json')
    with open('./MDeckViewModel.json','r', encoding='UTF-8') as f:
        deckdata=json.loads(f.read())
    f.close()
    world_id = battle_extension.worlddata
    begin_stage = 0
    end_stage = 0
    for i in world_id:
        if(i['Id'] == event_world_id):
            begin_stage = i['Areas'][0]['Locations'][0]['Id']
            end_stage = i['Areas'][0]['Locations'][-1]['Id']
    if(begin_stage == 0):
        print("can not find quest in farmevent world id is", event_world_id)
        return 1
    begin_stage = int(begin_stage/100)*1000 + 100 + begin_stage%10
    end_stage = int(end_stage/100)*1000 + 100 + end_stage%10
    party_id = (eval('get_party_list(token)'+battle.party_dict['regular_farm_magical_party']))
    for i in deckdata:
        if (i["Id"] == int(end_stage*1000)+1):
            if(i["MDeckDetails"][0]['Status']['Defence'] < i["MDeckDetails"][0]['Status']['MindDefence']):
                party_id = (eval('get_party_list(token)'+battle.party_dict['regular_farm_physical_party']))
                print(end_stage, "regular_farm_physical_party", party_id)
            else:
                party_id = (eval('get_party_list(token)'+battle.party_dict['regular_farm_magical_party']))
                print(end_stage, "regular_farm_magical_party", party_id)
    print(event_world_id, "is farm event world id and last stage id is", end_stage)
    can_start = post_req(r"https://mist-production-api-001.mist-train-girls.com/api/Battle/canstart/" + str(end_stage) + r"?uPartyId="+str(party_id), token)
    if(can_start['r']['CanStart'] is True):
        print("farm event already all stage cleared")
        return 0
    while(begin_stage <= end_stage):
        # 高铁任务战败就立即结束
        if(battle.auto_battle(begin_stage, party_id, token) == 1):
            print("farm event finish but",begin_stage, "is too hard not clear")
            return 0
        time.sleep(5)
        begin_stage = begin_stage + 1
    print("farm event clear")
    return 0


def farm_background(event_world_id, token):
    getfile('https://assets.mist-train-girls.com/production-client-web-static/MasterData/MDeckViewModel.json','./MDeckViewModel.json')
    with open('./MDeckViewModel.json','r', encoding='UTF-8') as f:
        deckdata=json.loads(f.read())
    f.close()
    world_id = battle_extension.worlddata
    begin_stage = 0
    end_stage = 0
    for i in world_id:
        if(i['Id'] == event_world_id):
            begin_stage = i['Areas'][0]['Locations'][0]['Id']
            end_stage = i['Areas'][0]['Locations'][-1]['Id']
    if(begin_stage == 0):
        print("can not find quest in farmevent world id is", event_world_id)
        return 1
    begin_stage = int(begin_stage/100)*1000 + 100 + begin_stage%10
    end_stage = int(end_stage/100)*1000 + 100 + end_stage%10
    party_id = (eval('get_party_list(token)'+battle.party_dict['regular_farm_magical_party']))
    for i in deckdata:
        if (i["Id"] == int(end_stage*1000)+1):
            if(i["MDeckDetails"][0]['Status']['Defence'] < i["MDeckDetails"][0]['Status']['MindDefence']):
                party_id = (eval('get_party_list(token)'+battle.party_dict['regular_farm_physical_party']))
                print(end_stage, "regular_farm_physical_party", party_id)
            else:
                party_id = (eval('get_party_list(token)'+battle.party_dict['regular_farm_magical_party']))
                print(end_stage, "regular_farm_magical_party", party_id)
    print(event_world_id, "is farm event world id and last stage id is", end_stage)
    can_start = post_req(r"https://mist-production-api-001.mist-train-girls.com/api/Battle/canstart/" + str(end_stage) + r"?uPartyId="+str(party_id), token)
    if(can_start['r']['CanStart'] is False):
        print("farm event is not all stage cleared")
        if((post_req(r"https://mist-production-api-001.mist-train-girls.com/api/Battle/canstart/" + str(begin_stage) + r"?uPartyId="+str(party_id), token)['r']['CanStart']) is False):
            print("farm event no stage can departure")
            return 1
    if(can_start['r']['CanStart'] is True):
        # 高铁任务周回战败 则尝试周回最低难度的关卡
        if(battle.auto_battle(end_stage, party_id, token) == 1):
            print("farm event",end_stage, "is too hard for farm") 
            battle.auto_battle(begin_stage, party_id, token)
            print(begin_stage, "is farmevent background autobattle", party_id)
        else:
            print(end_stage, "is farmevent background autobattle", party_id)
    else:
        battle.auto_battle(begin_stage, party_id, token)
        print(begin_stage, "is farmevent background autobattle", party_id)
    time.sleep(5)
    if(battle.recover_background_action_potion(token) == 0):
        post_req(r"https://mist-production-api-001.mist-train-girls.com/api/Battle/DepartBackGroundAutoPlay", token)
        return 0
    else:
        print("do not have any potion")
        return 2