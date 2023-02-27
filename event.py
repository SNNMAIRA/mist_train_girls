import treasure_event
import altar_event
import farm_event
from mist_train_girls_requests import get_req
import time
import datetime
# Raid活动:类型7 高铁活动:类型9 宝藏任务:类型8 祭坛任务:类型10 


def event_list(token):
    now_time = datetime.datetime.now()
    if(time.strftime('%z')[0]) == '-':
        min = int('-'+time.strftime('%z')[3:])
    else:
        min = int(time.strftime('%z')[3:])
    # 怕活动打不完 多准备二个小时
    jp_time = now_time - datetime.timedelta(hours=(int(time.strftime('%z')[0:3])-11), minutes=(min))
    event_list = get_req(r'https://mist-production-api-001.mist-train-girls.com/api/Events', token)['r']
    playable_list = []
    for i in event_list:
        if(i['EventType'] == 7 or i['EventType'] == 9 or i['EventType'] == 8 or i['EventType'] == 10):
            playable_list.append(i)
    for i in playable_list:
        print(i['MEventId'], end=' ')
    print("are now playable events")
    for i in playable_list:
        if(jp_time > datetime.datetime.strptime(i['EventEndDate'], "%Y-%m-%dT%H:%M:%S")):
            print(i['MEventId'], "event is not playable")
        else:
            # 注意这里高铁任务返回event world id
            print(i['MEventId'], "is current event")
            if(i['EventType'] == 9):
                return i['MWorldIds'][0],i['EventType']
            return i['MEventId'],i['EventType']


# Raid:类型7 高铁活动:类型9 宝藏任务:类型8 祭坛任务:类型10
def execute_event(token):
    event_id, event_type =  event_list(token)
    if(event_id is None):
        print("當前沒有可使用的活動")
        return 0
    try:
        # 這裏只是把活動未完成的關卡打一遍 之後自動周會還是需要再調用一次別的方法
        if(event_type == 8):
            treasure_event.treasure_event(event_id, token)
        elif(event_type == 10):
            altar_event.altar_event(event_id, token)
        # 注意高铁任务要传event_world_id 
        elif(event_type == 9):
            farm_event.farm_event(event_id, token)
        else:
            print("未知的活動類型")
            pass
    except Exception:
        print("event stage clear error, try farm this event")
        pass
    # 這裏負責自動周回活動關卡
    if(event_type == 8):
        treasure_event.treasure_background(event_id, token)
    # 注意祭坛活动传递的参数是关卡ID不是活动ID 101002309:2-5
    elif(event_type == 10):
        altar_event.altar_background(101002309, token)
    elif(event_type == 9):
        farm_event.farm_background(event_id, token)
    else:
        print("未知的活動類型")
        pass
    return 0