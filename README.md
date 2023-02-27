
# :sparkles: 迷雾列车少女:train2: 自动化 :sparkles:

这是一款运行在Python环境下的迷雾列车少女游戏自动化程序。它可以完全自动地完成游戏中的一些任务，包括日常任务的金币和经验关卡，活动关卡，寶藏活動，祭壇BOSS，高铁活动等。

## 安装

运行本程序需要安装以下库：

- [Selenium](https://www.selenium.dev/)
- [SeleniumWire](https://selenium-wire.readthedocs.io/en/latest/)

此外，还需要配置环境变量，使其能够调用Chrome的webdriver与Selenium进行交互。请选择适合自己的[ChromeDriver版本](https://sites.google.com/a/chromium.org/chromedriver/downloads)。

## 使用

1. 修改`main.py`里配置的dmm账号信息和`mist_train_girls_login.py`里配置chrome用户文件位置
2. 配置`mist_train_girls_login.py`和`mist_train_girls_requests.py`里的proxy信息
3. 使用Python 3.8以上版本运行`main.py`

## 注意事项

- 此程序适合养老但不适合练新号
- 不要使用会在战斗中永久改变自身技能的角色
- 日常任务的金币和经验关卡由第一组的第一队负责处理
- 活動關卡會自動判斷關卡敵人的抗性類型選擇隊伍
- 寶藏活动由第一組的第二隊負責物理，第三隊魔法
- 宝藏任务胜利则周回VH1-5关卡刷武器 战败则周回难度最低的1-1
- 祭壇BOSS第一組第四隊物理，第五隊魔法
- 如果1~30层出现战败 或者超过30层 则周回2-5
- 高铁活动第一组第六队物理，第七队魔法
- 战斗逻辑模拟全力的auto模式 但不会使用治疗技能
- 找出当前满足当前SP需求的最高费攻击技能，选择最前排敌人为目标

## 关于

本程序基于[MIT协议](https://en.wikipedia.org/wiki/MIT_License)开源，请随意编辑和转载，欢迎提出Issues和Pull Request。
