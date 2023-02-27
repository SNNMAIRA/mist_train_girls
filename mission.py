from mist_train_girls_requests import post_req
from mist_train_girls_requests import get_req
from battle import get_party_list
import time
import battle


def daily_mission(token):
    try:
        post_req(r'https://mist-production-api-001.mist-train-girls.com/api/SendRewards/category/1?isNextMissionComplete=true', token)
        print("daily mission reward receive")
        return 0
    except Exception:
        print("daily mission receive error")
        return 1


def weekly_mission(token):
    try:
        post_req(r'https://mist-production-api-001.mist-train-girls.com/api/SendRewards/category/2?isNextMissionComplete=true', token)
        print("weekly mission reward receive")
        return 0
    except Exception:
        print("weekly mission receive error")
        return 1


def event_mission(token):
    try:
        post_req(r'https://mist-production-api-001.mist-train-girls.com/api/SendRewards/category/5?isNextMissionComplete=true', token)
        print("event mission reward receive")
        return 0
    except Exception:
        print("event mission receive error")
        return 1


def receive_mission(token):
    try:
        daily_mission(token)
        time.sleep(1)
        weekly_mission(token)
        time.sleep(1)
        event_mission(token)
        time.sleep(1)
        daily_mission(token)
        time.sleep(1)
        weekly_mission(token)
        time.sleep(1)
        print("all mission receive success")
        return 0
    except Exception:
        print("mission reward error")
        return 1


def weekly_material(token):
    party_id = (eval('get_party_list(token)'+battle.party_dict['regular_farm_magical_party']))
    for i in range(10):
        battle.auto_battle(208001101,  party_id, token)
        time.sleep(5)
    print("weekly material is completed")
    return 0


def weekly_shopping(token):
    item_id = 7708050
    daily_shop_items = get_req(r"https://mist-production-api-001.mist-train-girls.com/api/Markets/DailyShop", token)['r']['Items']
    for i in daily_shop_items:
        if(i['HasPurchased'] == False):
            item_id = i['Id']
            break
        elif(i['MDailyShopFrameId'] >= 12):
            print("daily shop has not items puchaseable ")
            return 1
    post_req(r"https://mist-production-api-001.mist-train-girls.com/api/Markets/DailyShopItems/" + str(item_id) + r"/purchase", token)
    print("purchase item id is", item_id)
    print("weekly shopping is completed")
    return 0


def weekly_raid(count, token):
    ticket = 0
    count = 10 - count
    print("raid quest need to clear times", count)
    items = get_req(r'https://mist-production-api-001.mist-train-girls.com/api/UItems', token)['r']
    for i in items:
        if(i['MItemId'] == 84):
            ticket = i['Stock']
            break
    print("have approval ticket count is", count)
    if(ticket >= count):
        ticket = count
    else:
        print("do not have enough tickets for weekly raid")
        return 1
    party_id = (eval('get_party_list(token)'+battle.party_dict['regular_farm_magical_party']))
    for i in range(count):
        battle.auto_battle(210024110,  party_id, token)
        time.sleep(5)
    print("weekly raid is completed")
    return 0


def weekly_mission_clear(token):
    # try:
    mission_list = get_req(r'https://mist-production-api-001.mist-train-girls.com/api/GetUMissionProgresses', token)['r']
    for i in mission_list:
        if(i['MMissionId'] == 202000048):
            if(i['CompletedAt'] == None):
                print("weekly shopping mission is incompleted")
                weekly_shopping(token)
            else:
                print("already completed weekly shopping mission")
        # 讨伐任务的id变成了202000030 素材任务的id变成了202000033
        elif(i['MMissionId'] == 202000026):
            if(i['CompletedAt'] == None):
                print("weekly raid mission is incompleted")
                weekly_raid(i['Count'], token)
            else:
                print("already completed weekly raid mission")
        elif(i['MMissionId'] == 202000031):
            if(i['CompletedAt'] == None):
                print("weekly material mission is incompleted")
                weekly_material(token)
            else:
                print("already completed weekly material mission")
    return 0
    # except Exception as e:
    #     print(e)
    #     print("weekly mission error")
    #     return 1
