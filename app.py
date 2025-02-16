import xgboost as xgb
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

# Define the API
app = FastAPI()

# Load the trained model
model = xgb.XGBRegressor()
model.load_model(r"C:\Users\AKHIL\Documents\Women Cancer Relapse Project\models\breast_cancer_model.json")

# Define feature names (must match training features)
feature_names = ['Female', 'Living', 'IDC_BREAST', 'IDC_IDC', 'IDC_ILC', 'IDC_IMMC', 'IDC_MDLC', 
                 'Primary_Primary', 'ER-/HER2-_ER+/HER2-_High_Prolif', 'ER-/HER2-_ER+/HER2-_Low_Prolif', 
                 'ER-/HER2-_ER-/HER2-', 'ER-/HER2-_HER2+', 'MASTECTOMY_BREAST_CONSERVING', 
                 'MASTECTOMY_MASTECTOMY', 'Breast_Invasive_Ductal_Carcinoma_Breast', 
                 'Breast_Invasive_Ductal_Carcinoma_Breast_Invasive_Ductal_Carcinoma', 
                 'Breast_Invasive_Ductal_Carcinoma_Breast_Invasive_Lobular_Carcinoma', 
                 'Breast_Invasive_Ductal_Carcinoma_Breast_Invasive_Mixed_Mucinous_Carcinoma', 
                 'Breast_Invasive_Ductal_Carcinoma_Breast_Mixed_Ductal_and_Lobular_Carcinoma', 
                 'Breast_Cancer_Breast_Cancer']

# Define the input format
class InputData(BaseModel):
    features: list

@app.post("/predict")
def predict(data: InputData):
    try:
        # Convert input list to DataFrame with proper feature names
        input_df = pd.DataFrame([data.features], columns=feature_names)
        
        # Make a prediction
        prediction = model.predict(input_df)

        return {"prediction": prediction.tolist()}
    
    except Exception as e:
        return {"error": str(e)}
