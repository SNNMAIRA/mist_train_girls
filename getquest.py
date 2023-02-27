import os
import shutil
import json
import requests
proxies = {
  "http": "http://127.0.0.1:7890",
  "https": "http://127.0.0.1:7890",
  "ftp": "ftp://127.0.0.1:7890"
}
def getfile(address,filename):
    # 设置stream = True 请求头中将会设置好headers['Transfer-Encoding'] = 'chunked' 以这种方式指定chunked传输编码
    # 'Transfer-Encoding'只用于逐跳的标头 只使用在单次传输的时候 不会像端到端标头一样("这类标头必须被传输到最终的消息接收者:请求的服务器或者响应的客户端")
    r = requests.get(address, stream = True, proxies=proxies)
    if r.status_code==requests.codes.ok:
        with open(filename, "wb") as file:
            # 这个就是和steam = True一起用的 流式读取respond
            for block in r.iter_content(chunk_size = 1024):
                if block: 
                    file.write(block)
def enemy(deckdata,idno):
    for k in deckdata:
        if str(k['Id'])[:-3]==idno:
            print ('wave')
            for enemy in k['MDeckDetails']:
                print (enemy['Status'])
                print (enemy['ConditionResistGroup'])
                print (enemy['AttributeResistGroup'])
                enymyid=enemy['MEnemyId']
                
                prtskill(enymyid,enymydata,skilldata)
                for sk in enemy['AdditionalSkills']:
                    for i in skilldata:
                        if sk['MSkillId']==i['Id']:
                            print (i['Name']+'\t'+i['Description'])
                            break
            if len(k['MDeckDetails']) >1:
                array=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],]
                for i in range(len(k['MDeckDetails'])):
                    if k['MDeckDetails'][i]['IsBoss']==True:
                        array[k['MDeckDetails'][i]['Y']][4-k['MDeckDetails'][i]['X']]='B'
                        enymyid=k['MDeckDetails'][i]['MEnemyId']
                    else:
                        array[k['MDeckDetails'][i]['Y']][4-k['MDeckDetails'][i]['X']]=i+1
                for i in array:
                    print(i)
    return enymyid
def prtskill(enymyid,enymydata,skilldata):
    for e in enymydata:
        if e['Id']==enymyid:
            print(e['Name']+'\t'+race[e['Race']])
            for sk in e['MSkills']:
                for i in skilldata:
                    if sk['MSkillId']==i['Id']:
                        print (i['Name']+'\t'+i['Description'])
                        break
            for shields in e['MEnemyShields']:
                print(shields['ShieldType'])
                print(shields['BreakConditionDescription'])
                print('turn\t'+str(shields['RestoreTurn']))

                for i in skilldata:
                    if shields['ShieldMSKillId']==i['Id']:
                        print ('shield\t'+i['Name']+'\t'+i['Description'])
                        break
                for i in skilldata:
                    if shields['BreakMSkillId']==i['Id']:
                        print ('break\t'+i['Name']+'\t'+i['Description'])
                        break 
            break

        
def findid(intid):
    idno=str(intid)
    for i in data:
        if str(i['Id'])==idno:
            print(idno)
            print(i['RecommendOffenceAttribute'])
            enymyid=enemy(deckdata,idno)
            print(enymyid)
            prtskill(enymyid,enymydata,skilldata)

                    

                            
                
getfile('https://assets.mist-train-girls.com/production-client-web-static/MasterData/MQuestViewModel.json','./MQuestViewModel.json')
getfile('https://assets.mist-train-girls.com/production-client-web-static/MasterData/MDeckViewModel.json','./MDeckViewModel.json')
getfile('https://assets.mist-train-girls.com/production-client-web-static/MasterData/MEnemyViewModel.json','./MEnemyViewModel.json')
getfile('https://assets.mist-train-girls.com/production-client-web-static/MasterData/MSkillViewModel.json','./MSkillViewModel.json')
race={1:'無機',2:'植物',3:'妖精',4:'悪魔',5:'不死',6:'妖怪',7:'幽体',8:'海獣',9:'怪鳥',10:'魔獣',11:'害虫',12:'人間'}
with open('./MSkillViewModel.json','r', encoding='UTF-8') as f:
    skilldata=json.loads(f.read())
with open('./MEnemyViewModel.json','r', encoding='UTF-8') as f:
    enymydata=json.loads(f.read())
with open('./MQuestViewModel.json','r', encoding='UTF-8') as f:
    data=json.loads(f.read())
with open('./MDeckViewModel.json','r', encoding='UTF-8') as f:
    deckdata=json.loads(f.read())
for i in data:
    try:
        for j in i['QuestReward']['MRewards']:
            if j['ItemId']==182:
                if str(i['Id'])[-2:]=='35'and i['Id'] >303028135:#findid(301111701)
                    idno=str(i['Id'])
                    print(idno)
                    print(i['RecommendOffenceAttribute'])
                    enymyid=enemy(deckdata,idno)


                    

                            
    except:
        pass
                

    
