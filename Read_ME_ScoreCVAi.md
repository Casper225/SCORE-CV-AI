# 🛡️ SCORE CV AI

## Analyse intelligente, Matching et Optimisation des candidatures

**SCORE CV AI** est une solution basée sur l'Intelligence Artificielle et le Natural Language Processing (NLP) permettant d'analyser automatiquement un CV, de le comparer à une offre d'emploi et de produire un **score de compatibilité**, une analyse des compétences et des recommandations d'amélioration.

L'objectif est de transformer un CV non structuré en **données exploitables**, puis de mesurer automatiquement son adéquation avec les exigences d'une opportunité professionnelle.

> **Analysez votre CV. Mesurez votre compatibilité. Optimisez votre candidature.**

---

# 🎯 1. Problématique

Les recruteurs doivent analyser un grand nombre de CV pour identifier rapidement les profils correspondant aux exigences d'un poste.

Cette analyse peut être :

- longue ;
- répétitive ;
- subjective ;
- difficile à standardiser ;
- dépendante des mots-clés présents dans les CV.

Du côté des candidats, il est également difficile de savoir :

- si leur CV correspond réellement à une offre ;
- quelles compétences sont correctement valorisées ;
- quelles compétences sont manquantes ;
- quels éléments doivent être améliorés avant de postuler.

**SCORE CV AI** répond à cette problématique en automatisant l'analyse et le matching entre le CV et l'offre d'emploi.

---

# 🚀 2. Objectifs du projet

Le projet poursuit plusieurs objectifs :

- 📄 Extraire automatiquement le contenu d'un CV PDF ou DOCX.
- 🧹 Nettoyer et normaliser les données textuelles.
- 🧠 Utiliser le NLP pour identifier les informations importantes.
- 🔎 Extraire les compétences, expériences, formations et autres entités.
- 🔗 Identifier les relations entre les différentes entités du CV.
- 📊 Transformer les données textuelles en variables exploitables.
- 🧮 Comparer le CV avec une offre d'emploi.
- 🎯 Calculer un score de matching compris entre 0 et 100 %.
- ⚠️ Identifier les compétences manquantes.
- 💡 Générer des recommandations d'amélioration.
- 🌐 Exploiter des offres d'emploi réelles via JSearch API.
- 🖥️ Présenter les résultats dans une interface Streamlit interactive.

---

# 🏗️ 3. Architecture globale du projet

Le pipeline SCORE CV AI est organisé en plusieurs étapes :

```text
                    ┌──────────────────────┐
                    │      CV PDF/DOCX     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     CV Parser        │
                    │ pdfplumber / DOCX    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Data Cleaning      │
                    │      NLP             │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │         NER          │
                    │ Entity Extraction    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Relationship         │
                    │ Extraction           │
                    └──────────┬───────────┘
                               │
                               ▼
          ┌────────────────────┴────────────────────┐
          │                                         │
          ▼                                         ▼
┌──────────────────────┐                 ┌──────────────────────┐
│     CV Data          │                 │    Job Description   │
│    Structuration     │                 │    / JSearch API     │
└──────────┬───────────┘                 └──────────┬───────────┘
           │                                        │
           └────────────────┬───────────────────────┘
                            ▼
                 ┌──────────────────────┐
                 │ Feature Engineering  │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │       TF-IDF         │
                 │ Vector Representation│
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Cosine Similarity    │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Skill Matching       │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Matching / Scoring   │
                 │       Model          │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ Score 0 - 100 %      │
                 │ Écarts & Reco        │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │      Streamlit       │
                 │    Dashboard AI      │
                 └──────────────────────┘
```

---

# 📌 4. Étape 1 — CV Parser

La première étape consiste à récupérer automatiquement le contenu du CV.

SCORE CV AI accepte principalement :

- PDF ;
- DOCX.

### PDF

La bibliothèque `pdfplumber` permet d'extraire le texte contenu dans les différentes pages du document.

### DOCX

