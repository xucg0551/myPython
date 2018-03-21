MONGO_URL = 'localhost'
MONGO_DB_FULL = 'bet365_full'
MONGO_DB_HALF = 'bet365_half'
MONGO_DB_DSFOOTBALL = 'dsfootball'

MONGO_TABLE_COLLECTIONS = 'collections'
MONGO_TABLE_BETS = 'bets'
MONGO_TABLE_SUCCESSES = 'successes'
MONGO_TABLE_BALANCE = 'balance'

URL = 'https://www.7788365365.com/#/HO/'
# URL = 'https://www.563488.com/?&cb=10326411784#/HO/'
# URL = 'https://www.653-288.com/#/HO/'
refreshMin = 0
isChromeDriver = True
SpiderInterval = 3
ItemExchangeInterval = 2*60
BetSportItem = '足球'
BetSport = '滚球盘'
AsiaHalfItem = '上半場亞洲盤'
# ForbiddenLeagues_Half = ['80分钟', '19', '20', '女', '英格兰', '苏格兰', '威尔士', '爱尔兰', '巴西', '以色列', '阿根廷', '葡萄牙', '西班牙', '法国', '意大利', '德国', '伊朗', '哥斯达黎加', '希腊', '阿联酋 - 超级联赛', '香港超级联赛','阿尔及利亚杯', '欧洲友谊赛']
ForbiddenLeagues_Half = ['80分钟', '19', '20', '女']
ForbiddenMatches_Half = ['19', '20', '女']

ForbiddenLeagues_Full = ['80分钟', '19', '20', '女子']
ForbiddenMatches_Full = ['19', '20', '女']

# full_lgt_min = 45
# full_lgt_max = 75
# full_lgt_max_1 = 80


RULE_FULL = {
    # 'initial_handicaps':{'3.0,3.5':{'min':1.5, 'max':1.95}, '3.5':{'min':1.7, 'max':2.1},'3.5,4.0':{'min':1.85, 'max':2.1}} ,
    # 'initial_ratios':{'weak':{'min':1.0, 'max':1.55}, 'strong':{'min':5, 'max':12}},
    'initial_handicaps':{'1.5':{'min':1.0, 'max':2.5}, '2.5':{'min':1.61, 'max':2.5}} ,
    'initial_minutes':{'min':0, 'max':0},
    'half_time':45,
    'quick_goal_interval':20,
    'all_bets_info':{
        'arleady_goals':{
             4:[
                     {'latest_goal_times':{'min':45, 'max':76}, 'forbidden_quick_goal':False, 'last_half_goals':{'min':2, 'max':3}, 'first_goal_times':{'min':0, 'max':45}},
                     # {'latest_goal_times':{'min':45, 'max':75}, 'forbidden_quick_goal':True, 'last_half_goals':{'min':1, 'max':1}, 'first_goal_times':{'min':0, 'max':9}},
                     # {'latest_goal_times':{'min':65, 'max':75}, 'forbidden_quick_goal':True, 'last_half_goals':{'min':0, 'max':0}, 'first_goal_times':{'min':45, 'max':60}}
             ],
                        #1:{'latest_goal_times':{'min':0, 'max':82}, 'forbidden_quick_goal':False, 'last_half_goals':{'min':0, 'max':10}, 'first_goal_times':{'min':0, 'max':90}},
                        # 2:{'latest_goal_times':{'min':0, 'max':75}, 'forbidden_quick_goal':True, 'last_half_goals':{'min':1, 'max':10}, 'next_half_goals':{'min':1, 'max':10}, 'first_goal_times':{'min':0, 'max':90}},
            3:{'latest_goal_times':{'min':0, 'max':50}, 'forbidden_quick_goal':False, 'last_half_goals':{'min':3, 'max':3}, 'next_half_goals':{'min':0, 'max':0}, 'first_goal_times':{'min':0, 'max':90}},
                         #4:{'latest_goal_times':{'min':0, 'max':82}, 'forbidden_quick_goal':False, 'last_half_goals':{'min':0, 'max':10}, 'next_half_goals':{'min':1, 'max':10}, 'first_goal_times':{'min':0, 'max':90}},
                       # 5:{'latest_goal_times':{'min':0, 'max':80}, 'forbidden_quick_goal':False, 'last_half_goals':{'min':1, 'max':10}, 'next_half_goals':{'min':1, 'max':10}, 'first_goal_times':{'min':0, 'max':90}},
                        # 6:{'latest_goal_times':{'min':0, 'max':85}, 'forbidden_quick_goal':False, 'last_half_goals':{'min':0, 'max':10}, 'next_half_goals':{'min':1, 'max':10}, 'first_goal_times':{'min':0, 'max':90}},
            # 2:{'latest_goal_times':{'min':60, 'max':75}, 'forbidden_quick_goal':True, 'last_half_goals':{'min':1, 'max':1}, 'first_goal_times':{'min':30, 'max':90}},
            #  2:[
            #          {'latest_goal_times':{'min':60, 'max':75}, 'forbidden_quick_goal':True, 'last_half_goals':{'min':1, 'max':1}, 'first_goal_times':{'min':30.30, 'max':90}},
            #          {'latest_goal_times':{'min':45, 'max':75}, 'forbidden_quick_goal':True, 'last_half_goals':{'min':1, 'max':1}, 'first_goal_times':{'min':0, 'max':9}},
            #          {'latest_goal_times':{'min':65, 'max':75}, 'forbidden_quick_goal':True, 'last_half_goals':{'min':0, 'max':0}, 'first_goal_times':{'min':45, 'max':60}}
            #  ]
        },
        'ready_bets':{
            '2':{'obey_any_success': False},
            '3':{'obey_any_success': False},
            '4':{'obey_any_success': False},
            '5':{'obey_any_success': False},
            '6':{'obey_any_success': False},
            '7':{'obey_any_success': False},
        }
    },
 }


# half_lgt_min = 0
# half_lgt_max = 15

RULE_HALF = {
    'initial_handicaps':{'0.5':{'min':1.0, 'max':2.5}, '0.5,1.0':{'min':1.0, 'max':2.5},
                             '1':{'min':1.0, 'max':2.5}, '1.0':{'min':1.0, 'max':2.5},
                             '1.0,1.5': {'min': 2.05, 'max': 2.5}} ,
    # 'initial_ratios':{'weak':{'min':1.0, 'max':1.55}, 'strong':{'min':5, 'max':12}},
    'initial_minutes':{'min':0, 'max':0},
    'half_time':45,
    'quick_goal_interval':4,
    'morning_hour_range':{'min':6, 'max':12},
    'all_bets_info':{
        'arleady_goals':{
            'morning':{
                'cut_off_time':35,
                2:{'latest_goal_times':{'min':0, 'max':30}, 'allow_quick_goal_num':0, 'allow_one_party_no_goal':True},
                # 3:{'latest_goal_times':{'min':0, 'max':25}, 'allow_quick_goal_num':1, 'allow_one_party_no_goal':False},
            },
            'evening':{
                # 'cut_off_time':30,
                'cut_off_time':40,
                1:{'latest_goal_times':{'min':0, 'max':35}, 'allow_quick_goal_num':0, 'allow_one_party_no_goal':True},
                # 3:{'latest_goal_times':{'min':0, 'max':25}, 'allow_quick_goal_num':1, 'allow_one_party_no_goal':False},
            }
        },
        'ready_bets':{
            '2':{'obey_any_success': False},
            '3':{'obey_any_success': False},
            '4':{'obey_any_success': False},
            '5':{'obey_any_success': False},
            '6':{'obey_any_success': False},
        }
    },
 }




