from mist_train_girls_requests import get_req
from mist_train_girls_requests import post_req


def game_login(token):
    post_req(r"https://mist-production-api-001.mist-train-girls.com/api/Login", token)
    print("game login success")
    autoplay_progress = get_req(r"https://mist-production-api-001.mist-train-girls.com/api/Battle/GetBackGroundAutoPlayProgress", token)
    if(autoplay_progress['r']['IsComplete'] is True):
        print("battle completed")
        post_req(r"https://mist-production-api-001.mist-train-girls.com/api/Battle/CompleteBackGroundAutoPlay", token)
        print("confirm finishied backgound autobattle")
        return 0
    elif(autoplay_progress['r']['IsComplete'] is False):
        print("in battling")
        return 1
    else:
        print("there is no process bakeground battle")
        return 0