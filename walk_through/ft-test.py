import pandas as pd 

loans = pd.read_csv('data/loans.csv', low_memory=False)
clients = pd.read_csv('data/clients.csv', low_memory=False)

# Group loans by client id and calculate mean, max, min of loans
stats = loans.groupby('client_id')['loan_amount'].agg(['mean', 'max', 'min'])
stats.columns = ['mean_loan_amount', 'max_loan_amount', 'min_loan_amount']

# Merge with the clients dataframe
stats = clients.merge(stats, left_on = 'client_id', right_index=True, how = 'left')

print(stats.head(10))