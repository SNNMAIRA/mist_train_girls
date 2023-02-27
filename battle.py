from mist_train_girls_requests import get_req
from mist_train_girls_requests import post_req
from mist_train_girls_requests import post_jsonstring
import battle_extension
import time
# SkillRefId=102020063 对应MSkillViewModel.json下的一个技能 
# SkillCategory为1是攻击技能 2是治疗技能 3是buff/debuff/异常状态类技能 5是只能以自己为目标的技能 
# SkillType为1的是主动技能 2是释放大招 3是能力效果(宝珠 PT技能 Link效果 着装能力) 5是通常攻击 6是大招充能 7是队列的效果
# 所以只需要使用SkillCategory为1且SkillType为1的技能 目标一直选择Id最大的敌人就可以了
# BattleAutoSetting=0是手动战斗 1普攻自动 2限制自动 3全力自动
# failed reason 3次数不足 6体力不足 1未完成前置關卡
# 还要考虑战斗失败的情况 以后再写
# 注意到如果请求不合法 服务器***有時候***会再次发送当前的状态而不是返回400错误
party_dict= {
    "daily_party" : r"['r']['UParties'][0]['Id']",
    "treasure_physical_party" : r"['r']['UParties'][1]['Id']",
    "treasure_magical_party" : r"['r']['UParties'][2]['Id']",
    "altar_physical_party" : r"['r']['UParties'][3]['Id']",
    "altar_magical_party" : r"['r']['UParties'][4]['Id']",
    "regular_farm_physical_party" : r"['r']['UParties'][5]['Id']",
    "regular_farm_magical_party" : r"['r']['UParties'][6]['Id']",
    }


def giveup(token):
    post_jsonstring(r'https://mist-production-api-001.mist-train-girls.com/api/Battle/surrender', token, r'{"BattleAutoSetting":0,"BattleSpeed":2,"BattleSpecialSkillAnimation":1,"IsAutoSpecialSkill":false,"IsAutoOverDrive":false,"EnableConnect":false}')
    print("giveup previous battle")


def recover_action_point(token):
    current_action_point = get_req(r'https://mist-production-api-001.mist-train-girls.com/api/Users/Me', token)['r']['CurrentActionPoints']
    print('current_action_point is', current_action_point)
    recover_items = get_req(r'https://mist-production-api-001.mist-train-girls.com/api/UItems/ApRecoveryItems', token)
    small_potion = recover_items['r'][0]
    middle_potion = recover_items['r'][1]
    big_potion = recover_items['r'][2]
    event1_potion = recover_items['r'][-2]
    event2_potion = recover_items['r'][-1]
    print("have small potion", small_potion['Stock'], "middle potion", middle_potion['Stock'], "big potion", big_potion['Stock'], "event 1 potion", event1_potion['Stock'], "event 2 potion", event2_potion['Stock'])
    recover_point = 999 -current_action_point
    if(recover_point < 150):
        print("action point do not need recover")
        return 0
    if(battle_extension.is_potion_useable(event1_potion) != 0):
        event1_potion['Stock'] = 0
    if(battle_extension.is_potion_useable(event2_potion) != 0):
        event2_potion['Stock'] = 0
    if(event1_potion['Stock'] > int(recover_point/30)):
        post_req(r'https://mist-production-api-001.mist-train-girls.com/api/Users/recoverStamina/' + str(event1_potion['MItemId']) + '/' + str(int(recover_point/30)), token)
        print("use potion", event1_potion['MItemId'], "amount", (int(recover_point/30)))
    elif(event2_potion['Stock'] > int(recover_point/30)):
        post_req(r'https://mist-production-api-001.mist-train-girls.com/api/Users/recoverStamina/' + str(event2_potion['MItemId']) + '/' + str(int(recover_point/30)), token)
        print("use potion", event2_potion['MItemId'], "amount", (int(recover_point/30)))
    elif(small_potion['Stock'] > int(recover_point/30)):
        post_req(r'https://mist-production-api-001.mist-train-girls.com/api/Users/recoverStamina/' + str(small_potion['MItemId']) + '/' + str(int(recover_point/30)), token)
        print("use potion", small_potion['MItemId'], "amount", (int(recover_point/30)))
    elif(middle_potion['Stock'] > int(recover_point/90)):
        post_req(r'https://mist-production-api-001.mist-train-girls.com/api/Users/recoverStamina/' + str(middle_potion['MItemId']) + '/' + str(int(recover_point/90)), token)
        print("use potion", middle_potion['MItemId'], "amount", (int(recover_point/90)))
    elif(big_potion['Stock'] > int(recover_point/150)):
        post_req(r'https://mist-production-api-001.mist-train-girls.com/api/Users/recoverStamina/' + str(big_potion['MItemId']) + '/' + str(int(recover_point/150)), token)
        print("use potion", big_potion['MItemId'], "amount", (int(recover_point/150)))
    else:
        print("not enough potion")
        return 1
    return 0


