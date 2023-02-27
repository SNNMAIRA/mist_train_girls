from mist_train_girls_requests import post_req

def free_gacha(token):
    try:
        post_req(r"https://mist-production-api-001.mist-train-girls.com/api/UGachas/3/roll/5", token)
        print("daily free gacha success")
    except Exception:
        print("already finished daily free gacha")
    return 0
