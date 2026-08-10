!pip install pdfplumber easyocr pdf2image python-docx
!apt-get install -y poppler-utils


# importantion de la bibliothèques pour extraction pdf doc et txt
import pdfplumber
import easyocr
from pdf2image import convert_from_bytes
from docx import Document
import io



# Initialiser EasyOCR une fois
print("Initialisation EasyOCR")
reader = easyocr.Reader(['fr', 'en'], gpu=False)
print("Prêt\n")

# Création de la la class textextractor

class TextExtractor:
    """Extracteur de texte multi-format"""

    def __init__(self):
        """Initialiser l'extracteur"""
        global reader
        self.reader = reader

# Extraction PDF : Lire un fichier PDF et extraire son texte

def extract_pdf(self, pdf_bytes):

    # Variable qui va stocker le texte extrait
    text = ""


    # Tentative d'extraction avec pdfplumber

    try:

        with pdfplumber.open(pdf_bytes) as pdf:


            # Parcourir toutes les pages du PDF

            for page in pdf.pages:


                # Extraire le texte de la page

                page_text = page.extract_text()


                # Vérifier si du texte existe

                if page_text:

                    text += page_text

        # Vérification si l'extraction PDF a réussi

        if len(text.strip()) > 50:

            print("PDF texte détecté")

            return text



        else:

            print("PDF sans texte détecté")

            return None



    except Exception as e:

        print(
            f"Erreur lors de l'extraction du fichier {pdf_bytes} avec pdfplumber : {e}"
        )

        return None




# Utilisation OCR

def extract_text_from_pdf_bytes(pdf_bytes):


    # PDF scanné : utilisation OCR
    print(" PDF image détecté : lancement OCR")

    # Transformation du PDF en images
    print("    Conversion PDF → Images")
    images = convert_from_bytes(pdf_bytes)
    print(f"    {len(images)} page(s) détectée(s)")

    ocr_text = ""

    # Lecture de chaque page image
    for page_num, image in enumerate(images, 1):
        print(f"    OCR page {page_num}/{len(images)}...", end=" ")


        results = reader.readtext(image)

        # Parcourir les résultats
        for item in results:
            # item[1] correspond au texte détecté
            ocr_text += item[1] + " "

        print("OK")

    # Retour du texte obtenu par OCR
    print(f"   {len(ocr_text)} caractères extraits\n")
    return ocr_text



# Extraction document word :Lire un CV Word

def extract_docx(self, docx_bytes):



        # Ouverture du document Word

        document = Document(io.BytesIO(docx_bytes))


        text = ""


        # Un document Word est composé
        # de plusieurs paragraphes

        for paragraph in document.paragraphs:



            # On récupère chaque ligne

            text += paragraph.text + "\n"



        return text




# Exraction fichier TXT Un fichier TXT contient déjà du texte Il suffit de le décoder.

def extract_txt(self, txt_bytes):



        return txt_bytes.decode(
            "utf-8",
            errors="ignore"
        )



# Routeur automatique : Cette fonction décide automatiquement quelle méthode utiliser.

def extract(self,file_bytes,file_type):


        if file_type == "pdf":


            return self.extract_pdf(
                file_bytes
            )



        elif file_type == "docx":


            return self.extract_docx(
                file_bytes
            )



        elif file_type == "txt":


            return self.extract_txt(
                file_bytes
            )



        else:


            return "Format non supporté"