def recover_background_action_potion(token):
    background_info = get_req(r"https://mist-production-api-001.mist-train-girls.com/api/Battle/GetCurrentBackGroundAutoPlaySetting", token)
    current_background_action_point = background_info['r']['CurrentApStainaTank']
    max_background_action_point = background_info['r']['MaxApStaminaTank']
    recover_point = max_background_action_point - current_background_action_point
    if(recover_point < 150):
        print("no need to recover background battle action point")
        return 0
    recover_items = background_info['r']['ApRecoveryItems']
    small_potion = recover_items[0]
    middle_potion = recover_items[1]
    big_potion = recover_items[2]
    event1_potion = recover_items[-2]
    event2_potion = recover_items[-1]
    if(battle_extension.is_potion_useable(event1_potion) != 0):
        event1_potion['Stock'] = 0
    if(battle_extension.is_potion_useable(event2_potion) != 0):
        event2_potion['Stock'] = 0
    if(event1_potion['Stock'] > int(recover_point/30)):
        post_jsonstring(r'https://mist-production-api-001.mist-train-girls.com/api/BackGroundAutoPlayStaminaTank/RecoverBackGroundAutoPlayStaminaTank', token, r'{"UseItems":[{"MItemId":' + str(event1_potion['MItemId']) + r',"Quantity":' + str(int(recover_point/30)) + r'}]}')
        print("background battle use potion", event1_potion['MItemId'], "amount", (int(recover_point/30)))
    elif(event2_potion['Stock'] > int(recover_point/30)):
        post_jsonstring(r'https://mist-production-api-001.mist-train-girls.com/api/BackGroundAutoPlayStaminaTank/RecoverBackGroundAutoPlayStaminaTank', token, r'{"UseItems":[{"MItemId":' + str(event2_potion['MItemId']) + r',"Quantity":' + str(int(recover_point/30)) + r'}]}')
        print("background battle use potion", event2_potion['MItemId'], "amount", (int(recover_point/30)))
    elif(small_potion['Stock'] > int(recover_point/30)):
        post_jsonstring(r'https://mist-production-api-001.mist-train-girls.com/api/BackGroundAutoPlayStaminaTank/RecoverBackGroundAutoPlayStaminaTank', token, r'{"UseItems":[{"MItemId":' + str(small_potion['MItemId']) + r',"Quantity":' + str(int(recover_point/30)) + r'}]}')
        print("background battle use potion", small_potion['MItemId'], "amount", (int(recover_point/30)))
    elif(middle_potion['Stock'] > int(recover_point/90)):
        post_jsonstring(r'https://mist-production-api-001.mist-train-girls.com/api/BackGroundAutoPlayStaminaTank/RecoverBackGroundAutoPlayStaminaTank', token, r'{"UseItems":[{"MItemId":' + str(middle_potion['MItemId']) + r',"Quantity":' + str(int(recover_point/90)) + r'}]}')
        print("background battle use potion", middle_potion['MItemId'], "amount", (int(recover_point/90)))
    elif(big_potion['Stock'] > int(recover_point/150)):
        post_jsonstring(r'https://mist-production-api-001.mist-train-girls.com/api/BackGroundAutoPlayStaminaTank/RecoverBackGroundAutoPlayStaminaTank', token, r'{"UseItems":[{"MItemId":' + str(big_potion['MItemId']) + r',"Quantity":' + str(int(recover_point/150)) + r'}]}')
        print("background battle use potion", big_potion['MItemId'], "amount", (int(recover_point/150)))
    elif((big_potion['Stock']*150 + middle_potion['Stock']*90 + small_potion['Stock']*30) <= recover_point):
        post_jsonstring(r'https://mist-production-api-001.mist-train-girls.com/api/BackGroundAutoPlayStaminaTank/RecoverBackGroundAutoPlayStaminaTank', token, 
        # {"UseItems":[{"MItemId":4,"Quantity":1},{"MItemId":917,"Quantity":1}]}
        r'{"UseItems":[{"MItemId":' + str(big_potion['MItemId']) + r',"Quantity":' + str(big_potion['Stock'])
        + r'},{"MItemId":' + str(middle_potion['MItemId']) + r',"Quantity":' + str(middle_potion['Stock'])
        + r'},{"MItemId":' + str(small_potion['MItemId']) + r',"Quantity":' + str(small_potion['Stock']) + r'}]}')
        print("background battle use all potion")
    elif((big_potion['Stock']*150 + middle_potion['Stock']*90) <= recover_point):
        post_jsonstring(r'https://mist-production-api-001.mist-train-girls.com/api/BackGroundAutoPlayStaminaTank/RecoverBackGroundAutoPlayStaminaTank', token, 
        r'{"UseItems":[{"MItemId":' + str(big_potion['MItemId']) + r',"Quantity":' + str(big_potion['Stock'])
        + r'},{"MItemId":' + str(middle_potion['MItemId']) + r',"Quantity":' + str(middle_potion['Stock']) + r'}]}')
        print("background battle use big and middle potion")
    elif((big_potion['Stock']*150) <= recover_point):
        post_jsonstring(r'https://mist-production-api-001.mist-train-girls.com/api/BackGroundAutoPlayStaminaTank/RecoverBackGroundAutoPlayStaminaTank', token, 
        r'{"UseItems":[{"MItemId":' + str(big_potion['MItemId']) + r',"Quantity":' + str(big_potion['Stock']) + r'}]}')
        print("background battle use big potion")
    else:
        print("background battle not enough potion")
        return 1
    return 0
    


