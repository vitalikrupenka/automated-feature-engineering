import pandas as pd 
import featuretools as ft

my_sep = '\n\n' + '*' * 100 + '\n\n'

users = pd.read_csv('data/lg_users.csv', low_memory=False)
looks = pd.read_csv('data/lg_looks.csv', low_memory=False)
likes = pd.read_csv('data/lg_likes.csv', low_memory=False)

es = ft.EntitySet(id = 'users')

es = es.entity_from_dataframe(entity_id='users', dataframe=users, 
                                index='user_id')

es = es.entity_from_dataframe(entity_id='looks', dataframe=looks, 
                                index='look_id')

es = es.entity_from_dataframe(entity_id='likes', dataframe=likes,
                                make_index=True, index='like_id')

r_user_likes = ft.Relationship(es['users']['user_id'], es['likes']['user_id'])
r_look_likes = ft.Relationship(es['looks']['look_id'], es['likes']['look_id'])

es.add_relationship(r_user_likes)
es.add_relationship(r_look_likes)

# print('', es, es['users'], es['looks'], es['likes'], '', sep=my_sep)

# features, feature_names = ft.dfs(entityset=es, target_entity='likes',
#                                     agg_primitives=['sum'])
# print('', features, feature_names, '', sep=my_sep)

# Group loans by client id and calculate mean, max, min of loans

stats = likes.groupby('user_id')['look_liked'].agg(['sum'])
stats.columns = ['num_looks_liked']

# Merge with the clients dataframe
stats = users.merge(stats, left_on = 'user_id', right_index=True, how='left')
stats = stats.sort_values(by=['num_looks_liked', 'person_last_name'], ascending=[False, True])

print(stats.head(50))

df = pd.DataFrame(stats)
df.to_csv (r'data/lg_features.csv', index = False, header=True)
