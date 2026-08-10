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

# -*- coding: utf-8 -*-
"""
Relationship_Extraction_Score_CV_AI.ipynb

Partie 4 : Relationship Extraction Module

Objectif :
Extraire les relations entre les entités détectées par NER

Exemple :
Lionel travaille chez Intelcia comme Data Scientist

 PERSON -------- WORKS_AT -------- COMPANY
 PERSON -------- HAS_JOB -------- JOB_TITLE
PERSON -------- HAS_HAS_SKILL ------- SKILL
"""

# ============================================================
# INSTALLATION & IMPORTS
# ============================================================



import spacy
import json
import shutil
import sys # Added import sys

from pathlib import Path
from typing import List, Dict
from collections import defaultdict
from datetime import datetime

try:
    from google.colab import files
    COLAB = True
except:
    COLAB = False


# ============================================================
# CLASSE EXTRACTION RELATIONS
# ============================================================

class RelationshipExtractor:
    """Extraction des relations entre entités NER."""

    def __init__(self, ner_model_path: str):
        """Charge le modèle NER entraîné."""
        print("Chargement du modèle NER...")
        self.nlp = spacy.load(ner_model_path)
        print("Modèle NER chargé")

    def extract_relations(self, text: str, cv_id: str = "unknown") -> List[Dict]:
        """Extrait les 4 relations principales du CV."""
        doc = self.nlp(text)
        entities = self.group_entities(doc)

        relations = []

        # 4 relations
        relations += self.person_job(entities, cv_id)
        relations += self.person_company(entities, cv_id)
        relations += self.person_skill(entities, cv_id)
        relations += self.skill_job(entities, cv_id)

        return self.remove_duplicates(relations)

    # ========================================================
    # GROUPER LES ENTITES
    # ========================================================

    def group_entities(self, doc):
        """Groupe les entités par type."""
        entities = defaultdict(list)

        for ent in doc.ents:
            entities[ent.label_].append({
                "text": ent.text,
                "start": ent.start_char,
                "end": ent.end_char,
                "label": ent.label_
            })

        return entities

    # ========================================================
    # CALCUL DISTANCE
    # ========================================================

    def close(self, e1, e2, distance=80):
        """Vérifie si 2 entités sont proches."""
        gap = min(
            abs(e1["start"] - e2["end"]),
            abs(e2["start"] - e1["end"])
        )
        return gap <= distance

    # ========================================================
    # RELATION 1: PERSON -> JOB
    # ========================================================

    def person_job(self, entities, cv_id):
        """Extrait PERSON_HAS_JOB."""
        results = []

        for person in entities.get("PERSON", []):
            for job in entities.get("JOB_TITLE", []):
                if self.close(person, job):
                    results.append({
                        "relation": "PERSON_HAS_JOB",
                        "source": person["text"],
                        "target": job["text"],
                        "confidence": 0.95,
                        "cv_id": cv_id
                    })

        return results

    # ========================================================
    # RELATION 2: PERSON -> COMPANY
    # ========================================================

    def person_company(self, entities, cv_id):
        """Extrait PERSON_WORKS_AT."""
        results = []

        for person in entities.get("PERSON", []):
            for company in entities.get("COMPANY", []):
                if self.close(person, company, 120):
                    results.append({
                        "relation": "PERSON_WORKS_AT",
                        "source": person["text"],
                        "target": company["text"],
                        "confidence": 0.90,
                        "cv_id": cv_id
                    })

        return results

    # ========================================================
    # RELATION 3: PERSON -> SKILL
    # ========================================================

    def person_skill(self, entities, cv_id):
        """Extrait PERSON_HAS_SKILL."""
        results = []

        for person in entities.get("PERSON", []):
            for skill in entities.get("SKILL", []):
                if self.close(person, skill, 300):
                    results.append({
                        "relation": "PERSON_HAS_SKILL",
                        "source": person["text"],
                        "target": skill["text"],
                        "confidence": 0.85,
                        "cv_id": cv_id
                    })

        return results

    # ========================================================
    # RELATION 4: SKILL -> JOB
    # ========================================================

    def skill_job(self, entities, cv_id):
        """Extrait SKILL_REQUIRED_FOR_JOB."""
        results = []

        for skill in entities.get("SKILL", []):
            for job in entities.get("JOB_TITLE", []):
                if self.close(skill, job, 100):
                    results.append({
                        "relation": "SKILL_REQUIRED_FOR_JOB",
                        "source": skill["text"],
                        "target": job["text"],
                        "confidence": 0.88,
                        "cv_id": cv_id
                    })

        return results

    # ========================================================
    # SUPPRESSION DUPLICATS
    # ========================================================

    def remove_duplicates(self, relations):
        """Supprime les relations dupliquées."""
        unique = []
        seen = set()

        for r in relations:
            key = (r["relation"], r["source"], r["target"])

            if key not in seen:
                seen.add(key)
                unique.append(r)

        return unique