def character_regular_attack_id(character):
    for i in character['Skills']:
        if(i['SkillType'] == 5):
            return i['Id']

# 注意这里返回0才是不可战斗的状态
def character_capability(character):
    if(character['HP'] <= 0):
        print(character['ID'], "is incapability")
        return 0
    for i in character['Auras']:
        if(i['SkillEffectType'] == 18):
            print(character['ID'], "is stun")
            return 0
        elif(i['SkillEffectType'] == 19):
            print(character['ID'], "is sleeping")
            return 0
        elif(i['SkillEffectType'] == 20):
            print(character['ID'], "is confusion")
            return 0
        elif(i['SkillEffectType'] == 22):
            print(character['ID'], "is paralysis")
            return 0
        elif(i['SkillEffectType'] == 23):
            print(character['ID'], "is slience")
            return 0
        elif(i['SkillEffectType'] == 24):
            print(character['ID'], "is charming")
            return 0
    return 1

# 返回1就是战败了
def is_battle_lose(character_list):
    flag = 1
    for i in character_list:
        if(i['HP'] > 0):
            flag = 0
            break
    return flag


def battle_commands(battle_info):
    now_turn = battle_info['Version']
    # 最大id的敌人作为当前目标
    target_id = battle_info['BattleState']['Enemies'][-1]['ID']
    command = ""
    for i in battle_info['BattleState']['Characters']:
        if(character_capability(i) == 0):
            continue
        command = command + r'{"UnitSerialId":' + str(i["ID"]) + r',"TargetId":' + str(target_id) + r',"CommandId":' + str(character_regular_attack_id(i)) + r',"IsOverDrive":false}'
        if(i["ID"] < 5):
            command = command + ','
    battle_command = r'{"Type":1,"Commands":[' + command + r'],"BattleSettings":{"BattleAutoSetting":0,"BattleSpeed":2,"BattleSpecialSkillAnimation":1,"IsAutoSpecialSkill":false,"IsAutoOverDrive":false,"EnableConnect":false},"IsSimulation":false,"Version":'+ str(now_turn) + '}'
    return battle_command


def auto_battle_commands(battle_info, all_characters_skills_list):
    now_turn = battle_info['Version']
    # 最大id的敌人作为当前目标
    target_id = battle_info['BattleState']['Enemies'][-1]['ID']
    command = ""
    command_list = battle_extension.current_use_skill(all_characters_skills_list, battle_info['BattleState']['Characters'])
    for i in battle_info['BattleState']['Characters']:
        if(character_capability(i) == 0):
            continue
        command = command + r'{"UnitSerialId":' + str(i["ID"]) + r',"TargetId":' + str(target_id) + r',"CommandId":' + str(command_list[(i["ID"]-1)]) + r',"IsOverDrive":false}'
        if(i["ID"] < 5):
            command = command + ','
    auto_battle_commands = r'{"Type":1,"Commands":[' + command + r'],"BattleSettings":{"BattleAutoSetting":0,"BattleSpeed":2,"BattleSpecialSkillAnimation":1,"IsAutoSpecialSkill":false,"IsAutoOverDrive":false,"EnableConnect":false},"IsSimulation":false,"Version":'+ str(now_turn) + '}'
    print("auto battle command send")
    return auto_battle_commands


def get_party_list(token):
    return get_req(r"https://mist-production-api-001.mist-train-girls.com/api/UParties/1", token)


