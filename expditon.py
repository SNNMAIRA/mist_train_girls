from mist_train_girls_requests import get_req
from mist_train_girls_requests import post_jsonstring
import datetime
import time

# 只有出擊後存在結果的遠征隊列才會自動操作 如果隊列完全空閑(不處在遠征完成的狀態)則不會操作
def departure_expedition(token):
    try:
        now_time = datetime.datetime.now()
        if(time.strftime('%z')[0]) == '-':
            min = int('-'+time.strftime('%z')[3:])
        else:
            min = int(time.strftime('%z')[3:])
        # 考虑到时间误差 最多误差快三分钟 也就是当前时间换日本时间会比真正的时间慢三分钟
        jp_time = now_time - datetime.timedelta(hours=(int(time.strftime('%z')[0:3])-9), minutes=(min+3))
        departure_list = []
        expedition_info = (get_req(r"https://mist-production-api-001.mist-train-girls.com/api/Expeditions", token))
        for i in expedition_info['r']:
            # completed_time = datetime.datetime.strptime(r"2023-02-18T23:14:44", "%Y-%m-%dT%H:%M:%S")
            if(jp_time > datetime.datetime.strptime(i['CompletedAt'], "%Y-%m-%dT%H:%M:%S")):
                # 注意這裏加入list的id會是整形
                departure_list.append(i['Id'])
        if(len(departure_list) == 0):
            print("no team can departure expedtion")
            return 0
        print("able to departure", departure_list)
        post_jsonstring(r"https://mist-production-api-001.mist-train-girls.com/api/Expeditions/completeAll", token, '{"uExpeditionIds":'+str(departure_list)+'}')
        time.sleep(1)
        post_jsonstring(r"https://mist-production-api-001.mist-train-girls.com/api/Expeditions/departAll", token, '{"uExpeditionIds":'+str(departure_list)+'}')
        print("expedition departure finished", departure_list)
        return 0
        # 字符串转换成时间 这里的格式要和上边转换得到的一致
    except Exception:
        print("expedition departure error")
        return 1
