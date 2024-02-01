from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import spacy

# Initialize
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins={"*"},
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setting up the models
nlp_best = spacy.load("model-best")
nlp_last = spacy.load("model-last")

entity_types_best = list(nlp_best.pipe_labels['ner'])
entity_types_last = list(nlp_last.pipe_labels['ner'])

# Print the list of entity types
print("List of Entity Types, best:", entity_types_best)
print("List of Entity Types, last:", entity_types_last)

# Data Validation
class PredictionRequest(BaseModel):
    inputText: str

# API methods
@app.get("/")
async def read_root():
    return {
        "Hello There!": "Welcome to the Server!", 
        "For more info": "Please add '/docs' after the url", 
        "example": "http://127.0.0.1:8000/docs"
    }

@app.post("/predict/")
async def predict(request: PredictionRequest):
    # Process the text with SpaCy
    doc_best = nlp_best(request.inputText)
    doc_last = nlp_last(request.inputText)

    # Initialize dictionaries to store token information
    token_info_best = {}
    token_info_last = {}

    # Process the first document (doc_best)
    for token in doc_best:
        token_info_best[token.text] = token.ent_type_

    # Process the second document (doc_last)
    for token in doc_last:
        token_info_last[token.text] = token.ent_type_

    # Count occurrences of entity types in each dictionary
    # ex: MEDICALCONDITION: Diarrhea || MEDICINE: Loperamide || PATHOGEN: Virus 
    count_medicalcondition_best = sum(1 for ent_type in token_info_best.values() if ent_type == 'MEDICALCONDITION')
    count_medicine_best = sum(1 for ent_type in token_info_best.values() if ent_type == 'MEDICINE')
    count_pathogen_best = sum(1 for ent_type in token_info_best.values() if ent_type == 'PATHOGEN')

    count_medicalcondition_last = sum(1 for ent_type in token_info_last.values() if ent_type == 'MEDICALCONDITION')
    count_medicine_last = sum(1 for ent_type in token_info_last.values() if ent_type == 'MEDICINE')
    count_pathogen_last = sum(1 for ent_type in token_info_last.values() if ent_type == 'PATHOGEN')

    # Determine the prediction based on counts
    if count_medicalcondition_best > count_medicine_best and count_medicalcondition_best > count_pathogen_best:
        predict_best = "MEDICAL CONDITION"
    elif count_medicine_best > count_medicalcondition_best and count_medicine_best > count_pathogen_best:
        predict_best = "MEDICINE"
    elif count_pathogen_best > count_medicalcondition_best and count_pathogen_best > count_medicine_best:
        predict_best = "PATHOGEN"
    else:
        predict_best = "UNKNOWN"

    if count_medicalcondition_last > count_medicine_last and count_medicalcondition_last > count_pathogen_last:
        predict_last = "MEDICAL CONDITION"
    elif count_medicine_last > count_medicalcondition_last and count_medicine_last > count_pathogen_last:
        predict_last = "MEDICINE"
    elif count_pathogen_last > count_medicalcondition_last and count_pathogen_last > count_medicine_last:
        predict_last = "PATHOGEN"
    else:
        predict_last = "UNKNOWN"

    # Printing tokens
    print("\nToken information for best:")
    print(token_info_best)
    print("\nToken information for last:")
    print(token_info_last)

    # Print the counts
    print("\nCount of 'MEDICALCONDITION' in text:", count_medicalcondition_best)
    print("Count of 'MEDICINE' in text:", count_medicine_best)
    print("Count of 'PATHOGEN' in text:", count_pathogen_best)

    print("\nCount of 'MEDICALCONDITION' in text:", count_medicalcondition_last)
    print("Count of 'MEDICINE' in text:", count_medicine_last)
    print("Count of 'PATHOGEN' in text:", count_pathogen_last)

    # Print the predictions
    print("\nPredict for best:", predict_best)
    print("Predict for last:", predict_last)

    return { "predict_best": predict_best, "predict_last": predict_last }