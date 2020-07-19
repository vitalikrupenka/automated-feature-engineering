import pandas as pd 
import featuretools as ft

my_sep = '\n\n' + '*' * 100 + '\n\n'

clients = pd.read_csv('data/clients.csv', low_memory=False)
loans = pd.read_csv('data/loans.csv', low_memory=False)
payments = pd.read_csv('data/payments.csv', low_memory=False)

es = ft.EntitySet(id = 'clients')

es = es.entity_from_dataframe(entity_id='clients', dataframe=clients, 
                                index='client_id', time_index='joined')

es = es.entity_from_dataframe(entity_id='loans', dataframe=loans, 
                                index='loan_id', time_index='loan_start')

es = es.entity_from_dataframe(entity_id='payments', dataframe=payments,
                                variable_types={'missed' : ft.variable_types.Categorical},
                                make_index=True, index='payment_id',
                                time_index='payment_date')

r_client_loans = ft.Relationship(es['clients']['client_id'], es['loans']['client_id'])
r_loan_payments = ft.Relationship(es['loans']['loan_id'], es['payments']['loan_id'])

es.add_relationship(r_client_loans)
es.add_relationship(r_loan_payments)

#print('', es, es['clients'], es['loans'], es['payments'], '', sep=my_sep)

features, feature_names = ft.dfs(entityset=es, target_entity='clients',
                                    agg_primitives=['mean', 'max', 'percent_true', 'last'],
                                    trans_primitives=['month', 'year'])

print('', features, feature_names, '', sep=my_sep)

df = pd.DataFrame(features)
df.to_csv (r'data/features.csv', index = True, header=True)

# # Group loans by client id and calculate mean, max, min of loans
# stats = loans.groupby('client_id')['loan_amount'].agg(['mean', 'max', 'min'])
# stats.columns = ['mean_loan_amount', 'max_loan_amount', 'min_loan_amount']

# # Merge with the clients dataframe
# stats = clients.merge(stats, left_on = 'client_id', right_index=True, how = 'left')

# print(stats.head(50))

