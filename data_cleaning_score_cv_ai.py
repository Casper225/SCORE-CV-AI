# Installations des librairies

!pip install spacy langdetect unidecode phonenumbers

!python -m spacy download fr_core_news_sm
!python -m spacy download en_core_web_sm


# Importations des bibliothèques

import re
import logging
from typing import Dict, List, Optional, Set

import spacy
from spacy.language import Language

from langdetect import detect, DetectorFactory
from unidecode import unidecode
import phonenumbers

# CONFIGURATION

DetectorFactory.seed = 0


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# MODELES SPACY


SPACY_MODELS = {

    "fr": "fr_core_news_sm",

    "en": "en_core_web_sm"

}

# TERMES TECHNIQUES ATS A PROTEGER

PROTECTED_TERMS: Set[str] = {

    "machine learning",
    "deep learning",
    "data science",
    "data analysis",
    "artificial intelligence",
    "natural language processing",
    "computer vision",

    "computer science",

    "scikit learn",
    "scikit-learn",

    "open cv",
    "opencv",

    "power bi",
    "tableau",

    "amazon web services",
    "google cloud platform",
    "microsoft azure",

    "sql",
    "nosql",

    "c++",
    "c#",
    ".net"

}



# NORMALISATION COMPETENCES

SKILL_MAPPING = {


    "ml":
        "machine learning",

    "dl":
        "deep learning",

    "ai":
        "artificial intelligence",

    "ia":
        "intelligence artificielle",

    "nlp":
        "natural language processing",

    "cv":
        "computer vision",

    "sklearn":
        "scikit learn",

    "scikit-learn":
        "scikit learn",

    "opencv":
        "open cv",

    "aws":
        "amazon web services",

    "gcp":
        "google cloud platform",

    "azure":
        "microsoft azure",

    "powerbi":
        "power bi"

}



TECH_SYMBOLS = {

    "+",
    "#",
    ".",
    "-"

}



# CREATION CLASS CLEANER

class CVCleaner:


    def __init__(self):

        self.language = None

        self.nlp: Optional[Language] = None

        self.load_spacy_model("en")

# CHARGEMENT SPACY DYNAMIQUE

def load_spacy_model(
            self,
            language:str
    ):

        """
        Charge le modèle spaCy FR ou EN.
        """


        try:

            model = SPACY_MODELS.get(
                language
            )


            self.nlp = spacy.load(
                model
            )


            self.language = language


            logger.info(
                f"spaCy chargé : {model}"
            )


        except Exception as error:


            logger.warning(
                f"Impossible de charger {language}: {error}"
            )


            self.nlp = None

# DETECTION LANGUE

def detect_language(
            self,
            text:str
    )->str:


        try:


            language = detect(text)


            if language.startswith("fr"):

                lang="fr"

            else:

                lang="en"



            if lang != self.language:

                self.load_spacy_model(
                    lang
                )


            return lang



        except Exception:


            return self.language or "en"


# NORMALISATION TEXTE

def normalize_text(
            self,
            text:str
    )->str:


        text=text.lower()


        text=unidecode(
            text
        )


        text=re.sub(
            r"\s+",
            " ",
            text
        )


        return text.strip()



# NORMALISATION COMPETENCES

def normalize_skills(
            self,
            text:str
    )->str:



        for key,value in SKILL_MAPPING.items():


            text=re.sub(

                rf"\b{re.escape(key)}\b",

                value,

                text,

                flags=re.I

            )


        return text



# NETTOYAGE CARACTERES

def clean_special_characters(
            self,
            text:str
    )->str:


        pattern=(

            r"[^a-zA-Z0-9\s"

            +re.escape(
                "".join(TECH_SYMBOLS)
            )

            +"]"

        )


        text=re.sub(
            pattern,
            " ",
            text
        )


        return re.sub(
            r"\s+",
            " ",
            text
        ).strip()

# EXTRACTION EMAIL

def extract_emails(
            self,
            text:str
    )->List[str]:


        return list(
            set(
                re.findall(

                    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",

                    text

                )
            )
        )



# EXTRACTION TELEPHONE