# ========================================================
# GROUPER LES ENTITES
# ========================================================

def group_entities(self, doc):
        """Groupe les entités par type."""
        entities = defaultdict(list)

        for ent in doc.ents:
            entities[ent.label_].append({
                "text": ent.text,
                "start": ent.start_char,
                "end": ent.end_char,
                "label": ent.label_
            })

        return entities

# ========================================================
# CALCUL DISTANCE
# ========================================================

def close(self, e1, e2, distance=80):
        """Vérifie si 2 entités sont proches."""
        gap = min(
            abs(e1["start"] - e2["end"]),
            abs(e2["start"] - e1["end"])
        )
        return gap <= distance

# ========================================================
# RELATION 1: PERSON -> JOB
# ========================================================

def person_job(self, entities, cv_id):
        """Extrait PERSON_HAS_JOB."""
        results = []

        for person in entities.get("PERSON", []):
            for job in entities.get("JOB_TITLE", []):
                if self.close(person, job):
                    results.append({
                        "relation": "PERSON_HAS_JOB",
                        "source": person["text"],
                        "target": job["text"],
                        "confidence": 0.95,
                        "cv_id": cv_id
                    })

        return results

# ========================================================
# RELATION 2: PERSON -> COMPANY
# ========================================================

def person_company(self, entities, cv_id):
        """Extrait PERSON_WORKS_AT."""
        results = []

        for person in entities.get("PERSON", []):
            for company in entities.get("COMPANY", []):
                if self.close(person, company, 120):
                    results.append({
                        "relation": "PERSON_WORKS_AT",
                        "source": person["text"],
                        "target": company["text"],
                        "confidence": 0.90,
                        "cv_id": cv_id
                    })

        return results



    # ========================================================
    # RELATION 3: PERSON -> SKILL
    # ========================================================

def person_skill(self, entities, cv_id):
        """Extrait PERSON_HAS_SKILL."""
        results = []

        for person in entities.get("PERSON", []):
            for skill in entities.get("SKILL", []):
                if self.close(person, skill, 300):
                    results.append({
                        "relation": "PERSON_HAS_SKILL",
                        "source": person["text"],
                        "target": skill["text"],
                        "confidence": 0.85,
                        "cv_id": cv_id
                    })

        return results

# ========================================================
# RELATION 4: SKILL -> JOB
# ========================================================

def skill_job(self, entities, cv_id):
        """Extrait SKILL_REQUIRED_FOR_JOB."""
        results = []

        for skill in entities.get("SKILL", []):
            for job in entities.get("JOB_TITLE", []):
                if self.close(skill, job, 100):
                    results.append({
                        "relation": "SKILL_REQUIRED_FOR_JOB",
                        "source": skill["text"],
                        "target": job["text"],
                        "confidence": 0.88,
                        "cv_id": cv_id
                    })

        return results

 # ========================================================
 # SUPPRESSION DUPLICATS
 # ========================================================

def remove_duplicates(self, relations):
        """Supprime les relations dupliquées."""
        unique = []
        seen = set()

        for r in relations:
            key = (r["relation"], r["source"], r["target"])

            if key not in seen:
                seen.add(key)
                unique.append(r)

        return unique


# ============================================================
#  ÉVALUATION (P/R/F1)
# ============================================================

def evaluate_relations(predictions, truth):
    """
    Évalue les relations extraites.

    Args:
        predictions: relations extraites par le modèle
        truth: relations annotées (vérité)

    Returns:
        Dict avec Precision, Recall, F1
    """

    def normalize(x):
        """Normalise une relation."""
        return (
            x["relation"],
            x["source"].strip().lower(),
            x["target"].strip().lower()
        )

    # Conversion en set
    pred = set(normalize(x) for x in predictions)
    real = set(normalize(x) for x in truth)

    # Calcul TP / FP / FN
    tp = len(pred & real)        # Vrais positifs
    fp = len(pred - real)        # Faux positifs
    fn = len(real - pred)        # Faux négatifs

    # Calcul Precision / Recall / F1
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall) > 0
        else 0
    )

    return {
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1": round(f1, 3),
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "num_extracted": len(pred),
        "num_gold": len(real)
    }



# ============================================================
#  SAUVEGARDE JSON
# ============================================================

def save_json(relations, name="relations_cv"):
    """Sauvegarde les relations en JSON."""
    with open(name + ".json", "w", encoding="utf-8") as f:
        json.dump(relations, f, indent=4, ensure_ascii=False)

    print(f"JSON sauvegardé: {name}.json")
    return name + ".json"



# ============================================================
#  COMPRESSION ZIP
# ============================================================

