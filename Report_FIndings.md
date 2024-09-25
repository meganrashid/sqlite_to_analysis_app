# Results

## Purpose:
This model predicts a Company's business category based on the text of their homepage website. 

### Hypothesis: 
The implicit hypothesis is that websites within each category will use distinctive language that can be used to classify them.

## Overall process:
1. Normalize Text (done during eda.ipynb to complete EDA)
2. Label Encoding
3. Feature Extraction (TFIDF & BERT)
4. Model Training
5. Evaulate best performing model and vectorization method --> DistilBERT with Logistic Regression

## DistilBERT Results
Logistic regression with DistilBERT far outperforms the same model with TF-IDF

DistilBERT was selected because it can achieve similar performance to BERT with fewer parameters and faster training times. As I faced
memory limitations training locally, I also chose to precompute my DistilBERT embeddings and load them with the model for training purposes.

This required me to limit my data from the full 71k rows to 5k rows, but I would expand this dataset to include more records in next developments.

Unlike the TF-IDF vectorization, we see the top performing categories wiht BERT are:
1. Healthcare
2. Transportation & Logistics
3. Consumer Staples

The accuracy drops for remaining classes. However, even the worst performing category (Consumer Discretionary
66 examples), it far outperforms any of the TF-IDF variation models.

DistilBERT captures the context and not just word frequency, but we can absolutely improve by incorporating other features.

## Next steps:
1. Increase datasize (but need more memory to process)
2. Test out different models and hyperparameter tuning
3. Try category-specific models (e.g. one model for healthcare, one model for IT)
4. Return to text normalization and see if any important information was accidentally removed. 
    Examples:
    - Remove contact information & addresses
    - Ensure no lingering punctuation or unicode remains

As Logisitc Regression becomes less performant with more features, I would still test that this model is the right choice when I increase
the amount of data or features. 

## Data Considerations
From the EDA, I saw that certain categories are skewed by specific industries and mostly coming from the US. Therefore, in cross-validation, 
especially in category-specfic models, I'd like to test that the model(s) can still predict these industries.

I'd need to understand within each category if:
1. Do certain models perform better for one industry over another?
2. Is there one industry that brings down the global accuracy?

If the use case required high accuracy results to predict the category (e.g. filtering marketing campaigns based on predictionr results), I would
also consider how I can enrich this dataset to better represent different industries and geographic regions.