def extract_phones(
            self,
            text:str
    )->List[str]:


        phones=[]


        matches=re.findall(

            r"\+?\d[\d\s().-]{8,}",

            text

        )



        for number in matches:


            try:


                parsed=phonenumbers.parse(
                    number,
                    None
                )


                if phonenumbers.is_valid_number(parsed):

                    phones.append(
                        phonenumbers.format_number(
                            parsed,
                            phonenumbers.PhoneNumberFormat.INTERNATIONAL
                        )
                    )


            except:

                continue



        return list(set(phones))


# EXTRACTION DATES

def extract_dates(
            self,
            text:str
    )->List[str]:


        return list(
            set(
                re.findall(
                    r"\b(?:19|20)\d{2}\b",
                    text
                )
            )
        )

# EXTRACTION SECTIONS CV

def extract_sections(
            self,
            text:str
    )->Dict[str,str]:


        sections={}


        patterns={


            "profile":
            r"(profil|summary|about|objective)",


            "experience":
            r"(experience|experiences|work history)",


            "education":
            r"(formation|education|diplome|degree)",


            "skills":
            r"(competences|skills|technical skills)",


            "certifications":
            r"(certification|certifications)",


            "projects":
            r"(projets|projects)",


            "languages":
            r"(langues|languages)"

        }



        lines=text.split("\n")


        current=None



        for line in lines:


            clean=line.lower().strip()



            found=False


            for name,pattern in patterns.items():


                if re.search(
                    pattern,
                    clean
                ):

                    current=name

                    sections[current]=""

                    found=True

                    break



            if not found and current:


                sections[current]+=line+"\n"




        return sections

    # PROTECTION TERMES TECHNIQUES

def protect_terms(
            self,
            text:str
    )->Dict[str,Dict[str,str]]:


        """
        Protège les termes techniques avant la lemmatisation.
        """

        mapping={}


        protected_text=text


        for index,term in enumerate(PROTECTED_TERMS):


            token=f"TERM_{index}"


            if term in protected_text:


                protected_text=protected_text.replace(

                    term,

                    token

                )


                mapping[token]=term



        return {

            "text":protected_text,

            "mapping":mapping

        }



# RESTAURATION TERMES

def restore_terms(
            self,
            text:str,
            mapping:Dict[str,str]
    )->str:


        for token,value in mapping.items():


            text=text.replace(

                token,

                value

            )


        return text


    # =================================================
    # LEMMATISATION NLP
    # =================================================


def lemmatize(
            self,
            text:str
    )->str:



        #Lemmatisation avec spaCy.



        if self.nlp is None:

            logger.warning(
                "Aucun modèle spaCy disponible"
            )

            return text



        protected=self.protect_terms(
            text
        )



        doc=self.nlp(

            protected["text"]

        )



        tokens=[]



        for token in doc:


            if not token.is_stop:


                tokens.append(

                    token.lemma_

                )



        result=" ".join(tokens)



        result=self.restore_terms(

            result,

            protected["mapping"]

        )



        return result





    # =================================================
    # PIPELINE COMPLET
    # =================================================


def process(
            self,
            cv_text:str
    )->Dict:


        """
        Pipeline complet de nettoyage CV.
        """


        if not cv_text:


            raise ValueError(
                "Le CV est vide"
            )



        # Détection langue

        language=self.detect_language(

            cv_text

        )



        # Normalisation texte

        text=self.normalize_text(

            cv_text

        )



        # Normalisation compétences ATS

        text=self.normalize_skills(

            text

        )



        # Extraction informations

        emails=self.extract_emails(

            cv_text

        )


        phones=self.extract_phones(

            cv_text

        )


        dates=self.extract_dates(

            cv_text

        )


        sections=self.extract_sections(

            cv_text

        )



        # Nettoyage

        text=self.clean_special_characters(

            text

        )



        # NLP

        text=self.lemmatize(

            text

        )



        return {


            "language":language,


            "clean_text":text,


            "contacts":{


                "emails":emails,


                "phones":phones

            },


            "dates":dates,


            "sections":sections


        }




