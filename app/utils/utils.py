


import os
import pickle
import pandas as pd


def apply_one_hot_encoding(model_folder, input_df):
    with open(os.path.join(model_folder, "one_hot_columns.pkl"), "rb") as f:
        training_columns_structure = pickle.load(f)
    expected_columns = training_columns_structure.columns.tolist()
    if "Churn" in expected_columns:
        expected_columns.remove("Churn")
    input_df_encoded = pd.DataFrame(0, index=[0], columns=expected_columns)

    for col in input_df.columns:
        
        value = input_df[col].iloc[0]
        raw_value = input_df[col].iloc[0]
        if hasattr(raw_value, "value"):
            value = raw_value.value
        else:
            value = raw_value
            
        target_col = f"{col}_{value}"
        if target_col in input_df_encoded.columns:
            input_df_encoded[target_col] = 1
        else:
            pass
    return  input_df_encoded


def apply_label_encoding(model_folder, input_df_copy, input_df_scaled):
    with open(os.path.join(model_folder, "label_encoders.pkl"), "rb") as f:
        label_encoders  = pickle.load(f)
    categorical_columns = input_df_copy.select_dtypes(include=['object']).columns
        
    for column in categorical_columns:
        if column in label_encoders:
            input_df_copy[column] = label_encoders[column].transform(input_df_copy[column])
            input_df_scaled[column] = label_encoders[column].transform(input_df_scaled[column])
            
    return input_df_copy, input_df_scaled

    