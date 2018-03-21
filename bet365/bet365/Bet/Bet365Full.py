from Bet.Bet365 import Bet365
from FireFoxDriverTool.FireFoxDriver import FireFoxDriver, ByType
from pyquery import PyQuery as pq
import time, json
import userConfig
from MongoBetTool.MongoBet import MongoBet
from Balance.Balance import Balance
from LoggingTool.Logging import Logging
from MatchParseTool.MatchParse import MatchParse
from MatchOperationTool.MatchOperation import MatchOperation
from MailTool.Mail import Mail

class Bet365Full(Bet365):
    def __init__(self):
        super(Bet365Full, self).__init__(type=1)

    def procMatches(self):
        # print('满足条件的比赛顺序：','next_half-->next_half_combined_goals-->next_half_all_goals-->goals_distribution_time-->latest_goal_time-->handicap-->any_bet_succeed-->bet_times')
        print('目前进行的比赛数目：', self.all)
        print('目前关注的比赛数目：', len(self.collections))

        self.runnings.clear()
        self.runnings = {key: False for key in self.collections.keys()}

        for aMatch in self.allMatches():
            names = MatchParse.nameForMatch(aMatch)
            if MatchOperation.hasForbiddenMatch(names, 1) == True:
                continue

            md5 = MatchParse.md5ForNameOfMatch(aMatch)
            time_now = float(MatchParse.timeForMatch(aMatch))
            if md5 in self.collections:
                self.runnings[md5] = True

            # 如果进行中的比赛不在收藏中，则不解析其他的比赛信息 或者已经加入的赛前比赛
            if (time_now != 0 and md5 not in self.collections) or (time_now == 0 and md5 in self.collections):
                continue

            score = MatchParse.scoreForMatch(aMatch)
            handicap = MatchParse.fullHandicapForMatch(aMatch)
            odds = float(MatchParse.fullOddsForMatch(aMatch))
            # ratios = MatchParse.fullRatioForMatch(aMatch)
            all_goals = int(score.split(':')[0]) + int(score.split(':')[1]) if score != None else 0

            # 初步筛选比赛
            time_ok = (time_now >= userConfig.RULE_FULL['initial_minutes']['min'] and \
                       time_now <= userConfig.RULE_FULL['initial_minutes']['max'])
            handicap_ok = handicap in userConfig.RULE_FULL['initial_handicaps']

            if time_ok and handicap_ok:
            # if time_ok:
                matchDict = {
                    'parties_name': names,
                    'score': score,
                    'goals_time': [],
                    'times_betteds': {'3': False, '2':False},
                    'full_handicap': handicap,
                    'full_handicap_odds': odds,
                    'play_time': 0.0,
                    'start_time': None,
                    '_id': md5,
                    # 'ratio': ratio,
                    'league': self.league,
                    'all_goals': 0,
                    'win_goals': 0,
                    'half_rest': False,
                    'next_half': False,
                    'goal_cancel': False,
                    'any_bet_succeed': False,
                    'all_quick_goal_num':0,
                    'last_half_quick_goal_num':0,
                    'next_half_quick_goal_num':0,
                    'last_half_all_goals': 0,
                    'next_half_all_goals': 0,
                    'last_half_combined_goals':0,
                    'next_half_combined_goals':0,
                }

                #判断当前未收藏的比赛是否在ds中
                # if md5 not in self.collections and md5 in self.ds.fetch_all():
                if md5 not in self.collections:
                    self.collections[md5] = matchDict

            # 如果比赛正在进行且在收藏中
            if md5 in self.collections.keys() and time_now != 0:
                # 更新比赛开始的时间且加入数据库
                if self.collections[md5]['start_time'] == None:
                    if handicap in userConfig.RULE_FULL['initial_handicaps']:
                        odds_ok = (odds >= userConfig.RULE_FULL['initial_handicaps'][handicap]['min'] and \
                                   odds <= userConfig.RULE_FULL['initial_handicaps'][handicap]['max'])

                        if odds_ok:
                            self.mongo.saveMatch(userConfig.MONGO_TABLE_COLLECTIONS, self.collections[md5])
                        else:
                            self.collections.pop(md5)
                            continue
                    else:
                        self.collections.pop(md5)
                        continue

                    self.collections[md5]['start_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    if (self.mongo.saveMatch(userConfig.MONGO_TABLE_COLLECTIONS, self.collections[md5])):
                       pass

                # 是否是半场休息时间且删除不满足条件的比赛（包括删除数据库的比赛）
                if self.collections[md5]['play_time'] >= time_now and time_now == userConfig.RULE_FULL['half_time']:
                    #更新上半场休息判断和上半场所有的进球
                    self.collections[md5]['half_rest'] = True
                    self.mongo.saveMatch(userConfig.MONGO_TABLE_COLLECTIONS, self.collections[md5])
                    # if self.collections[md5]['last_half_all_goals'] not in userConfig.RULE_FULL['all_bets_info']['last_half_all_goals']:
                    #     self.mongo.deleteMatch(userConfig.MONGO_TABLE_COLLECTIONS, self.collections[md5])
                    #     self.collections.pop(md5)
                    #     continue

                #是否是进入下半场且保存下半场状态到数据库中
                if time_now != userConfig.RULE_FULL['half_time'] and self.collections[md5]['half_rest'] == True:
                    self.collections[md5]['half_rest'] = False
                    self.collections[md5]['next_half'] = True
                    self.mongo.saveMatch(userConfig.MONGO_TABLE_COLLECTIONS, self.collections[md5])

                # 更新当前的比赛时间
                self.collections[md5]['play_time'] = time_now

                #比赛进球或者进球取消
                if self.collections[md5]['score'] != score:  # 有进球的情况
                    self.collections[md5]['score'] = score

                    # 如果进球取消的情况
                    if self.collections[md5]['all_goals'] > all_goals:
                        self.collections[md5]['goal_cancel'] = True
                        self.collections[md5]['goals_time'].pop()
                    else:
                        goals_time = self.collections[md5]['goals_time']
                        quick_goal_interval = userConfig.RULE_FULL['quick_goal_interval']

                        #更新上半场合并进球的次数
                        if len(goals_time) != 0 and (time_now-goals_time[-1] <= quick_goal_interval) and self.collections[md5]['next_half'] == False:
                            self.collections[md5]['last_half_quick_goal_num'] += 1
                            self.collections[md5]['all_quick_goal_num'] += 1

                        #更新下半场合并进球的次数
                        if len(goals_time) != 0 and (time_now-goals_time[-1] <= quick_goal_interval) and self.collections[md5]['next_half'] == True:
                            self.collections[md5]['next_half_quick_goal_num'] += 1
                            self.collections[md5]['all_quick_goal_num'] += 1

                        self.collections[md5]['goals_time'].append(time_now)

                    # 更新上半场所有进球和合并进球
                    if self.collections[md5]['next_half'] == False:
                        self.collections[md5]['last_half_all_goals'] = all_goals
                        self.collections[md5]['last_half_combined_goals'] = all_goals - self.collections[md5]['last_half_quick_goal_num']

                    #更新下半场所有进球和合并进球
                    if self.collections[md5]['next_half'] == True:
                        self.collections[md5]['next_half_all_goals'] = all_goals - self.collections[md5]['last_half_all_goals']
                        self.collections[md5]['next_half_combined_goals'] = all_goals - self.collections[md5]['last_half_all_goals'] - self.collections[md5]['next_half_quick_goal_num']

                    #更新所有进球
                    self.collections[md5]['all_goals'] = all_goals
                    self.mongo.updateMatch(userConfig.MONGO_TABLE_COLLECTIONS, self.collections[md5])

                    win_goals = self.collections[md5]['win_goals']
                    # 如果进球取消且已经下注了，则删除sucesses表的记录，同时投注金额也要回滚
                    if self.collections[md5]['goal_cancel'] == True and all_goals == win_goals - 1:
                        self.collections[md5]['any_bet_succeed'] = False
                        betted_cancel = False
                        cancel_hint = '恼之， '
                        for (times, betted) in self.collections[md5]['times_betteds'].items():  # 投注回滚
                            if betted == True:  # 已经下注的则要回滚
                                self.balance.rollback(times)
                                betted_cancel = True
                                cancel_hint = cancel_hint + times + 'times '
                        if betted_cancel:
                            delete_ok = self.mongo.deleteMatch(userConfig.MONGO_TABLE_SUCCESSES, self.collections[md5])
                            save_ok = self.mongo.saveMatch(userConfig.MONGO_TABLE_COLLECTIONS, self.collections[md5])
                            if delete_ok and save_ok:
                                Logging.info('{}---{}'.format(cancel_hint, self.collections[md5]))
                    elif self.collections[md5]['goal_cancel'] == False and all_goals == win_goals:
                        self.collections[md5]['any_bet_succeed'] = True
                        betted_success = False
                        win_hint = '得之， '
                        for (times, betted) in self.collections[md5]['times_betteds'].items():  # 判断进球是否下注，且列出下注的倍数
                            if betted == True:
                                self.balance.win(times)
                                betted_success = True
                                win_hint = win_hint + times + '倍 '
                        if betted_success:  # 进球且已经下注，则增加记录
                            save_ok = self.mongo.saveMatch(userConfig.MONGO_TABLE_SUCCESSES, self.collections[md5])
                            delete_ok = self.mongo.deleteMatch(userConfig.MONGO_TABLE_COLLECTIONS,
                                                               self.collections[md5])
                            if delete_ok and save_ok:
                                Logging.info('{}---{}'.format(win_hint, self.collections[md5]))
                            continue

                print_need = False

                #是否是下半场
                if self.collections[md5]['next_half'] == False:
                    continue

                #进球数是否满足条件
                if all_goals not in userConfig.RULE_FULL['all_bets_info']['arleady_goals']:
                    continue

                # 根据第一个进球来判断选择哪种可能性
                infos_all = userConfig.RULE_FULL['all_bets_info']['arleady_goals'][all_goals]
                goals_time = self.collections[md5]['goals_time']
                first_goal_time = float(goals_time[0]) if len(goals_time) != 0 else 0

                if isinstance(infos_all, list):
                    for infos in infos_all:
                        is_possibility_ok = (first_goal_time >= infos['first_goal_times']['min'] and first_goal_time <= infos['first_goal_times']['max'])
                        if is_possibility_ok:
                            break

                    if is_possibility_ok == False:
                        print('{}, is_possibility_ok=no'.format(names)) if print_need else self.collections.pop(md5)
                        continue
                elif isinstance(infos_all, dict):
                    infos = infos_all

                #是否是快速进球的条件
                forbidden_quick_goal = infos.get('forbidden_quick_goal', False)
                if forbidden_quick_goal and self.collections[md5]['all_quick_goal_num'] > 0:
                    print('{}, forbidden_quick_goal=no'.format(names)) if print_need else self.collections.pop(md5)
                    continue

                #上半场进球是否满足条件
                last_half_goals_min = infos['last_half_goals']['min']
                last_half_goals_max = infos['last_half_goals']['max']
                last_half_goals = self.collections[md5]['last_half_all_goals']
                if (last_half_goals >= last_half_goals_min and last_half_goals <= last_half_goals_max) == False:
                    print('{}, last_half_goals=no'.format(names)) if print_need else self.collections.pop(md5)
                    continue

                # # 下半场进球是否满足条件
                # next_half_goals_min = infos['next_half_goals']['min']
                # next_half_goals_max = infos['next_half_goals']['max']
                # next_half_goals = self.collections[md5]['next_half_all_goals']
                # if (next_half_goals >= next_half_goals_min and next_half_goals <= next_half_goals_max) == False:
                #     print('{}, next_half_goals=no'.format(names)) if print_need else self.collections.pop(md5)
                #     continue


                # 最近进球时间是否满足条件
                goals_time = self.collections[md5]['goals_time']
                latest_goal_time = float(goals_time[-1]) if len(goals_time) != 0 else 0
                latest_goal_times_min = infos['latest_goal_times']['min']
                latest_goal_times_max = infos['latest_goal_times']['max']
                if (latest_goal_time >= latest_goal_times_min and latest_goal_time <= latest_goal_times_max) == False:
                    print('{}, latest_goal_time=no'.format(names)) if print_need else self.collections.pop(md5)
                    continue

                # 投注的进球数是否满足条件
                handicap_now_ok = (handicap != None and isinstance(handicap,str) and "," not in handicap and ((float(handicap) > all_goals) and (float(handicap) < all_goals + 1)))
                if handicap_now_ok == False:
                    print('names={},all_combined_goals->yes,latest_goal_time->yes,handicap={}->no'.format(names, handicap))
                    continue

                times_betted = None
                for (key, val) in self.collections[md5]['times_betteds'].items():
                    if odds >= float(key) and val == False:
                        times_betted = key
                        break

                #赔率是否满足条件
                if times_betted == None:
                    print('names={},all_combined_goals->yes,handicap->yes,latest_goal_time->yes,bet_times={}->no'.format(names,odds))
                    continue

                # 是否遵守投注过就不再投注的原则
                obey_any_success = userConfig.RULE_FULL['all_bets_info']['ready_bets'][times_betted]['obey_any_success']
                if obey_any_success == True and self.collections[md5]['any_bet_succeed'] == True:
                    print('names={},all_combined_goals->yes,handicap->yes,latest_goal_time->yes,bet_times->no, any_bet_succeed->no'.format(names))
                    continue

                target_achieved_ok = (self.balance.isTargetAchieved(times_betted) == False)
                if target_achieved_ok:
                    self.doPay(names, times_betted, all_goals)
                else:
                    print('names={}, target_achieved->no'.format(names))

        # 删除已经比赛完的
        for (md5_key, running) in self.runnings.items():
            if running == False and md5_key in self.collections:
                betted_lose = False
                lose_hint = '失之， '
                already_goals = self.collections[md5_key]['all_goals']
                win_goals = self.collections[md5_key]['win_goals']
                for (times, betted) in self.collections[md5_key]['times_betteds'].items():
                    if betted == True and already_goals < win_goals:
                        self.balance.lose(times)
                        betted_lose = True
                        lose_hint = lose_hint + times + 'times '

                delete_ok = self.mongo.deleteMatch(userConfig.MONGO_TABLE_COLLECTIONS, self.collections[md5_key])
                if delete_ok:
                    if betted_lose == True:
                        Logging.info('{}---{}'.format(lose_hint, self.collections[md5_key]))
                        # Mail.send(lose_hint, json.dumps(self.collections[md5_key], ensure_ascii=False))
                    else:
                        pass
                        # Logging.info('删除比赛---{}'.format(self.collections[md5_key]))
                self.collections.pop(md5_key)