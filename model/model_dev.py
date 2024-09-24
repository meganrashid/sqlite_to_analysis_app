import pandas as pd
import os 
import numpy as np
import pickle

from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import classification_report, accuracy_score
from sklearn.pipeline import Pipeline

# from transformers import BertTokenizer, BertModel
from transformers import DistilBertTokenizer, DistilBertModel #smaller and faster than BERT
import torch

from sklearn.base import TransformerMixin, BaseEstimator

# read data back in from pickle file created with eda.ipynb

print("""Purpose:
This model predicts a Company's business category based on the text of their homepage website. 

Hypothesis: 
The implicit hypothesis is that websites within each category will use distinctive language that can be used to classify them.

Overall process:
1. Normalize Text (done during eda.ipynb to complete EDA)
2. Label Encoding
3. Feature Extraction (TFIDF & BERT)
4. Model Training
5. Evaulate best performing model and vectorization method
      
For more info on training process, check out model_dev.ipynb""")

# Dynamically get the current working directory

# # get the base directory
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

text_path = os.path.abspath(os.path.join(base_dir, 'output','combined_data.pkl'))
# read data back in 
df_clean = pd.read_pickle(text_path)

# Get a random sample of 5k rows due to memory constraints
df_sample = df_clean.sample(n=5000)

#Turning the labels into numbers
label_encoder = LabelEncoder()
df_sample['Category_encoded'] = label_encoder.fit_transform(df_sample['Category'])

# split the data into features (X) and labels (y)
X = df_sample['clean_text_str']
y = df_sample['Category_encoded']

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Define KFold cross-validator
kf = KFold(n_splits=10, shuffle=True, random_state=42) # using the normal 10 folds

# # Define the classification models to be tested
models = {
    'Logistic Regression': LogisticRegression(multi_class='ovr', max_iter=1000)
}

# use to create DistilBERT embeddings
class DistilBERTEmbeddingTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, model_name='distilbert-base-uncased', max_length=512): #use distilbert because it's smaller and faster than BERT
        self.model_name = model_name  # Explicitly set model_name
        self.tokenizer = DistilBertTokenizer.from_pretrained(self.model_name)
        self.model = DistilBertModel.from_pretrained(self.model_name)
        self.max_length = max_length

    def fit(self, X, y=None):
        # Fit method required for scikit-learn compatibility
        return self

    def transform(self, X):
        embeddings = []
        for text in X:
            # Tokenize and convert text to tensors
            tokens = self.tokenizer(text, return_tensors='pt', padding='max_length',
                                    truncation=True, max_length=self.max_length)
            
            # Ensure no gradient computation for embeddings
            with torch.no_grad():
                output = self.model(**tokens)
                # Take the CLS token embedding
                cls_embedding = output.last_hidden_state[:, 0, :].numpy()
            
            embeddings.append(cls_embedding[0])  # Append as numpy array
            
        return np.array(embeddings)

# # load precomputed embeddings
X_train_embeddings2 = np.load(os.path.abspath(os.path.join(base_dir, 'model','X_train_distilbert.npy')))
X_test_embeddings2 = np.load(os.path.join(base_dir, 'model','X_test_distilbert.npy'))

# Store BERT results
bert_results = []
bert_report_list=[]

# Iterate over models using the precomputed BERT embeddings
for model_name, model in models.items():
    # if isinstance(model, MultinomialNB): # MultinomialNB requires non-negative input values but embeddings can include negative values
    #     print(f"Skipping {model_name} as it is not compatible with BERT embeddings.")
    #     continue
    
    print(f"\n=== {model_name} ===")
    
    # Train the model using precomputed BERT embeddings
    model.fit(X_train_embeddings2, y_train)
    y_pred_bert = model.predict(X_test_embeddings2)
    
    # Cross-Validation with precomputed BERT embeddings
    bert_scores = cross_val_score(model, X_train_embeddings2, y_train, cv=kf, scoring='accuracy')
    
    # Calculate accuracy and classification report
    bert_accuracy = accuracy_score(y_test, y_pred_bert)
    bert_report = classification_report(y_test, y_pred_bert, target_names=label_encoder.classes_, output_dict=True)


    bert_df = pd.DataFrame([bert_report]).T
    bert_df = bert_df.reset_index().rename(columns={'index':'Category'})
    bert_df_report = bert_df[0].apply(pd.Series)

    bert_final = pd.merge(bert_df['Category'], bert_df_report, left_index=True,right_index=True)

    # filter dataframe                                   
    bert_clean = bert_final.loc[(bert_final['Category']!='weighted avg') & (bert_final['Category']!='macro avg') & (bert_final['Category']!='accuracy')]
    bert_clean['model']=model_name
    bert_report_list.append(bert_clean)

    # Save the model
    with open('logistic_dbert_model.pkl', 'wb') as model_file:
        pickle.dump(model, model_file)

     # To load the model later
    with open('logistic_dbert_model.pkl', 'rb') as model_file:
        loaded_model = pickle.load(model_file)
    
    # Append BERT results to the results list
    bert_results.append({
        'Model': model_name,
        'Cross_Val_Accuracy': bert_scores.mean(),
        'Test_Accuracy': bert_accuracy,
        'Precision': bert_report['weighted avg']['precision'],
        'Recall': bert_report['weighted avg']['recall'],
        'F1-Score': bert_report['weighted avg']['f1-score']

    })

# Convert BERT results to DataFrame
bert_results_df = pd.DataFrame(bert_results)
print("BERT Results:")
print(bert_results_df)

dbert_df = pd.concat(bert_report_list)
print(dbert_df.sort_values(by=['model','f1-score'], ascending=False))

print('Model training complete. To call the model use')
print('predictions = loaded_model.predict(new_embeddings)')