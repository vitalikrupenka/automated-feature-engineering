
import pandas as pd 

import matplotlib.pyplot as plt 
import seaborn as sns
import numpy as np 

u_features = pd.read_csv('data/lg_features_real.csv')

print(u_features.shape, end='\n\n')

# ufc = u_features.columns.values
# drop_ids = [x for x in ufc if 'look_id_' in x]

u_features = u_features.drop(['user_id'], axis=1)

X = u_features.drop(['style_business_casual'], axis=1)
Y = u_features['style_business_casual']

# X = u_features.drop(['size_m'], axis=1)
# Y = u_features['size_m']

# X = u_features.drop(['color_white'], axis=1)
# Y = u_features['color_white']

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

print(x_train.shape, x_test.shape, end='\n\n')
print(y_train.shape, y_test.shape, end='\n\n')

from sklearn.linear_model import LogisticRegression

lrm = LogisticRegression().fit(x_train, y_train)

print('Training score: ', lrm.score(x_train, y_train), end='\n\n')

predictors = x_train.columns

# coef = pd.Series(lrm.coef_, predictors).sort_values()
# print(coef, end='\n\n')

y_pred = lrm.predict(x_test)
df_pred_actual = pd.DataFrame({'predicted': y_pred, 'actual': y_test})
print(df_pred_actual.head(10), end='\n\n')

from sklearn import metrics
# cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
# print('Testing score: ', cnf_matrix, end='\n\n')

print("Accuracy: {:.2f} %".format(100 * metrics.accuracy_score(y_test, y_pred)))
print("Precision: {:.2f} %".format(100 * metrics.precision_score(y_test, y_pred)))
print("Recall:  {:.2f} %".format(100 * metrics.recall_score(y_test, y_pred)))

#Visualizations
y_pred_proba = lrm.predict_proba(x_test)[::,1]
fpr, tpr, _ = metrics.roc_curve(y_test,  y_pred_proba)
auc = metrics.roc_auc_score(y_test, y_pred_proba)
plt.plot(100 * fpr, 100 * tpr, label="data 1, auc={:.2f} %".format(100 * auc))
# plt.plot(100 * fpr, 100 * tpr, label="data 1, auc=" + str(100 * auc))
plt.legend(loc=4)
plt.show()

from sklearn.metrics import precision_recall_curve
precision, recall, thresholds = precision_recall_curve(y_test, y_pred_proba) 
pr_auc = metrics.auc(recall, precision)

plt.title("Precision-Recall vs Threshold Chart")
plt.plot(100 * thresholds, 100 * precision[: -1], "b--", label="Precision, %")
plt.plot(100 * thresholds, 100 * recall[: -1], "r--", label="Recall, %")
plt.ylabel("Precision / Recall, %")
plt.xlabel("Threshold, %")
plt.legend(loc="lower left")
plt.ylim([0,100])
plt.show()

# fig, ax = plt.subplots(figsize=(12, 8))
# plt.scatter(y_test, y_pred)
# plt.show()

# df_pred_actual_sample = df_pred_actual.sample(5)
# df_pred_actual_sample = df_pred_actual_sample.reset_index()

# plt.figure(figsize = (20, 10))
# plt.plot(df_pred_actual_sample['predicted'], label='Predicted')
# plt.plot(df_pred_actual_sample['actual'], label='Actual')
# plt.ylabel('Age')
# plt.legend()
# plt.show()

# class_names=[0,1] # name  of classes
# fig, ax = plt.subplots()
# tick_marks = np.arange(len(class_names))
# plt.xticks(tick_marks, class_names)
# plt.yticks(tick_marks, class_names)
# # create heatmap
# sns.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap="YlGnBu" ,fmt='g')
# ax.xaxis.set_label_position("top")
# plt.tight_layout()
# plt.title('Confusion matrix', y=1.1)
# plt.ylabel('Actual label')
# plt.xlabel('Predicted label')
# plt.show()