



import os
from fastapi import APIRouter, HTTPException
import pickle

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from app.pydantic_models.pydantic_models import CustomerChurnPayload
import pandas as pd

from app.utils.utils import apply_label_encoding, apply_one_hot_encoding

churn_router = APIRouter(tags=["Churn"])


@churn_router.get("/")
def home():
    return {"message": "FastAPI is working!"}


@churn_router.post("/predict_churn")
def predict_churn(input_data: CustomerChurnPayload)->dict:
    try:
        input_df = pd.DataFrame([input_data.dict()])
        input_df['CLV'] = input_df['tenure'] * input_df['TotalCharges']
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_folder = os.path.join(base_path, "pickle")
        
        input_df_one_hot_encoded = input_df.copy()
        input_df_one_hot_encoded = apply_one_hot_encoding(model_folder, input_df_one_hot_encoded)
        print(input_df_one_hot_encoded.head())

        naive_bias_model_path = os.path.join(model_folder, "naive_bias_model.pkl")
        logistic_model_path = os.path.join(model_folder, "logistic_model.pkl")
        decission_tree_model_path = os.path.join(model_folder, "decission_tree_model.pkl")
        random_forest_model_path = os.path.join(model_folder, "random_forest_model.pkl")
        knn_model_path =   os.path.join(model_folder, "knn_model.pkl")
        svm_model_path = os.path.join(model_folder, "svc_model.pkl")
        model_files = [
           naive_bias_model_path,
           logistic_model_path,
           decission_tree_model_path,
           random_forest_model_path,
           knn_model_path,
           svm_model_path 
        ]

        input_df_copy = input_df.copy()
        input_df_scaled = input_df.copy()
        input_df_copy, input_df_scaled = apply_label_encoding(model_folder, input_df_copy, input_df_scaled) 
        print(input_df_copy.head())   

        models = []
        for file in model_files:
            with open(file, "rb") as f:
                models.append(pickle.load(f))
        
        scaler = StandardScaler()
        numerical_columns = input_df_copy.select_dtypes(include=['number']).columns
        input_df_scaled[numerical_columns] = scaler.fit_transform(input_df_copy[numerical_columns])
            
        predictions = []
        for model in models:
            if isinstance(model, (DecisionTreeClassifier, RandomForestClassifier, LogisticRegression)):
                predictions.append(model.predict(input_df_one_hot_encoded)[0])
            elif isinstance(model, GaussianNB):
                predictions.append(model.predict(input_df_copy)[0])
            elif isinstance(model, (KNeighborsClassifier, SVC)):
                predictions.append(model.predict(input_df_scaled)[0])
        
        majority = 1 if predictions.count(1) > predictions.count(0) else 0
                 
        return {
            "majority": majority,
            'customer_lifetime_value':  float(input_df["CLV"].iloc[0])
        }            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")