def regular_attack_only_battle(quest_id, party_id, token):
    try:
        # party_id 是整形
        battle_status = post_req(r"https://mist-production-api-001.mist-train-girls.com/api/Battle/start/" + str(quest_id) + r"?uPartyId=" + str(party_id) + r"&rentalUUserId=null&isRaidHelper=null&uRaidId=null&raidParticipationMode=null", token)
        battle_id = battle_status['r']['BattleId']
        print(quest_id, "regulat attack party_id is", party_id)
        time.sleep(5)
        while(len(battle_status['r']['BattleState']['Enemies']) > 0):
            battle_command = battle_commands(battle_status['r'])
            battle_status = post_jsonstring(r"https://mist-production-api-001.mist-train-girls.com/api/Battle/attack/" + str(battle_id), token, battle_command)
            time.sleep(10)
            print("turn number",battle_status['r']['BattleState']['TurnNumber'], "wave number",battle_status['r']['BattleState']['WaveNumber'])
        result = post_req(r'https://mist-production-api-001.mist-train-girls.com/api/Battle/victory?isSimulation=false', token)
        print(quest_id, "clear second is", result['r']['ClearSec'])
        print(quest_id, "clear experence is", result['r']['PlayerLevel']['PlayerExperienceReword'])
        return 0
    except Exception:
        print(quest_id, "quest error party is", party_id)
        return 1


def daily_battle(token):
    try:
        # party_id 是整形
        party_id = (eval('get_party_list(token)'+party_dict['daily_party']))
        print("party_id is", party_id)
        # 201001101金币第一关 202001101经验第一关
        get_req(r"https://mist-production-api-001.mist-train-girls.com/api/Quests/201001101/prepare/"+str(party_id), token)
        can_start = post_req(r"https://mist-production-api-001.mist-train-girls.com/api/Battle/canstart/201001101?uPartyId="+str(party_id), token)
        while(can_start['r']['CanStart'] is True):
            regular_attack_only_battle(201001101, party_id, token)
            time.sleep(5)
            can_start = post_req(r"https://mist-production-api-001.mist-train-girls.com/api/Battle/canstart/201001101?uPartyId="+str(party_id), token)
        print("201001101", "start battle failed reason is", can_start['r']['FaildReason'])
        get_req(r"https://mist-production-api-001.mist-train-girls.com/api/Quests/202001101/prepare/"+str(party_id), token)
        can_start = post_req(r"https://mist-production-api-001.mist-train-girls.com/api/Battle/canstart/202001101?uPartyId="+str(party_id), token)
        while(can_start['r']['CanStart'] is True):
            regular_attack_only_battle(202001101, party_id, token)
            time.sleep(5)
            can_start = post_req(r"https://mist-production-api-001.mist-train-girls.com/api/Battle/canstart/202001101?uPartyId="+str(party_id), token)
        print("202001101", "start battle failed reason is", can_start['r']['FaildReason'])
        print("daily battle completed")
        return 0 
    except Exception:
        print("daily battle error")
        return 1

# 返回1表示战斗失败
def auto_battle(quest_id, party_id, token):
    try:
        print(quest_id, "is quest party", party_id)
        get_req(r"https://mist-production-api-001.mist-train-girls.com/api/Quests/" + str(quest_id) + r"/prepare/"+str(party_id), token)
        can_start = post_req(r"https://mist-production-api-001.mist-train-girls.com/api/Battle/canstart/" + str(quest_id) + r"?uPartyId="+str(party_id), token)
        if(can_start['r']['CanStart'] is not True):
            print(quest_id, "start battle failed reason is", can_start['r']['FaildReason'])
            raise Exception("auto battle error") 
        battle_status = post_req(r"https://mist-production-api-001.mist-train-girls.com/api/Battle/start/" + str(quest_id) + r"?uPartyId=" + str(party_id) + r"&rentalUUserId=null&isRaidHelper=null&uRaidId=null&raidParticipationMode=null", token)
        time.sleep(5)
        battle_id = battle_status['r']['BattleId']
        all_characters_skills_list = battle_extension.all_skills_list(battle_status['r']['BattleState']['Characters'])
        while(len(battle_status['r']['BattleState']['Enemies']) > 0):
            battle_command = auto_battle_commands(battle_status['r'], all_characters_skills_list)
            battle_status = post_jsonstring(r"https://mist-production-api-001.mist-train-girls.com/api/Battle/attack/" + str(battle_id), token, battle_command)
            time.sleep(11)
            print("turn number",battle_status['r']['BattleState']['TurnNumber'], "wave number",battle_status['r']['BattleState']['WaveNumber'])
            if(is_battle_lose(battle_status['r']['BattleState']['Characters']) == 1):
                result = post_req(r'https://mist-production-api-001.mist-train-girls.com/api/Battle/defeat?isSimulation=false', token)
                print(quest_id, "is falled party is", party_id)        
                return 1
        result = post_req(r'https://mist-production-api-001.mist-train-girls.com/api/Battle/victory?isSimulation=false', token)
        print(quest_id, "clear second is", result['r']['ClearSec'])
        print(quest_id, "clear experence is", result['r']['PlayerLevel']['PlayerExperienceReword'])
        return 0
    except Exception:
        print(quest_id, "battle error", party_id)
        raise Exception("battle error")
