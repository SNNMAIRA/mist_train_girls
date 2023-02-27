from mist_train_girls_requests import post_req
from mist_train_girls_requests import post_jsonstring


def enegy_recharge(token):
    try:
        training_enegy_left = int(post_req(r"https://mist-production-api-001.mist-train-girls.com/api/Training/updateCheckPoint", token)['r']['TrainingInfoEnergyLeft'])
        print("training enegy left", training_enegy_left)
        restore_enegy = 144000 - training_enegy_left
        if(restore_enegy > 0):
            # 使用金币恢复能量
            url = r"https://mist-production-api-001.mist-train-girls.com/api/Training/chargeEnergy?useMoneyCount="+str(int(restore_enegy/100))
            new_enegy = post_jsonstring(url, token, '{}')
            print("new engegy restored", new_enegy )
        return 0
    except Exception:
        print("training enegy restore error")
        return 1
