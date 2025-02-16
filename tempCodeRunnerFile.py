import pandas as pd
import xgboost as xgb
from fastapi import FastAPI
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI()

# Load your trained model
model = xgb.Booster()
model.load_model("your_model_path.json")  # Make sure this is the correct path

# Define the feature names
feature_names = [
    "Female", "Living", "IDC_BREAST", "IDC_IDC", "IDC_ILC", "IDC_IMMC", "IDC_MDLC",
    "Primary_Primary", "ER-/HER2-_ER+/HER2-_High_Prolif", "ER-/HER2-_ER+/HER2-_Low_Prolif",
    "ER-/HER2-_ER-/HER2-", "ER-/HER2-_HER2+", "MASTECTOMY_BREAST_CONSERVING",
    "MASTECTOMY_MASTECTOMY", "Breast_Invasive_Ductal_Carcinoma_Breast",
    "Breast_Cancer_Breast_Cancer"
]

# Define input schema
class InputData(BaseModel):
    Female: int
    Living: int
    IDC_BREAST: int
    IDC_IDC: int
    IDC_ILC: int
    IDC_IMMC: int
    IDC_MDLC: int
    Primary_Primary: int
    ER_HER2_High_Prolif: int
    ER_HER2_Low_Prolif: int
    ER_HER2_Negative: int
    HER2_Positive: int
    MASTECTOMY_BREAST_CONSERVING: int
    MASTECTOMY_MASTECTOMY: int
    Breast_Invasive_Ductal_Carcinoma_Breast: int
    Breast_Cancer_Breast_Cancer: int

@app.post("/predict/")
def predict(data: InputData):
    try:
        # Convert input to DataFrame
        data_df = pd.DataFrame([data.dict()])

        # Ensure the DataFrame has the correct feature names
        data_df = data_df[feature_names]

        # Convert to DMatrix for XGBoost
        dmatrix = xgb.DMatrix(data_df)

        # Make predictions
        prediction = model.predict(dmatrix)

        return {"prediction": prediction.tolist()}

    except Exception as e:
        return {"error": str(e)}