`python-docx` permet de récupérer le contenu textuel des documents Word.

Le parser transforme ainsi un document non structuré en texte exploitable par les étapes NLP suivantes.

```text
CV PDF / DOCX
      ↓
Extraction du texte
      ↓
Texte brut exploitable
```

Une gestion des erreurs est également prévue lorsqu'une bibliothèque n'est pas installée ou lorsqu'un document ne peut pas être correctement lu.

---

# 🧹 5. Étape 2 — Data Cleaning & NLP Preprocessing

Le texte extrait d'un CV peut contenir :

- espaces multiples ;
- caractères invisibles ;
- URLs ;
- caractères spéciaux ;
- variations linguistiques ;
- informations difficiles à exploiter directement.

Le preprocessing permet de nettoyer et normaliser ces informations.

Cette étape prépare les données pour les modèles NLP et les algorithmes de matching.

Les opérations peuvent notamment inclure :

- normalisation du texte ;
- suppression des éléments inutiles ;
- détection de la langue ;
- tokenisation ;
- lemmatisation ;
- gestion des stopwords ;
- conservation des termes techniques importants.

Une attention particulière est portée aux technologies contenant des caractères comme `C++`, `C#`, `Node.js`, etc., afin de ne pas détruire les informations importantes.

---

# 🧠 6. Étape 3 — Named Entity Recognition (NER)

La NER permet d'identifier automatiquement les entités importantes présentes dans un CV.

Exemples :

```text
PERSON
ORG
JOB
SKILL
CERTIFICATION
LOCATION
EDUCATION
DATE
```

L'objectif est de transformer le texte brut en informations structurées.

Exemple :

```text
"Pierre Dupont travaille comme Data Scientist chez ABC depuis 2023."

             ↓

PERSON : Pierre Dupont
JOB : Data Scientist
ORG : ABC
DATE : 2023
```

Cette étape permet à SCORE CV AI de mieux comprendre la structure d'un CV.

---

# 🔗 7. Étape 4 — Relationship Extraction

La Relationship Extraction complète la NER en identifiant les relations entre les entités.

Le projet utilise notamment des relations telles que :

```text
PERSON_HAS_JOB
PERSON_WORKS_AT
PERSON_KNOWS_SKILL
SKILL_IN_JOB
CERTIFICATION_VALIDATES_SKILL
PERSON_FROM_LOCATION
```

Exemple :

```text
Pierre Dupont
      │
      ├── PERSON_HAS_JOB ──► Data Scientist
      │
      ├── PERSON_WORKS_AT ─► ABC
      │
      └── PERSON_KNOWS_SKILL ─► Python
```

Cette représentation permet de passer d'une simple extraction d'entités à une **compréhension structurée du profil candidat**.

---

# 🌐 8. Étape 5 — Intégration des offres d'emploi avec JSearch API

Pour rendre le système plus proche d'un environnement réel, SCORE CV AI peut intégrer des offres d'emploi provenant de **JSearch API**.

Le système peut récupérer notamment :

- titre du poste ;
- entreprise ;
- description ;
- localisation ;
- compétences recherchées ;
- exigences du poste.

Le CV peut ensuite être comparé à des offres réelles plutôt qu'à une simple description statique.

```text
JSearch API
     ↓
Offres d'emploi
     ↓
Nettoyage / structuration
     ↓
Matching avec le CV
```

La clé API est conservée dans une variable d'environnement et ne doit jamais être publiée directement dans le dépôt GitHub.

---

# 🔄 9. Étape 6 — Data Integration

Cette étape constitue le **cœur de l'intégration technique** du projet.

Les informations provenant des différents modules sont regroupées :

```text
CV Parser
    +
NLP Cleaning
    +
NER
    +
Relationship Extraction
    +
Job Data
    +
JSearch API
```

Les données sont ensuite transformées en une structure commune permettant de comparer :

```text
Profil candidat
        VS
Exigences de l'offre
```

