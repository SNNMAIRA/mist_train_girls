from mist_train_girls_requests import get_req
from mist_train_girls_requests import post_req
import datetime

# file = open("./casino_log/{} poker.txt".format(str(datetime.datetime.now().strftime('%y-%m-%d %H-%M'))), 'a')
file = open("./casino_log/{} poker.txt".format(str(datetime.datetime.now().strftime('%y-%m-%d'))), 'a')


def now_cards(cards):
    now_cardlist = []
    for i in range(5):
        now_cardlist.append(cards[i*2:i*2+2])
    return now_cardlist


def sort_cards(cardlist):
    cards = cardlist.copy()
    for i in range(5):
        if(cards[i][1]) == "X":
            cards[i] = cards[i][:-1]
            cards[i] = cards[i] + "10"
        if(cards[i][1]) == "J":
            cards[i] = cards[i][:-1]
            cards[i] = cards[i] + "11"
        if(cards[i][1]) == "Q":
            cards[i] = cards[i][:-1]
            cards[i] = cards[i] + "12"
        if(cards[i][1]) == "K":
            cards[i] = cards[i][:-1]
            cards[i] = cards[i] + "13"
    for i in range(5):
        for j in range(i+1):
            if(int(cards[j][1:]) > int(cards[i][1:])):
                temp = cards[i]
                cards[i] = cards[j]
                cards[j] = temp
    print("SORTED", cards)
    return cards


def suit_count(sorted_cardlist):
    {0: 'O', 1: 'S', 2: 'D', 3: 'H', 4: 'C'}

    suit_list = [0, 0, 0, 0, 0]
    for i in range(5):
        if(sorted_cardlist[i][0] == "S"):
            suit_list[1] = suit_list[1] + 1
        if(sorted_cardlist[i][0] == "D"):
            suit_list[2] = suit_list[2] + 1
        if(sorted_cardlist[i][0] == "H"):
            suit_list[3] = suit_list[3] + 1
        if(sorted_cardlist[i][0] == "C"):
            suit_list[4] = suit_list[4] + 1
        if(sorted_cardlist[i][0] == "$"):
            suit_list[0] = suit_list[0] + 1
    # 返回最大相同花色數量 和最大花色類型
    return max(suit_list) + suit_list[0], suit_list.index(max(suit_list))


def number_count(sorted_cardlist):
    number_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(5):
        number_list[int(sorted_cardlist[i][1:])] = number_list[int(sorted_cardlist[i][1:])] + 1
    # 返回最大相同數字數量
    return max(number_list) + number_list[0], number_list.index(max(number_list))


def straight_count(sorted_cardlist):
    # 啊懶得寫了 是順子就返回5 不是就返回0
    straight = 0
    if(int(sorted_cardlist[0][1:]) != 0):
        if(int(sorted_cardlist[0][1:])+4 == int(sorted_cardlist[1][1:])+3 == int(sorted_cardlist[2][1:])+2 == int(sorted_cardlist[3][1:])+1 == int(sorted_cardlist[4][1:])):
            straight = 5
    else:
        if((int(sorted_cardlist[4][1:]) - int(sorted_cardlist[1][1:]) <= 4)):
            straight = 5
    # 返回最大連續數字數量
    return straight


def execute_suit(original_cardlist, max_suit_color):
    dict = {0: 'O', 1: 'S', 2: 'D', 3: 'H', 4: 'C'}
    change_list = []
    for i in range(5):
        if(original_cardlist[i][0] != dict[max_suit_color] and original_cardlist[i][0] != '$'):
            change_list.append(i)
    return change_list


def execute_number(original_cardlist, max_number_digital):
    dict1 = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'X', 11: 'J', 12: 'Q', 13: 'K'}
    dict2 = {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0, 'X': 0, 'J': 0, 'Q': 0, 'K': 0}
    change_list = []
    for i in range(5):
        dict2[original_cardlist[i][1]] = dict2[original_cardlist[i][1]] + 1
    for i in range(1, 14):
        if(dict2[dict1[i]] < 2):
            for j in range(5):
                if(dict1[i] == original_cardlist[j][1]):
                    change_list.append(j)
    return change_list


