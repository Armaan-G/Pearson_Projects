def get_suggest_disease(symptoms):
    #{"disease": "COVID-19"},{"disease": "Flu"}
    db = {"fever": ["COVID-19","Flu"],
    "dry cough": ["COVID-19"],
    "shortness of breath": ["COVID-19", "Asthma"],
    "loss of taste/smell": ["COVID-19"],
    "runny nose": ["Common Cold"],
    "sneezing": ["Common Cold", "Allergies"],
    "cough": ["Common Cold", "Flu", "Asthma"],
    "fatigue": ["Common Cold"],
    "body aches": ["Flu"],
    "chills": ["Flu"],
    "headache": ["Flu"],
    "itchy eyes": ["Allergies"],
    "nasal congestion": ["Allergies"],
    "skin rash": ["Allergies"],
    "wheezing": ["Asthma"],
    "rash": ["eczema"]}

    if (symptoms in db):
        return db.get(symptoms)
    else:
        return "disease not found"