Cette intégration permet de connecter les différentes briques développées indépendamment dans un pipeline cohérent.

---

# 🧮 10. Étape 7 — Feature Engineering

Le Feature Engineering transforme les informations extraites en caractéristiques exploitables par le système de matching.

Les caractéristiques peuvent notamment représenter :

- nombre de compétences correspondantes ;
- nombre de compétences manquantes ;
- présence d'une compétence requise ;
- similarité textuelle ;
- expérience ;
- technologies ;
- certifications ;
- langues ;
- soft skills.

Exemple :

```text
Python          → 1
Docker          → 1
Kubernetes      → 0
SQL             → 1
NLP             → 1
```

Ces caractéristiques permettent ensuite de construire un score plus représentatif.

---

# 📊 11. Étape 8 — TF-IDF

Le TF-IDF permet de transformer les textes du CV et de l'offre en représentations numériques.

Il mesure l'importance des termes dans les documents.

SCORE CV AI utilise notamment :

```python
TfidfVectorizer(
    ngram_range=(1, 2),
    sublinear_tf=True
)
```

L'utilisation de unigrammes et bigrammes permet de mieux prendre en compte certaines expressions techniques.

Exemple :

```text
Machine Learning
Data Science
Deep Learning
Natural Language Processing
```

---

# 📐 12. Étape 9 — Cosine Similarity

Après la vectorisation TF-IDF, la similarité cosinus permet de mesurer la proximité entre le CV et l'offre.

Le résultat est transformé en score de similarité.

```text
CV
 ↓
TF-IDF
 ↓
Vecteur numérique
       ↘
        Cosine Similarity
       ↗
Vecteur numérique
 ↑
Offre
```

Plus les représentations sont proches, plus la similarité est élevée.

Cette approche constitue la première composante du matching hybride.

---

# 🎯 13. Étape 10 — Skill Matching

La similarité textuelle est complétée par un matching explicite des compétences.

Le système vérifie les compétences demandées par l'offre et leur présence dans le CV.

Trois catégories sont produites :

### ✅ Compétences trouvées

Compétences demandées et présentes dans le CV.

### ⚠️ Compétences manquantes

Compétences demandées mais absentes du CV.

### 💡 Recommandations

Compétences ou domaines pouvant être renforcés par le candidat.

Cette approche permet d'obtenir une analyse plus compréhensible qu'un simple score.

---

# 🧠 14. Étape 11 — Matching Model & Scoring

Le système utilise actuellement un **matching hybride** combinant :

```text
60 % → TF-IDF + Cosine Similarity
40 % → Skill Matching
```

Le score final est normalisé entre :

```text
0 %
   ↓
50 %
   ↓
80 %
   ↓
100 %
```

Avec une interprétation :

```text
≥ 80 %  → EXCELLENT
≥ 65 %  → TRÈS BON
≥ 50 %  → MOYEN
< 50 %  → À AMÉLIORER
```

Cette combinaison permet de ne pas dépendre uniquement de la présence exacte des mots-clés.

---

# 💡 15. Étape 12 — Recommandations

SCORE CV AI ne se limite pas à afficher un score.

Le système identifie également les éléments qui peuvent améliorer la candidature.

Exemple :

```text
Score : 72 %

✅ Python
✅ Docker
✅ Git
✅ Data Science

⚠️ Kubernetes

💡 Recommandations :
- Renforcer Kubernetes
- Développer les compétences Cloud
- Approfondir Spark
```

L'objectif est de transformer le matching en **outil d'aide à la décision**.

---

# 🖥️ 16. Étape 13 — Interface Streamlit

L'interface Streamlit constitue la couche finale du projet.

Elle permet à l'utilisateur de :

- téléverser son CV ;
- saisir une offre d'emploi ;
- lancer l'analyse ;
- visualiser le score ;
- consulter les compétences détectées ;
- identifier les écarts ;
- consulter les recommandations ;
- visualiser les soft skills ;
- visualiser les langues détectées.

