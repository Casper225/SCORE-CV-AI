# Installation des packages

!python -m spacy download fr_core_news_sm
!python -m spacy download en_core_web_sm
!pip install spacy scikit-learn pandas

# Importation des bibliothèques

import spacy

import random
import json
import shutil

import pandas as pd

from sklearn.model_selection import train_test_split

#from spacy.util import filter_spans  # Récupère l'utilitaire de filtrage
from spacy.training import Example

from google.colab import files

# Définition es labels NER : Le modèle doit savoir quelles informations chercher

LABELS = ["PERSON","JOB_TITLE","COMPANY","SKILL","EDUCATION","CERTIFICATION","EXPERIENCE","DATE","LOCATION","LANGUAGE"]

# Création du dataset hybride : Un modèle NER a besoin d’exemples annotés(300 CV générés automatiquementn,annotations automatiques)

names = ["Lionel KOUAKOU","Jean Dupont","Marie Martin","Paul Bernard"]


jobs = ["Data Scientist","Data Analyst","Software Engineer","Machine Learning Engineer","Project Manager"]


companies=["Intelcia","Google","Microsoft","Orange","Amazon"]


skills=["Python","SQL","Machine Learning","TensorFlow","Power BI","AWS"]


educations=["Licence Informatique","Master Data Science","Computer Science Degree"]


certifications=["NVIDIA Machine Learning","Microsoft Power BI","AWS Certification"]


locations=["Abidjan","Paris","London"]


dataset=[]



for i in range(300):


    person=random.choice(names)

    job=random.choice(jobs)

    company=random.choice(companies)

    skill=random.choice(skills)

    education=random.choice(educations)

    certification=random.choice(certifications)

    location=random.choice(locations)



    text=f"""

    {person} est {job}
    chez {company}.

    Compétences :
    {skill}

    Formation :
    {education}

    Certification :
    {certification}

    Localisation :
    {location}

    """



    entities=[]



    def add_entity(value,label):

        start=text.find(value)

        end=start+len(value)


        entities.append(

            (

            start,

            end,

            label

            )

        )



    add_entity(person,"PERSON")

    add_entity(job,"JOB_TITLE")

    add_entity(company,"COMPANY")

    add_entity(skill,"SKILL")

    add_entity(education,"EDUCATION")

    add_entity(certification,"CERTIFICATION")

    add_entity(location,"LOCATION")



    dataset.append(

        (

        text,

        {

        "entities":entities

        }

        )

    )



with open(

"cv_dataset.json",

"w",

encoding="utf-8"

) as f:


    json.dump(

        dataset,

        f,

        ensure_ascii=False,

        indent=4

    )



print(
"Dataset créé :",
len(dataset)
)

# Chargement du dataset

with open("cv_dataset.json","r",encoding="utf-8") as f:

    df=json.load(f)

    print(len(df))

# Séparation entraînement/test  :80% → apprentissage // 20% → évaluation

train_data,test_data=train_test_split(df,test_size=0.2,random_state=42)

# Création du modèle spaCy NER : On crée un modèle vide français

nlp=spacy.blank("fr")

ner=nlp.create_pipe("ner")


for label in LABELS:
    ner.add_label(label)

#Fonction anti-overlap

def remove_overlapping_entities(entities):

    # Trier par longueur (plus longue d'abord)
    entities = sorted(entities, key=lambda x: (x[1] - x[0]), reverse=True)

    clean = []

    for start, end, label in entities:

        overlap = False

        for s, e, l in clean:
            if not (end <= s or start >= e):
                overlap = True
                break

        if not overlap:
            clean.append((start, end, label))

    return clean

#Nettoyage du dataset AVANT entraînement
clean_data = []

for text, ann in train_data:

    entities = ann["entities"]

    clean_entities = remove_overlapping_entities(entities)

    clean_data.append(
        (text, {"entities": clean_entities})
    )

train_data = clean_data

from spacy.tokens import doc
# Entraînement du modèle:Le modèle apprend à reconnaître les entités

nlp = spacy.blank("xx")
ner = nlp.add_pipe("ner")

LABELS = [
    "PERSON","JOB_TITLE","COMPANY","SKILL",
    "EDUCATION","CERTIFICATION","EXPERIENCE",
    "DATE","LOCATION","LANGUAGE"
]

for label in LABELS:
    ner.add_label(label)

optimizer = nlp.begin_training()

epochs = 50

for epoch in range(epochs):

    random.shuffle(train_data)
    losses = {}

    for text, annotations in train_data:

        doc = nlp.make_doc(text)

        example = Example.from_dict(doc, annotations)

        nlp.update(
            [example],
            drop=0.3,
            sgd=optimizer,
            losses=losses
        )

    print("Epoch", epoch+1, "/", epochs, "Loss:", losses)


# EVALUATION MODELE NER
# Precision - Recall - F1 Score

def evaluate_model(nlp, test_data):

    tp = 0
    fp = 0
    fn = 0


    for text, annotation in test_data:


        # Prédiction modèle
        doc = nlp(text)


        # Entités prédites
        predicted = set(

            (
                ent.start_char,
                ent.end_char,
                ent.label_

            )

            for ent in doc.ents

        )


        # Entités réelles
        # Conversion liste -> tuple
        real = set(

            tuple(entity)

            for entity in annotation["entities"]

        )


        # Comparaison

        tp += len(predicted & real)

        fp += len(predicted - real)

        fn += len(real - predicted)



    precision = (

        tp / (tp + fp)

        if tp + fp > 0

        else 0

    )


    recall = (

        tp / (tp + fn)

        if tp + fn > 0

        else 0

    )


    f1 = (

        2 * precision * recall /
        (precision + recall)

        if precision + recall > 0

        else 0

    )


    return precision, recall, f1

# Lancement des evaluations : Precision - Recall - F1 Score

precision, recall, f1 = evaluate_model(
    nlp,
    test_data
)


print("==============================")

print("Precision :", round(precision,3))

print("Recall    :", round(recall,3))

print("F1 Score  :", round(f1,3))

print("==============================")

# Tester le modèle

test_cv="""

Lionel KOUAKOU est Data Scientist chez Intelcia.

Compétences :
Python et Machine Learning.

Formation :
Licence Informatique.

"""


doc=nlp(test_cv)



for ent in doc.ents:

    print(

        ent.text,

        "---->",

        ent.label_

    )

# Sauvgarde du modèle

MODEL_NAME="score_cv_ai_ner"

nlp.to_disk(MODEL_NAME)
print("Modèle sauvegardé")

# Compression du modèle

shutil.make_archive("score_cv_ai_ner","zip","score_cv_ai_ner")

# Téléchargementdu modèle

files.download("score_cv_ai_ner.zip")
