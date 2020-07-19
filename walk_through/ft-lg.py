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
                                variable_types={'missed' : ft.variable_types.Discrete},
                                make_index=True, index='like_id')

r_user_likes = ft.Relationship(es['users']['user_id'], es['likes']['user_id'])
r_look_likes = ft.Relationship(es['looks']['look_id'], es['likes']['look_id'])

es.add_relationship(r_client_loans)
es.add_relationship(r_loan_payments)

print('', es, es['users'], es['looks'], es['likes'], '', sep=my_sep)

# features, feature_names = ft.dfs(entityset=es, target_entity='clients',
#                                     agg_primitives=['mean', 'max', 'percent_true', 'last'],
#                                     trans_primitives=['month', 'year'])

# print('', features, feature_names, '', sep=my_sep)

# df = pd.DataFrame(features)
# df.to_csv (r'data/features.csv', index = True, header=True)

# print(stats.head(50))