L'interface est organisée sous forme de dashboard :

```text
┌─────────────────────────────────────────────┐
│              🛡️ SCORE CV AI                 │
│       Analyse intelligente du CV            │
├───────────────────────┬─────────────────────┤
│ 📄 MON CV             │ 🎯 SCORE MATCHING    │
├───────────────┬───────┼─────────────────────┤
│ 💼 OFFRE      │ 👤    │ 🔎 ANALYSE           │
│               │CONTACT│   DÉTAILLÉE          │
├───────────────┴───────┴─────────────────────┤
│ 💻 TECH       │ 🤝 SOFT SKILLS │ 🌍 LANGUES │
├─────────────────────────────────────────────┤
│              📊 RÉSUMÉ                      │
└─────────────────────────────────────────────┘
```

Le design utilise un thème professionnel **émeraude / gris clair** afin de donner à l'application une identité proche d'un produit SaaS de recrutement.

---

# 📦 17. Technologies utilisées

## Langage

- Python

## Data Science

- Pandas
- NumPy
- Scikit-learn

## NLP

- spaCy
- NLTK
- langdetect

## Extraction de documents

- pdfplumber
- python-docx
- EasyOCR pour les documents nécessitant une extraction OCR

## Machine Learning

- TF-IDF
- Cosine Similarity
- modèles de matching/scoring

## API

- JSearch API

## Interface

- Streamlit
- HTML/CSS personnalisé

## Environnement

- Google Colab
- GitHub
- Python

---

# 📁 18. Organisation recommandée du projet

```text
SCORE-CV-AI/
│
├── app.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── datasets/
│
├── models/
│   ├── ner_model/
│   └── scoring_model/
│
├── src/
│   │
│   ├── cv_parser.py
│   ├── preprocessing.py
│   ├── relationship_extraction.py
│   ├── experience_extractor.py
│   ├── feature_engineering.py
│   ├── scoring.py
│   ├── score_cv_ai_model.py
│   └── jsearch_client.py
│
├── notebooks/
│   ├── 01_cv_parsing.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_ner.ipynb
│   ├── 04_relationship_extraction.ipynb
│   └── 05_data_integration_model_building.ipynb
│
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

# ⚙️ 19. Installation

Cloner le repository :

```bash
git clone https://github.com/VOTRE-USERNAME/score-cv-ai.git
cd score-cv-ai
```

Créer un environnement virtuel :

```bash
python -m venv venv
```

Activer l'environnement sous Windows :

```bash
venv\Scripts\activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

Ou installer les principales bibliothèques :

```bash
pip install streamlit
pip install pdfplumber
pip install python-docx
pip install scikit-learn
pip install pandas
pip install numpy
pip install spacy
pip install nltk
pip install langdetect
pip install easyocr
```

---

# 🔐 20. Configuration de l'API JSearch

Créer un fichier `.env` :

```env
JSEARCH_API_KEY=votre_cle_api
```

Ne jamais publier cette clé sur GitHub.

Ajouter `.env` dans `.gitignore` :

```text
.env
__pycache__/
*.pyc
venv/
.ipynb_checkpoints/
```

---

# ▶️ 21. Lancement de l'application

Depuis le dossier du projet :

```bash
streamlit run app.py
```

L'application ouvre alors le dashboard SCORE CV AI dans le navigateur.

---

# 🔄 22. Fonctionnement utilisateur

Le fonctionnement général est volontairement simple :

### Étape 1 — Importer le CV

L'utilisateur téléverse son CV au format PDF ou DOCX.

### Étape 2 — Ajouter l'offre

L'utilisateur colle le texte de l'offre d'emploi.

### Étape 3 — Lancer l'analyse

SCORE CV AI extrait et traite automatiquement les informations.

### Étape 4 — Calculer le matching

Le moteur combine :

```text
TF-IDF
+
Cosine Similarity
+
Skill Matching
```

