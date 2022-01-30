import numpy as np

# logic_dict = {'ScrimYards':{'tier_0': range(100,250), 'tier_1': range(80,100), 'tier_2': range(60,80), 
# 'tier_3': range(40,60), 'tier_4': range(20,40), 'tier_5': range(0,20)}, }

# my_num = 26

# def find_my_tier(num):
#     for tier, range in logic_dict['ScrimYards'].items():
#         if num in range:
#             return tier
#         else:
#             continue

# print(find_my_tier(my_num))

my_num = .85
if my_num in np.arange(0,1,.01):
    print('True')
