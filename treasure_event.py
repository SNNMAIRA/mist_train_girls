from mist_train_girls_requests import post_req
from mist_train_girls_requests import post_jsonstring
from mist_train_girls_requests import get_req
from battle_extension import getfile
from battle import get_party_list
import datetime
import time
import battle
import json
# 在外層調用的時候控制好 活動結束時間小於一個小時則不會執行 找出第一個活動結束時間大於一個小時的可用活動類型
# 找到第一個類型為寶藏任務/高鐵/祭壇/raid boss 類型的活動的ID
# 在困难和非常困难关卡 如果战斗失败则立即返回
def treasure_event(event_id ,token):
    # 如果活動是寶藏任務
    # 拉取活動信息 模擬真實操作
    post_req(r'https://mist-production-api-001.mist-train-girls.com/api/Event/' + str(event_id) + r'/updateEvent', token)
    get_req(r'https://mist-production-api-001.mist-train-girls.com/api/Event/tresure/' + str(event_id), token)
    # 寶藏活動第一個區域的id
    event_info = get_req(r"https://mist-production-api-001.mist-train-girls.com/api/Event/info?mEventId=" + str(event_id), token)
    area1_id = event_info['r']['OpendEventAreas'][0]['MAreaId']
    try:
        area1_quest_id_sample = int(int(event_info['r']['EventQuestBonuses'][0]['MQuestId']/1000)*1000) + 501
    except Exception:
        print("can not get area1 quest id in treasure event")
        return 0
    area2_quest_id_sample = int(area1_quest_id_sample + 1000)
    getfile('https://assets.mist-train-girls.com/production-client-web-static/MasterData/MDeckViewModel.json','./MDeckViewModel.json')
    with open('./MDeckViewModel.json','r', encoding='UTF-8') as f:
        deckdata=json.loads(f.read())
    f.close()
    party_id = (eval('get_party_list(token)'+battle.party_dict['treasure_magical_party']))
    for i in deckdata:
        if (i["Id"] == int((int(area1_quest_id_sample/1000)*1000 + 501)*1000) + 1):
            if(i["MDeckDetails"][0]['Status']['Defence'] < i["MDeckDetails"][0]['Status']['MindDefence']):
                party_id = (eval('get_party_list(token)'+battle.party_dict['treasure_physical_party']))
                print(area1_id, "treasure_physical_party", party_id)
            else:
                party_id = (eval('get_party_list(token)'+battle.party_dict['treasure_magical_party']))
                print(area1_id, "treasure_magical_party", party_id)
    print(event_id, "treasure event id is", area1_id)
    # 獲取id的區域内所有關卡的id
    area1_info = get_req(r'https://mist-production-api-001.mist-train-girls.com/api/Areas/' + str(area1_id) + r'/Difficulties', token)['r']
    area1_unlocked_diffculties = area1_info['UnlockDifficulty']
    area1_quests = area1_info['UnlockQuestIds']
    print(area1_id, "area uncloked quests id are", area1_quests)
    time.sleep(3)
    area1_quests_easy = []
    area1_quests_hard = []
    area1_quests_veryhard = []
    for i in area1_quests:
        if(i%1000 < 400):
            area1_quests_easy.append(i)
        elif(400 < i%1000 < 500):
            area1_quests_hard.append(i)
        elif(500 < i%1000):
            area1_quests_veryhard.append(i)
        else:
            print("未知的關卡", i)
            raise Exception("未知的關卡 "+str(i))
    area1_quests_easy.insert(0, int(area1_quest_id_sample/1000)*1000 + 301)
    area1_stage_easy = len(area1_quests_easy)
    if(area1_stage_easy == 10 and len(area1_unlocked_diffculties) >= 1):
        area1_stage_easy = 11
    while(area1_stage_easy <= 10):
        if(area1_stage_easy == 10):
            post_req(r'https://mist-production-api-001.mist-train-girls.com/api/Quests/startSceneQuest/' + str(int(area1_quest_id_sample/1000)) + '3' + str(area1_stage_easy), token)
        elif(area1_stage_easy == 9):
            battle.auto_battle(int(area1_quest_id_sample/1000)*1000 + 300 + area1_stage_easy, party_id, token)
            time.sleep(5)
        elif(area1_stage_easy%2 == 0):
            post_req(r'https://mist-production-api-001.mist-train-girls.com/api/Quests/startSceneQuest/' + str(int(area1_quest_id_sample/1000)) + '30' + str(area1_stage_easy), token)
        elif(area1_stage_easy%2 == 1):
            battle.auto_battle(int(area1_quest_id_sample/1000)*1000 + 300 + area1_stage_easy, party_id, token)
            time.sleep(5)
        area1_stage_easy = area1_stage_easy + 1
    area1_stage_hard = len(area1_quests_hard)
    if(area1_stage_hard == 5 and len(area1_unlocked_diffculties) >= 2):
        area1_stage_hard = 6
    elif(area1_stage_hard == 0):
        area1_stage_hard = 1
    while(area1_stage_hard <= 5):
        if(battle.auto_battle(int(area1_quest_id_sample/1000)*1000 + 400 + area1_stage_hard, party_id, token) == 1):
            print("treasure event finish but", int(area1_quest_id_sample/1000)*1000 + 400 + area1_stage_hard, "is too hard not clear")
            return 0
        time.sleep(5)
        area1_stage_hard = area1_stage_hard + 1
    area2_id = event_info['r']['OpendEventAreas'][1]['MAreaId']
    print(event_id, "treasure event area two id is", area2_id)
    area2_info = get_req(r'https://mist-production-api-001.mist-train-girls.com/api/Areas/' + str(area2_id) + r'/Difficulties', token)['r']
    area2_unlocked_diffculties = area2_info['UnlockDifficulty']
    area2_quests = area2_info['UnlockQuestIds']
    time.sleep(3)
    area2_quests_easy = []
    area2_quests_hard = []
    area2_quests_veryhard = []
    for i in area2_quests:
        if(i%1000 < 400):
            area2_quests_easy.append(i)
        elif(400 < i%1000 < 500):
            area2_quests_hard.append(i)
        elif(500 < i%1000):
            area2_quests_veryhard.append(i)
        else:
            print("未知的關卡", i)
            raise Exception("未知的關卡 "+str(i))
    area1_stage_veryhard = len(area1_quests_veryhard)
    if(area1_stage_veryhard == 5 and len(area2_quests_veryhard) >= 1):
        area1_stage_veryhard = 6
    elif(area1_stage_veryhard == 0):
        area1_stage_veryhard = 1
    while(area1_stage_veryhard <= 5):
        if(battle.auto_battle(int(area1_quest_id_sample/1000)*1000 + 500 + area1_stage_veryhard, party_id, token) == 1):
            print("treasure event finish but", int(area1_quest_id_sample/1000)*1000 + 500 + area1_stage_veryhard, "is too hard not clear")
            return 0
        time.sleep(5)
        area1_stage_veryhard = area1_stage_veryhard + 1
    now_time = datetime.datetime.now()
    if(time.strftime('%z')[0]) == '-':
        min = int('-'+time.strftime('%z')[3:])
    else:
        min = int(time.strftime('%z')[3:])
    # 如果区域2还没开始 就不做了
    jp_time = now_time - datetime.timedelta(hours=(int(time.strftime('%z')[0:3])-9), minutes=(min+3))
    if(jp_time < datetime.datetime.strptime(event_info['r']['OpendEventAreas'][1]['StartDate'], "%Y-%m-%dT%H:%M:%S")):
        print("area2 is not playable")
        return 0
    area2_id = event_info['r']['OpendEventAreas'][1]['MAreaId']
    area2_info = get_req(r'https://mist-production-api-001.mist-train-girls.com/api/Areas/' + str(area2_id) + r'/Difficulties', token)['r']
    area2_unlocked_diffculties = area2_info['UnlockDifficulty']
    area2_quests = area2_info['UnlockQuestIds']
    print(area2_id, "area uncloked quests id are", area2_quests)
    time.sleep(3)
    area2_quests_easy = []
    area2_quests_hard = []
    area2_quests_veryhard = []
    for i in area2_quests:
        if(i%1000 < 400):
            area2_quests_easy.append(i)
        elif(400 < i%1000 < 500):
            area2_quests_hard.append(i)
        elif(500 < i%1000):
            area2_quests_veryhard.append(i)
        else:
            print("未知的關卡", i)
            raise Exception("未知的關卡 "+str(i))
    party_id = (eval('get_party_list(token)'+battle.party_dict['treasure_magical_party']))
    for i in deckdata:
        if (i["Id"] == int(area2_quest_id_sample*1000) + 1):
            if(i["MDeckDetails"][0]['Status']['Defence'] < i["MDeckDetails"][0]['Status']['MindDefence']):
                party_id = (eval('get_party_list(token)'+battle.party_dict['treasure_physical_party']))
                print(area2_id, "treasure_physical_party", party_id)
            else:
                party_id = (eval('get_party_list(token)'+battle.party_dict['treasure_magical_party']))
                print(area2_id, "treasure_magical_party", party_id)
    area2_stage_easy = len(area2_quests_easy)
    if(area2_stage_easy == 10 and len(area2_unlocked_diffculties) >= 2):
        area2_stage_easy = 11
    elif(area2_stage_easy == 0):
        area2_stage_easy = 1
    while(area2_stage_easy <= 10):
        if(area2_stage_easy == 10):
            post_req(r'https://mist-production-api-001.mist-train-girls.com/api/Quests/startSceneQuest/' + str(int(area2_quest_id_sample/1000)) + '3' + str(area2_stage_easy), token)
        elif(area2_stage_easy == 9):
            battle.auto_battle(int(area2_quest_id_sample/1000)*1000 + 300 + area2_stage_easy, party_id, token)
            time.sleep(5)
        elif(area2_stage_easy%2 == 1):
            post_req(r'https://mist-production-api-001.mist-train-girls.com/api/Quests/startSceneQuest/' + str(int(area2_quest_id_sample/1000)) + '30' + str(area2_stage_easy), token)
        elif(area2_stage_easy%2 == 0):
            battle.auto_battle(int(area2_quest_id_sample/1000)*1000 + 300 + area2_stage_easy, party_id, token)
            time.sleep(5)
        area2_stage_easy = area2_stage_easy + 1
    area2_stage_hard = len(area2_quests_hard)
    if(area2_stage_hard == 5 and len(area2_unlocked_diffculties) >= 3):
        area2_stage_hard = 6
    elif(area2_stage_hard == 0):
        area2_stage_hard = 1
    while(area2_stage_hard <= 5):
        if(battle.auto_battle(int(area2_quest_id_sample/1000)*1000 + 400 + area2_stage_hard, party_id, token) == 1):
            print("treasure event finish but", int(area2_quest_id_sample/1000)*1000 + 400 + area2_stage_hard, "is too hard not clear")
            return 0
        time.sleep(5)
        area2_stage_hard = area2_stage_hard + 1
    area2_stage_veryhard = len(area2_quests_veryhard)
    if(area2_stage_veryhard == 0):
        area2_stage_veryhard = 1
    while(area2_stage_veryhard <= 4):
        if(battle.auto_battle(int(area2_quest_id_sample/1000)*1000 + 500 + area2_stage_veryhard, party_id, token) == 1):
            print("treasure event finish but", int(area2_quest_id_sample/1000)*1000 + 500 + area2_stage_veryhard, "is too hard not clear")
            return 0
        time.sleep(5)
        area2_stage_veryhard = area2_stage_veryhard + 1
    print("treasure event complete", event_id)
    return 0