def create_zip(filename="score_cv_ai_relation"):
    """Crée le ZIP et le télécharge (Colab only)."""
    shutil.make_archive(filename, "zip", ".")
    print(f" ZIP créé: {filename}.zip")

    if COLAB:
        print(" Téléchargement en cours...")
        files.download(filename + ".zip")

    return filename + ".zip"

#==========================================================
#TEST COMPLET
#==========================================================


import sys # Assurez-vous que sys est importé

if __name__ == "__main__":

    print("\n" + "="*70)
    print("RELATIONSHIP EXTRACTION - SCORE CV AI")
    print("(Version SIMPLIFIÉE - Sans ZIP)")
    print("="*70)

    model_initialized = False # Flag pour vérifier si le modèle est chargé

    # ===== ÉTAPE 1: Charger NER =====
    print("\n[ÉTAPE 1] Chargement du modèle NER...")
    try:
        extractor = RelationshipExtractor("score_cv_ai_ner")
        model_initialized = True
    except OSError as e:
        print(f"❌ Erreur: {e}")
        print("   Vérifie que le dossier 'score_cv_ai_ner' existe")
        print("   Exécute d'abord: entity_recognition_score_cv_ai.py")
        sys.exit(1) # Utilise sys.exit(1) pour arrêter l'exécution dans le notebook

    if model_initialized:
        # ===== ÉTAPE 2: Extraire relations =====
        print("\n[ÉTAPE 2] Extraction des relations...")

        test_cv = """
        Lionel KOUAKOU est Data Scientist chez Intelcia.

        Compétences:
        Python, Machine Learning, TensorFlow, SQL, Power BI.

        Formation:
        Licence Informatique, Master Data Science.

        Certifications:
        NVIDIA Machine Learning, AWS Certification.

        Localisation:
        Abidjan, Côte d'Ivoire.
        """

        relations = extractor.extract_relations(test_cv, cv_id="lionel_001")

        print(f"\n✅ {len(relations)} relations extraites:")
        print("-" * 70)

        for i, rel in enumerate(relations, 1):
            print(f"\n{i}. {rel['relation']}")
            print(f"   {rel['source']} → {rel['target']}")
            print(f"   Confiance: {rel['confidence']:.2f}")

        # ===== ÉTAPE 3: Évaluer =====
        print("\n" + "="*70)
        print("[ÉTAPE 3] Évaluation (Precision/Recall/F1)")
        print("="*70)

        gold_relations = [
            {"relation": "PERSON_HAS_JOB", "source": "Lionel KOUAKOU", "target": "Data Scientist"},
            {"relation": "PERSON_WORKS_AT", "source": "Lionel KOUAKOU", "target": "Intelcia"},
            {"relation": "PERSON_HAS_SKILL", "source": "Lionel KOUAKOU", "target": "Python"},
            {"relation": "PERSON_HAS_SKILL", "source": "Lionel KOUAKOU", "target": "Machine Learning"},
            {"relation": "SKILL_REQUIRED_FOR_JOB", "source": "Python", "target": "Data Scientist"},
        ]

        metrics = evaluate_relations(relations, gold_relations)

        print(f"\n{'-'*70}")
        print(f"Precision: {metrics['precision']:.3f}")
        print(f"Recall:    {metrics['recall']:.3f}")
        print(f"F1 Score:  {metrics['f1']:.3f}")
        print(f"{'-'*70}")
        print(f"\nDétails:")
        print(f"  True Positives:  {metrics['tp']}")
        print(f"  False Positives: {metrics['fp']}")
        print(f"  False Negatives: {metrics['fn']}")
        print(f"  Extraites:       {metrics['num_extracted']}")
        print(f"  Attendues:       {metrics['num_gold']}")

        # ===== ÉTAPE 4: Sauvegarder =====
        print("\n" + "="*70)
        print("[ÉTAPE 4] Sauvegarde des résultats")
        print("="*70)

        json_file = save_json(relations) # Correction: utilize save_json avec seulement les relations

        # ===== RÉSUMÉ FINAL =====
        print("\n" + "="*70)
        print("✅ SECTION 4 TERMINÉE - RELATIONSHIP EXTRACTION")
        print("="*70)
        print(f"""
        📊 RÉSULTATS:
        ├─ Relations extraites: {len(relations)}
        ├─ Precision: {metrics['precision']:.3f}
        ├─ Recall: {metrics['recall']:.3f}
        ├─ F1 Score: {metrics['f1']:.3f}
        │
        📁 FICHIER GÉNÉRÉ:
        ├─ {json_file} ✅
        │  (Petit fichier, facile à télécharger)
        │
        🎯 POUR LA SOUTENANCE:
        ├─ Score CV AI NER: score_cv_ai_ner.zip ✅
        ├─ Code Relationship: relationship_extraction_*.py ✅
        ├─ Résultats: {json_file} ✅
        └─ GitHub: Code source complet ✅
        """)
