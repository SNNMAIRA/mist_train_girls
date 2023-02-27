import json
import requests
import time
import datetime
proxies = {
  "http": "http://127.0.0.1:7890",
  "https": "http://127.0.0.1:7890",
  "ftp": "ftp://127.0.0.1:7890"
}

def getfile(address,filename):
    try:
        # 设置stream = True 请求头中将会设置好headers['Transfer-Encoding'] = 'chunked' 以这种方式指定chunked传输编码
        # 'Transfer-Encoding'只用于逐跳的标头 只使用在单次传输的时候 不会像端到端标头一样("这类标头必须被传输到最终的消息接收者:请求的服务器或者响应的客户端")
        r = requests.get(address, stream = True, proxies = proxies)
        if r.status_code==requests.codes.ok:
            with open(filename, "wb") as file:
                # 这个就是和steam = True一起用的 流式读取respond
                for block in r.iter_content(chunk_size = 1024):
                    if block: 
                        file.write(block)
            file.close()
    # 没有获取到列表也没关系 不一定要用最新的
    except Exception:
        print(filename, "list refresh error")
        pass

getfile('https://assets.mist-train-girls.com/production-client-web-static/MasterData/MSkillViewModel.json','./MSkillViewModel.json')
getfile('https://assets.mist-train-girls.com/production-client-web-static/MasterData/MApRecoveryItemViewModel.json','./MApRecoveryItemViewModel.json')
getfile('https://assets.mist-train-girls.com/production-client-web-static/MasterData/MWorldViewModel.json','./MWorldViewModel.json')
with open('./MSkillViewModel.json','r', encoding='UTF-8') as f:
    skilldata=json.loads(f.read())
with open('./MApRecoveryItemViewModel.json','r', encoding='UTF-8') as f:
    potiondata=json.loads(f.read())
with open('./MWorldViewModel.json','r', encoding='UTF-8') as f:
    worlddata=json.loads(f.read())


def is_potion_useable(potion_id):
    for i in potiondata:
        if(i["MItemId"] == potion_id['MItemId']):        
            now_time = datetime.datetime.now()
            if(time.strftime('%z')[0]) == '-':
                min = int('-'+time.strftime('%z')[3:])
            else:
                min = int(time.strftime('%z')[3:])
            # 這裏要快三分鐘 避免剛好過期的情況
            jp_time = now_time - datetime.timedelta(hours=(int(time.strftime('%z')[0:3])-9), minutes=(min-3))
            if(jp_time < datetime.datetime.strptime(i['EndDate'], "%Y-%m-%dT%H:%M:%S")):
                print(potion_id['MItemId'], "potion is not expired")
                return 0
            else:
                print(potion_id['MItemId'], "potion is expired")
                return 1
    print(potion_id['MItemId'], "can not find potion")
    return 1
    


# 注意这里的reference_id是整形 也不同于直接的技能id
def skill_useable(skill_reference_id):
    # 技能可以使用则返回0 不能用返回1
    for i in skilldata:
        if(i["Id"] == skill_reference_id and i["SkillCategory"] == 1 and i["SkillType"] == 1):
            # print(i["Description"], i["Name"])
            return 0
    return 1


def character_useable_skill_list(character):
    skill_list = []
    for i in character['Skills']:
        if(i['SkillType'] == 1):
            if((skill_useable(i['SkillRefId']) == 0) and (i['IsCommandSkill'] == True)):
                skill_list.append({'skill_id':i['Id'],'skill_cost':i['SP']})
        if(i['SkillType'] == 5 and (i['IsCommandSkill'] == True)):
            skill_list.append({'skill_id':i['Id'],'skill_cost':i['SP']})
    return skill_list


def sort_skill_list(skill_list):
    sorted_list = []
    flag = 0
    for i in range(len(skill_list)):
        flag = 0
        for j in range(len(sorted_list)):
            if(sorted_list[j]['skill_cost'] > skill_list[i]["skill_cost"]):
                flag = 1
                sorted_list.insert(j, skill_list[i])
                break
        if(flag == 0):
            sorted_list.insert(len(sorted_list), skill_list[i])
    sorted_list.reverse()
    return sorted_list


def all_skills_list(character_list):
    all_skills = []
    for i in character_list:
        all_skills.append(sort_skill_list(character_useable_skill_list(i)))
    return all_skills


def current_use_skill(characters_skills_list, characters):
    use_skill_list = []
    for i in range(len(characters_skills_list)):
        for j in characters_skills_list[i]:
            if(j['skill_cost'] <= characters[i]['SP']):
                use_skill_list.append(j['skill_id'])
                break
    return use_skill_list