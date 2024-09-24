import pandas as pd
import os 
import numpy as np

from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder

# read data back in from pickle file created with eda.ipynb

# Dynamically get the current working directory
current_dir = os.getcwd()
text_path = os.path.abspath(os.path.join(current_dir, '..', 'output','combined_data.pkl'))

# read data back in 
df_clean = pd.read_pickle(text_path)


#Turning the labels into numbers
label_encoder = LabelEncoder()
df_clean['Category_encoded'] = label_encoder.fit_transform(df_clean['Category'])

# split the data into features (X) and labels (y)
X = df_clean['clean_text_str']
y = df_clean['Category_encoded']

# Define KFold cross-validator
kf = KFold(n_splits=10, shuffle=True, random_state=42) # using the normal 10 folds

# # Define the classification models to be tested
# models = {
#     'Naive Bayes': MultinomialNB(),
#     'Logistic Regression': LogisticRegression(multi_class='ovr', max_iter=1000),
#     'SGD Classifier': SGDClassifier(),
#     'Random Forest': RandomForestClassifier(n_estimators=100)
# }