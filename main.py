# 使用3.8以上版本的python 进行字典迭代反转
# 讨伐任务的id变成了202000030 素材任务的id变成了202000033 原因暂不清楚
import mist_train_girls_login
import login
import gacha
import training
import casino
import expditon
import battle
import mission
import time
import event
import sys
# 如果CompletedAt==Null就是任务没完成 Count=0就是该任务的计数
# 每周 十次讨伐任务MMissionId=202000026 十次素材收集关卡MMissionId=202000031 购买一次物品MMissionId=202000048
# 讨伐任务书 "Id":95576498,"MItemId":84
# 沉默的SkillEffectType=23 魅惑的SkillEffectType=24 混乱的SkillEffectType=20
# 睡眠的SkillEffectType=19 麻痹的SkillEffectType=22 眩晕的的SkillEffectType=18 SerialAuraId不是固定的
# 沉默并不会发送普通攻击的数据包 沉默时该角色完全不会发送任何战斗指令
# 上面的异常状态都不用发送战斗指令
# 使用前先修改這裏的DMM賬號和密碼
try:
    token = mist_train_girls_login.get_mist_trains_girls_token("braveteen@outlook.com", "qpwoeiu12345")
except Exception:
    print("can not access the game")
    sys.exit()
try:
    battling = login.game_login(token)
except Exception:
    print("login fail")
    sys.exit()
training.enegy_recharge(token)
time.sleep(5)
gacha.free_gacha(token)
time.sleep(5)
expditon.departure_expedition(token)
time.sleep(5)
#  1表示正在副官戰鬥 2表示體力不足
try:
    if(battling == 0):
        battle.giveup(token)
        # 不能恢復體力就不戰鬥
        if(battle.recover_action_point(token) != 0):
            battling = 2
except Exception:
    print("battle fail")
    sys.exit()
# 日常任務的戰鬥即使體力不足也要嘗試
if(battling != 1):
    battle.daily_battle(token)
mission.weekly_mission_clear(token)
mission.receive_mission(token)
time.sleep(5)
try:
    if(battling == 0 ):
        event.execute_event(token)
except Exception:
    print("event error")
    sys.exit()
casino.casio_poker(token)