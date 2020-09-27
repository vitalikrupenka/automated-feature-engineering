import pandas as pd 

u_features = pd.read_csv('data/lg_features_real.csv')
u_looks = pd.read_csv('data/lg_looks_real.csv')

uf_set = set(u_features.columns.values)
ul_set = set(u_looks.columns.values)

isec_cols = list(uf_set.intersection(ul_set))

# print(isec_cols, len(isec_cols), end='\n\n')

isf = u_features[isec_cols]
isl = u_looks[isec_cols]

def intersection(lst1, lst2): 
    lst3 = [lst1[i] for i in range(len(lst1)) if lst1[i] == lst2[i]]
    return lst3 

# print(isf.head(), isf.shape)
# print(intersection(isf.values[0], isl.values[0]))

isr = []
for i in range(len(isf.values)):
    for j in range(len(isl.values)):
        # print(intersection(isf.values[i], isl.values[j]))
        if isf['male'][i] == isl['male'][j]:
            isr.append([i+1, j+1, 
                        float('{:.2f}'.format(len(intersection(isf.values[i], isl.values[j])) / len(isf.values[i]) * 100))])
        else:
            isr.append([i+1, j+1, 0])

# print(isr[0:100])
# print(len(isr))

ism = dict()
for item in isr:
    ism[item[0]] = ism.get(item[0], [0, 0, 0])
    if item[2] > ism[item[0]][1]:
        ism[item[0]] = ((item[1], item[2]))

# print(ism)

# for key, val in ism.items():
#     print('User\'s %d favorite Look is %d with the probability of %.2f' % (key, val[0], val[1]), end='\n')

import matplotlib.image as img 
import matplotlib.pyplot as plt 

user_id = 105

look_img = img.imread('data/looks/%d.png' % (ism[user_id][0]))
plt.imshow(look_img)
plt.show()

df_likes = dict()
for item in isr:
    df_likes['user_id'] = df_likes.get('user_id', [])
    if item[0] not in df_likes['user_id']:
        df_likes['user_id'].append(item[0])

    like_threshold = 75
    is_liked = 0
    if item[2] >= like_threshold:
        is_liked = 1

    colname = 'look_id_' + str(item[1])
    df_likes[colname] = df_likes.get(colname, [])
    df_likes[colname].append(is_liked)

# for key, val in df_likes.items():
#     print(key + ':', val, end='\n')

# print(len(df_likes['user_id']), len(df_likes['look_id_1']), len(df_likes['look_id_183']))

u_likes = pd.DataFrame(data=df_likes, index=None)
u_likes.to_csv('data/lg_likes_real-pred.csv', index=False)
# print(u_likes.sample(100))

u_features_rp = pd.read_csv('data/lg_features_real-pred.csv')
ufrp_corr = u_features_rp.corr()

import seaborn as sns
fig, ax = plt.subplots(figsize=(24, 20))
sns.heatmap(ufrp_corr, annot=False)
plt.show()