# 找到veryhard裏除了最後打王関之外最後一個解鎖的關卡
def treasure_background(event_id, token):
    # 拉取活動信息 模擬真實操作
    post_req(r'https://mist-production-api-001.mist-train-girls.com/api/Event/' + str(event_id) + r'/updateEvent', token)
    get_req(r'https://mist-production-api-001.mist-train-girls.com/api/Event/tresure/' + str(event_id), token)
    # 寶藏活動第一個區域的id
    event_info = get_req(r"https://mist-production-api-001.mist-train-girls.com/api/Event/info?mEventId=" + str(event_id), token)
    area1_id = event_info['r']['OpendEventAreas'][0]['MAreaId']
    try:
        area1_quest_id_sample = int(int(event_info['r']['EventQuestBonuses'][0]['MQuestId']/1000)*1000) + 501
    except Exception:
        print("can not get area1 quest id in treasure event")
        return 0
    # area2_quest_id_sample = int(area1_quest_id_sample + 1000)
    getfile('https://assets.mist-train-girls.com/production-client-web-static/MasterData/MDeckViewModel.json','./MDeckViewModel.json')
    with open('./MDeckViewModel.json','r', encoding='UTF-8') as f:
        deckdata=json.loads(f.read())
    f.close()
    # now_time = datetime.datetime.now()
    # if(time.strftime('%z')[0]) == '-':
    #     min = int('-'+time.strftime('%z')[3:])
    # else:
    #     min = int(time.strftime('%z')[3:])
    # # 如果区域2还没开始 就不做了
    # jp_time = now_time - datetime.timedelta(hours=(int(time.strftime('%z')[0:3])-9), minutes=(min+3))
    # if(jp_time < datetime.datetime.strptime(event_info['r']['OpendEventAreas'][1]['StartDate'], "%Y-%m-%dT%H:%M:%S")):
    #     print("area2 is not playable")
    # else:
    #     area2_id = event_info['r']['OpendEventAreas'][1]['MAreaId']
    #     area2_info = get_req(r'https://mist-production-api-001.mist-train-girls.com/api/Areas/' + str(area2_id) + r'/Difficulties', token)['r']
    #     area2_unlocked_diffculties = area2_info['UnlockDifficulty']
    #     area2_quests = area2_info['UnlockQuestIds']
    #     print(area2_id, "area uncloked quests id are", area2_quests)
    #     time.sleep(3)
    #     area2_quests_easy = []
    #     area2_quests_hard = []
    #     area2_quests_veryhard = []
    #     stage_id = area2_quest_id_sample
    #     for i in area2_quests:
    #         if(i%1000 < 400):
    #             area2_quests_easy.append(i)
    #         elif(400 < i%1000 < 500):
    #             area2_quests_hard.append(i)
    #         elif(500 < i%1000):
    #             area2_quests_veryhard.append(i)
    #         else:
    #             print("未知的關卡", i)
    #             raise Exception("未知的關卡 "+str(i))
    #     if(len(area2_quests_veryhard) >= 5):
    #         stage_id = area2_quests_veryhard[-2]
    #     elif(len(area2_quests_veryhard) == 0):
    #         print("area2 has no quest can battle")
    #         stage_id = area1_quest_id_sample
    #     else:
    #         stage_id = area2_quests_veryhard[-1]
    #     if(stage_id == area1_quest_id_sample):
    #         pass
    #     else:
    #         party_id = (eval('get_party_list(token)'+battle.party_dict['treasure_magical_party']))
    #         for i in deckdata:
    #             if (i["Id"] == int(area2_quest_id_sample*1000) + 1):
    #                 if(i["MDeckDetails"][0]['Status']['Defence'] < i["MDeckDetails"][0]['Status']['MindDefence']):
    #                     party_id = (eval('get_party_list(token)'+battle.party_dict['treasure_physical_party']))
    #                     print(area2_id, "treasure_physical_party", party_id)
    #                 else:
    #                     party_id = (eval('get_party_list(token)'+battle.party_dict['treasure_magical_party']))
    #                     print(area2_id, "treasure_magical_party", party_id)
    #         battle.auto_battle(stage_id, party_id, token)
    #         time.sleep(5)
    #         if(battle.recover_background_action_potion(token) == 0):
    #             post_req(r"https://mist-production-api-001.mist-train-girls.com/api/Battle/DepartBackGroundAutoPlay", token)
    #             print(stage_id, "background autobattle completed", party_id)
    #             return 0
    #         else:
    #             print("do not have any potion")
    #             return 2
    area1_info = get_req(r'https://mist-production-api-001.mist-train-girls.com/api/Areas/' + str(area1_id) + r'/Difficulties', token)['r']
    area1_unlocked_diffculties = area1_info['UnlockDifficulty']
    area1_quests = area1_info['UnlockQuestIds']
    print(area1_id, "area uncloked quests id are", area1_quests)
    time.sleep(3)
    area1_quests_easy.insert(0, int(area1_quest_id_sample/1000)*1000 + 301)
    area1_quests_easy = []
    area1_quests_hard = []
    area1_quests_veryhard = []
    for i in area1_quests:
        if(i%1000 < 400):
            area1_quests_easy.append(i)
        elif(400 < i%1000 < 500):
            area1_quests_hard.append(i)
        elif(500 < i%1000):
            area1_quests_veryhard.append(i)
        else:
            print("未知的關卡", i)
            raise Exception("未知的關卡 "+str(i))
    if(len(area1_quests_veryhard) >= 5):
        stage_id = area1_quests_veryhard[-1]
    # 没有解锁hard关卡就选择第一关周回
    elif(len(area1_quests_veryhard) == 0):
        print("area1 has no veryhard quest can battle")
        stage_id = area1_quests_easy[-1]
    else:
        stage_id = area1_quests_veryhard[-1]
    party_id = (eval('get_party_list(token)'+battle.party_dict['treasure_magical_party']))
    for i in deckdata:
        if (i["Id"] == int((int(area1_quest_id_sample/1000)*1000 + 501)*1000) + 1):
            if(i["MDeckDetails"][0]['Status']['Defence'] < i["MDeckDetails"][0]['Status']['MindDefence']):
                party_id = (eval('get_party_list(token)'+battle.party_dict['treasure_physical_party']))
                print(area1_id, "treasure_physical_party", party_id)
            else:
                party_id = (eval('get_party_list(token)'+battle.party_dict['treasure_magical_party']))
                print(area1_id, "treasure_magical_party", party_id)
    # 宝藏任务周回战败 则尝试周回最低难度的关卡
    if(battle.auto_battle(stage_id, party_id, token) == 1):
        print("farm event",stage_id, "is too hard for farm") 
        battle.auto_battle(area1_quests_easy[-1], party_id, token)
        print(area1_quests_easy[-1], "is farmevent background autobattle", party_id)
    else:
        print(stage_id, "is farmevent background autobattle", party_id)
    time.sleep(5)
    if(battle.recover_background_action_potion(token) == 0):
        post_req(r"https://mist-production-api-001.mist-train-girls.com/api/Battle/DepartBackGroundAutoPlay", token)
        print(stage_id, "background autobattle completed", party_id)
        return 0
    else:
        print("do not have any potion")
        return 2