### Étape 5 — Consulter les résultats

L'utilisateur obtient :

```text
🎯 Score de matching
✅ Compétences trouvées
⚠️ Compétences manquantes
💡 Recommandations
💻 Compétences techniques
🤝 Soft Skills
🌍 Langues
```

---

# 📊 23. Exemple de résultat

Pour une offre :

```text
Lead Developer Python
5 ans d'expérience
Docker
Kubernetes
Git
SQL
Cloud
```

Le système peut produire :

```text
╔══════════════════════════════╗
║       SCORE MATCHING         ║
║            84 %              ║
║          EXCELLENT            ║
╚══════════════════════════════╝

✅ Python
✅ Docker
✅ Git
✅ SQL

⚠️ Kubernetes
⚠️ Cloud

💡 Recommandations

• Renforcer Kubernetes
• Développer les compétences Cloud
```

---

# 🧪 24. Gestion des erreurs

Le projet prévoit plusieurs mécanismes de sécurité :

- vérification de la présence du fichier ;
- vérification du format ;
- gestion des bibliothèques optionnelles ;
- gestion des erreurs de lecture PDF/DOCX ;
- gestion des erreurs TF-IDF ;
- vérification de la présence du CV ;
- vérification de la présence de l'offre ;
- limitation du score entre 0 et 100.

L'objectif est d'éviter qu'une erreur sur une étape fasse nécessairement tomber toute l'application.

---

# 📈 25. Évolution du projet

Le moteur actuel constitue une base fonctionnelle et modulaire.

Les prochaines améliorations peuvent inclure :

### 🔹 Matching sémantique avancé

Ajouter des modèles d'embeddings ou Sentence Transformers afin de mieux comprendre les synonymes et les formulations différentes.

```text
"Développeur Python"
        ≈
"Python Software Engineer"
```

### 🔹 Analyse de l'expérience

Comparer :

- années d'expérience ;
- postes occupés ;
- technologies utilisées ;
- niveau de responsabilité.

### 🔹 Extraction plus avancée

Améliorer automatiquement l'extraction :

- nom ;
- entreprise ;
- poste ;
- durée ;
- certification ;
- formation ;
- localisation.

### 🔹 OCR

Utiliser EasyOCR comme fallback pour les CV scannés ou les documents sans couche texte exploitable.

### 🔹 Modèle de scoring avancé

Faire évoluer le scoring hybride vers un modèle supervisé entraîné sur des exemples de CV/offres annotés.

### 🔹 Génération de CV optimisé

Ajouter une fonctionnalité permettant de proposer une version optimisée du CV en fonction de l'offre.

### 🔹 Analyse ATS

Ajouter un module dédié à l'évaluation de la compatibilité avec les systèmes ATS.

---

# 🧠 26. Architecture Machine Learning future

L'évolution cible du système peut être représentée ainsi :

```text
                 CV + JOB
                    │
                    ▼
              NLP Pipeline
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
      NER       Relations     Skills
        │           │           │
        └───────────┼───────────┘
                    ▼
            Feature Engineering
                    │
       ┌────────────┼────────────┐
       ▼            ▼            ▼
     TF-IDF     Embeddings    Experience
       │            │            │
       └────────────┼────────────┘
                    ▼
             Matching Model
                    │
                    ▼
             Scoring Model
                    │
                    ▼
          ┌─────────┴─────────┐
          ▼                   ▼
       Score (%)         Recommendations
```

---

# 🎯 27. Valeur métier

SCORE CV AI peut être utilisé dans plusieurs contextes :

### 👤 Candidat

Pour mesurer la compatibilité d'un CV avec une offre et identifier les compétences à renforcer.

### 🏢 Recruteur

Pour accélérer la présélection et obtenir une première analyse standardisée des candidatures.

### 🧑‍💼 RH

Pour analyser les écarts entre les profils disponibles et les exigences des postes.

### 📊 Plateforme emploi

Pour proposer automatiquement des offres correspondant aux profils des candidats.

