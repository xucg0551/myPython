from datetime import datetime,date

# login_time = datetime.strptime('2018-03-08 11:00:00', '%Y-%m-%d %H:%M:%S')
# print(login_time.hour)
# # when_key = 'morning' if (login_time.hour >= 5 and login_time.hour <= 12) else 'evening'
# print(when_key)




# RULE_HALF = {
#     'initial_handicaps':{'0.5':{'min':1.0, 'max':2.5}, '0.5,1.0':{'min':1.0, 'max':2.5},
#                              '1':{'min':1.0, 'max':2.5}, '1.0':{'min':1.0, 'max':2.5},
#                              '1.0,1.5': {'min': 2.05, 'max': 2.5}} ,
#     # 'initial_ratios':{'weak':{'min':1.0, 'max':1.55}, 'strong':{'min':5, 'max':12}},
#     'initial_minutes':{'min':0, 'max':0},
#     'half_time':45,
#     'quick_goal_interval':4,
#     'morning_hour_range':{'min':5, 'max':12},
#     'all_bets_info':{
#         'arleady_goals':{
#             'morning':{
#                 'cut_off_time':35,
#                 1:{'latest_goal_times':{'min':0, 'max':35}, 'allow_quick_goal_num':0},
#                 2:{'latest_goal_times':{'min':0, 'max':35}, 'allow_quick_goal_num':1},
#             },
#             'evening':{
#                 'cut_off_time':30,
#                 # 2:{'latest_goal_times':{'min':0, 'max':20}, 'allow_quick_goal_num':0},
#                 3:{'latest_goal_times':{'min':0, 'max':25}, 'allow_quick_goal_num':1},
#             }
#
#
#             # 4:{'latest_goal_times':{'min':half_lgt_min, 'max':half_lgt_max}, 'allow_quick_goal_num':1},
#
#         },
#         'ready_bets':{
#             '2':{'obey_any_success': False},
#             '3':{'obey_any_success': False},
#             '4':{'obey_any_success': False},
#             '5':{'obey_any_success': False},
#             '6':{'obey_any_success': False},
#         }
#     },
#  }
#
# morning_hour_range_min = RULE_HALF['morning_hour_range']['min']
# morning_hour_range_max = RULE_HALF['morning_hour_range']['max']
# when_key = 'morning' if (datetime.now().hour >= morning_hour_range_min and datetime.now().hour <= morning_hour_range_max) else 'evening'
# print(when_key)

# infos = RULE_HALF['all_bets_info']['arleady_goals'][when_key]
# min_latest_goal_time = infos[1]['latest_goal_times']['min']
# max_latest_goal_time = infos[2]['latest_goal_times']['max']
# print(min_latest_goal_time)
# print(max_latest_goal_time)

RULE_FULL = {
    # 'initial_handicaps':{'3.0,3.5':{'min':1.5, 'max':1.95}, '3.5':{'min':1.7, 'max':2.1},'3.5,4.0':{'min':1.85, 'max':2.1}} ,
    # 'initial_ratios':{'weak':{'min':1.0, 'max':1.55}, 'strong':{'min':5, 'max':12}},
    'initial_handicaps':{'1.5':{'min':1.0, 'max':2.5}, '2.5':{'min':1.61, 'max':2.5}} ,
    'initial_minutes':{'min':0, 'max':0},
    'half_time':45,
    'quick_goal_interval':4,
    'all_bets_info':{
        'arleady_goals':{
                        # 2:{'latest_goal_times':{'min':0, 'max':85}, 'forbidden_quick_goal':False, 'last_half_goals':{'min':0, 'max':10}, 'first_goal_times':{'min':0, 'max':90}},
                        # 3:{'latest_goal_times':{'min':0, 'max':85}, 'forbidden_quick_goal':False, 'last_half_goals':{'min':0, 'max':10}, 'first_goal_times':{'min':0, 'max':90}},
                        # 4:{'latest_goal_times':{'min':0, 'max':85}, 'forbidden_quick_goal':False, 'last_half_goals':{'min':0, 'max':10}, 'first_goal_times':{'min':0, 'max':90}},
                        # 5:{'latest_goal_times':{'min':0, 'max':85}, 'forbidden_quick_goal':False, 'last_half_goals':{'min':0, 'max':10}, 'first_goal_times':{'min':0, 'max':90}},
                        # 6:{'latest_goal_times':{'min':0, 'max':85}, 'forbidden_quick_goal':False, 'last_half_goals':{'min':0, 'max':10}, 'first_goal_times':{'min':0, 'max':90}},
            # 2:{'latest_goal_times':{'min':60, 'max':75}, 'forbidden_quick_goal':True, 'last_half_goals':{'min':1, 'max':1}, 'first_goal_times':{'min':30, 'max':90}},
            2:[
                    {'latest_goal_times':{'min':60, 'max':75}, 'forbidden_quick_goal':True, 'last_half_goals':{'min':1, 'max':1}, 'first_goal_times':{'min':30.30, 'max':90}},
                    {'latest_goal_times':{'min':45, 'max':75}, 'forbidden_quick_goal':True, 'last_half_goals':{'min':1, 'max':1}, 'first_goal_times':{'min':0, 'max':9}},
                    {'latest_goal_times':{'min':65, 'max':75}, 'forbidden_quick_goal':True, 'last_half_goals':{'min':0, 'max':0}, 'first_goal_times':{'min':45, 'max':60}}
            ]
        },
        'ready_bets':{
            '2':{'obey_any_success': True},
            '3':{'obey_any_success': False},
            '4':{'obey_any_success': False},
            '5':{'obey_any_success': False},
            '6':{'obey_any_success': False},
            '7':{'obey_any_success': False},
        }
    },
 }



# 第一个进球是否满足条件
possibilities = RULE_FULL['all_bets_info']['arleady_goals'][2]
goals_time = [9, 80]
first_goal_time = float(goals_time[0]) if len(goals_time) != 0 else 0

if isinstance(possibilities, list):
    for infos in possibilities:
        is_possibility_ok = (
        first_goal_time >= infos['first_goal_times']['min'] and first_goal_time <= infos['first_goal_times']['max'])
        if is_possibility_ok:
            break
elif isinstance(possibilities, dict):
    infos = possibilities


print(infos)
print(infos.get('forbidden_quick_goal', False))
