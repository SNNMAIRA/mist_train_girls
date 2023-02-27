from mist_train_girls_requests import post_req
from mist_train_girls_requests import post_jsonstring
from mist_train_girls_requests import get_req
from battle import get_party_list
from battle_extension import getfile
import time
import battle
import datetime
import json

def altar_event(event_id ,token):
    # 拉取活動信息 模擬真實操作
    post_req(r'https://mist-production-api-001.mist-train-girls.com/api/Event/' + str(event_id) + r'/updateEvent', token)
    get_req(r'https://mist-production-api-001.mist-train-girls.com/api/Event/' + str(event_id) + r'/growup/ranking', token)
    event_info = get_req(r"https://mist-production-api-001.mist-train-girls.com/api/Event/info?mEventId=" + str(event_id), token)
    area_id = event_info['r']['OpendEventAreas'][0]['MAreaId']
    stage_id_sample = int(int(get_req(r"https://mist-production-api-001.mist-train-girls.com/api/Event/" + str(event_id)+ r"/growupinfo", token)['r']['RankingMQuestId']/100)*100) + 1
    getfile('https://assets.mist-train-girls.com/production-client-web-static/MasterData/MDeckViewModel.json','./MDeckViewModel.json')
    with open('./MDeckViewModel.json','r', encoding='UTF-8') as f:
        deckdata=json.loads(f.read())
    f.close()
    party_id = (eval('get_party_list(token)'+battle.party_dict['altar_magical_party']))
    for i in deckdata:
        if (i["Id"] == int((stage_id_sample+34)*1000) + 1):
            if(i["MDeckDetails"][0]['Status']['Defence'] < i["MDeckDetails"][0]['Status']['MindDefence']):
                party_id = (eval('get_party_list(token)'+battle.party_dict['altar_physical_party']))
                print(area_id, "altar_physical_party", party_id)
            else:
                party_id = (eval('get_party_list(token)'+battle.party_dict['altar_magical_party']))
                print(area_id, "altar_magical_party", party_id)
    print(event_id, "altar event id is", area_id)
    # 從三十五関往後找 找到第一個可以打的關卡ID
    current_id = stage_id_sample + 34
    # 自動打到祭壇的第三十関
    can_start = post_req(r"https://mist-production-api-001.mist-train-girls.com/api/Battle/canstart/" + str(current_id) + r"?uPartyId="+str(party_id), token)
    while(can_start['r']['CanStart'] is not True):
        if(can_start['r']['FaildReason'] == 1):
            current_id = current_id - 1
        else:
            raise Exception("altar event get current quest error")
        can_start = post_req(r"https://mist-production-api-001.mist-train-girls.com/api/Battle/canstart/" + str(current_id) + r"?uPartyId="+str(party_id), token)
    print(current_id, "is now altar quest")
    if(current_id%100 > 30):
        print("now alter quest is above 30")
        return 0
    while(current_id%100 <= 30):
        # 祭坛任务战败就什么都不用做 等着打2-5
        if(battle.auto_battle(current_id, party_id, token) == 1):
            print("altar event finish but", current_id, "is too hard not clear")
            return 0
        time.sleep(5)
        current_id = current_id + 1
    print("altar quest is cleared", current_id)
    return 0

# 打完祭坛就挂指定的关卡 默认2-5
def altar_background(quest_id, token):
    getfile('https://assets.mist-train-girls.com/production-client-web-static/MasterData/MDeckViewModel.json','./MDeckViewModel.json')
    with open('./MDeckViewModel.json','r', encoding='UTF-8') as f:
        deckdata=json.loads(f.read())
    f.close()
    party_id = (eval('get_party_list(token)'+battle.party_dict['regular_farm_magical_party']))
    for i in deckdata:
        if (i["Id"] == int(quest_id*1000)+1):
            if(i["MDeckDetails"][0]['Status']['Defence'] < i["MDeckDetails"][0]['Status']['MindDefence']):
                party_id = (eval('get_party_list(token)'+battle.party_dict['regular_farm_physical_party']))
                print(quest_id, "regular_farm_physical_party", party_id)
            else:
                party_id = (eval('get_party_list(token)'+battle.party_dict['regular_farm_magical_party']))
                print(quest_id, "regular_farm_magical_party", party_id)
    battle.auto_battle(quest_id, party_id, token)
    time.sleep(5)
    if(battle.recover_background_action_potion(token) == 0):
        post_req(r"https://mist-production-api-001.mist-train-girls.com/api/Battle/DepartBackGroundAutoPlay", token)
        print(quest_id, "background autobattle completed", party_id)
        return 0
    else:
        print("do not have any potion")
        return 2