---

# 🏆 28. Compétences démontrées par le projet

Ce projet permet de démontrer plusieurs compétences techniques :

**Data Science**

- Data preprocessing
- Feature Engineering
- Vectorisation
- Similarity analysis
- Scoring

**Machine Learning**

- représentation numérique des textes ;
- matching ;
- modèles de scoring ;
- évaluation des performances.

**NLP**

- nettoyage de texte ;
- NER ;
- extraction d'entités ;
- extraction de relations ;
- détection de compétences.

**Data Engineering**

- intégration de plusieurs sources ;
- structuration des données ;
- consommation d'API ;
- pipeline de traitement.

**Software Engineering**

- architecture modulaire ;
- gestion des erreurs ;
- fonctions réutilisables ;
- variables d'environnement ;
- gestion des dépendances.

**Deployment / Product**

- Streamlit ;
- interface utilisateur ;
- dashboard interactif ;
- intégration des modèles dans une application.

---

# 📌 29. État actuel du projet

### ✅ Fonctionnel

- [x] Import CV PDF
- [x] Import CV DOCX
- [x] Extraction du texte
- [x] Préprocessing NLP
- [x] Extraction d'informations
- [x] Matching de compétences
- [x] TF-IDF
- [x] Cosine Similarity
- [x] Scoring hybride
- [x] Identification des écarts
- [x] Recommandations
- [x] Interface Streamlit
- [x] Session State
- [x] Dashboard de résultats

### 🔄 En évolution

- [ ] Intégration complète du modèle de scoring final
- [ ] Connexion complète avec JSearch API
- [ ] Matching sémantique avancé
- [ ] Analyse approfondie de l'expérience
- [ ] OCR avancé
- [ ] Dataset CV/offres annoté plus important
- [ ] Évaluation quantitative du modèle
- [ ] Déploiement cloud

---

# 📊 30. Évaluation du modèle

L'objectif est de ne pas seulement mesurer l'apparence de l'application, mais également la performance du système.

Les futures évaluations porteront notamment sur :

```text
Precision
Recall
F1-Score
Accuracy
Cosine Similarity
Erreur moyenne du score
```

Pour le matching, une validation sur un dataset composé de couples :

```text
CV + Offre + Label de compatibilité
```

permettra d'évaluer objectivement la qualité des prédictions.

---

# 🔒 31. Sécurité et confidentialité

Les CV contenant des données personnelles, le projet doit respecter plusieurs principes :

- ne pas stocker inutilement les CV ;
- ne jamais exposer les clés API ;
- ne pas publier de données personnelles dans GitHub ;
- utiliser des variables d'environnement pour les secrets ;
- anonymiser les datasets utilisés pour l'entraînement ;
- limiter la conservation des documents utilisateurs.

---

# 👨‍💻 . Auteur

**Lionel KOUAKOU**

Data Scientist | Python | Machine Learning | NLP | Data Analytics

Projet personnel de conception et développement d'une solution d'IA appliquée au recrutement et à l'analyse des candidatures.

---

# ⭐ 33. Conclusion

**SCORE CV AI** est un projet de Data Science appliquée combinant **NLP, Machine Learning, Data Integration, Feature Engineering, API, scoring et développement d'application**.

L'objectif n'est pas simplement de produire un pourcentage, mais de construire une chaîne complète :

```text
DOCUMENT
   ↓
DONNÉES
   ↓
NLP
   ↓
STRUCTURATION
   ↓
FEATURE ENGINEERING
   ↓
MATCHING
   ↓
SCORING
   ↓
EXPLICATION
   ↓
RECOMMANDATION
   ↓
DÉCISION
```

Le projet évolue progressivement d'un prototype de matching basé sur les mots-clés vers une plateforme d'analyse de candidatures intégrant des méthodes NLP, des modèles de similarité et des mécanismes de scoring.

> **SCORE CV AI — Transformez votre CV en avantage compétitif.**