def execute_straight(original_cardlist):
    change_list = []
    return change_list


def execute_single(original_cardlist):
    change_list = []
    for i in range(5):
        if(original_cardlist[i][0] != "$"):
            change_list.append(i)
    return change_list


def casio_poker(token):
    try:
        current_casio_status = get_req(r"https://mist-production-api-001.mist-train-girls.com/api/Casino/GetCasinoTop", token)
        if(current_casio_status['r']["TodayCasinoCoinStatus"]["IsLockCoin"] is not False):
            print("already finished today's casino")
            return 0
        bet_begin = post_req(r"https://mist-production-api-001.mist-train-girls.com/api/Casino/Poker/Bet?type=2&betCoin=5000", token)
        original_cardlist = now_cards(str(bet_begin['r']))
        file.write(str(original_cardlist)+'起始手牌 \n')
        sorted_cardlist = sort_cards(original_cardlist)

        max_suit_count, max_suit_color = suit_count(sorted_cardlist)
        max_number_count, max_number_digital = number_count(sorted_cardlist)
        max_straight_count = straight_count(sorted_cardlist)
        discard_list = []
        if(max_suit_count == 5):
            discard_list = execute_suit(original_cardlist, max_suit_color)
        elif(max_straight_count == 5):
            discard_list = execute_straight(original_cardlist)
        elif(max_number_count >= 3):
            discard_list = execute_number(original_cardlist, max_number_digital)
        elif(max_suit_count == 4):
            discard_list = execute_suit(original_cardlist, max_suit_color)
        elif(max_number_count == 2):
            discard_list = execute_number(original_cardlist, max_number_digital)
        else:
            discard_list = execute_single(original_cardlist)

        poker_url = "https://mist-production-api-001.mist-train-girls.com/api/Casino/Poker/ChangeHand"
        if (len(discard_list) != 0):
            poker_url = "https://mist-production-api-001.mist-train-girls.com/api/Casino/Poker/ChangeHand?"
        for i in range(len(discard_list)):
            poker_url = poker_url + "&changeIndexes={}".format(discard_list[i])
        changed_cards_result = post_req(poker_url, token)
        file.write(str(now_cards(str(changed_cards_result['r']["Cards"])))+'改良手牌 \n')

        # 如果是上一次換牌后中了
        dict = {'0': 0, '1': 14, 'A': 14, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'X': 10, 'J': 11, 'Q': 12, 'K': 13}
        if(changed_cards_result['r']['RewardCoinCount'] != 0):
            reward_coin = 5000
            guess_card = dict[post_req(r"https://mist-production-api-001.mist-train-girls.com/api/Casino/Poker/DoubleUp/Start", token)['r'][1]]
            while (reward_coin != 0):
                file.write(str(guess_card)+'猜測的牌 \n')
                if(guess_card <= 8):
                    guess_result = post_req(r"https://mist-production-api-001.mist-train-girls.com/api/Casino/Poker/DoubleUp/Choose?choice=1", token)
                else:
                    guess_result = post_req(r"https://mist-production-api-001.mist-train-girls.com/api/Casino/Poker/DoubleUp/Choose?choice=2", token)
                if(int(guess_result['r']["RewardCoinCount"]) > 0 and int(guess_result['r']["RewardCoinCount"]) < 1000000):
                    guess_card = dict[guess_result['r']["DrawCard"][1]]
                elif(int(guess_result['r']["RewardCoinCount"]) > 1000000):
                    print("win amount is", int(guess_result['r']["RewardCoinCount"]))
                    file.write(str(int(guess_result['r']["RewardCoinCount"]))+'贏得賭幣 \n')
                    reward_coin = 0
                else:
                    reward_coin = 0
            current_casio_status = get_req(r"https://mist-production-api-001.mist-train-girls.com/api/Casino/GetCasinoTop", token)
            if(current_casio_status['r']["TodayCasinoCoinStatus"]["IsLockCoin"] is False):
                casio_poker(token)
            else:
                # casio_poker(token)
                file.write('今天贏麻了')
                print("casino finish")
                return 0
        else:
            return casio_poker(token)
    except Exception:
        print("casino poker gamble error")
        return 1
