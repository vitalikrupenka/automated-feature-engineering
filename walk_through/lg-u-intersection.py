import pandas as pd 

u_features = pd.read_csv('data/lg_features_real.csv')
u_looks = pd.read_csv('data/lg_looks_real.csv')

# print(u_features.columns.values, u_features.shape, end='\n\n')
# print(u_looks.columns.values, u_looks.shape, end='\n\n')

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
        isr.append([i+1, j+1, 
                    float('{:.2f}'.format(len(intersection(isf.values[i], isl.values[j])) / len(isf.values[i]) * 100))]) 
        
ism = {}
mx = 0
for i in range(len(isr)):
    curr = isr[i][2]
    if curr > mx:
        mx = curr
    ism[isr[i][0]] = [isr[i][1], mx]
    # ism[isr[i][0]] = ism.get(isr[i][0], []).append([isr[i][1], mx])

print(mx)
# print(isr[:10])

for key, val in ism.items():
    print('User\'s %d favorite Look is %d with the probability of %.2f' % (key, val[0], val[1]), end='\n')
print(ism.keys(), len(ism.keys()))