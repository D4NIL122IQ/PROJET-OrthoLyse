import json
import csv
from fpdf import FPDF #type:ignore
from docx import Document #type:ignore

def exporte_json(chemin, data):
    """
    Exporte les données en format JSON.
    """
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    #print(f"Données exportées en JSON : {chemin}")

def exporte_txt(chemin, data):
    """
    Exporte les données en format texte (.txt).
    Chaque clé-valeur sera écrite ligne par ligne.
    """
    with open(chemin, "w", encoding="utf-8") as f:
        for cle, valeur in data.items():
            f.write(f"{cle}: {valeur}\n")
    #print(f"Données exportées en TXT : {chemin}")

def exporte_csv_column(chemin, data):
    """
    Exporte les données en format CSV.
    Les clés du dictionnaire seront utilisées comme en-tête.
    """
    with open(chemin, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Clé", "Valeur"])  # En-tête
        for cle, valeur in data.items():
            writer.writerow([cle, valeur])  # Chaque ligne correspond à clé-valeur
    #print(f"Données exportées en CSV : {chemin}")

def exporte_csv_row(chemin, data):
    """
    Exporte les données en format CSV sous forme de tableau.
    Les clés du dictionnaire sont utilisées comme en-têtes des colonnes.
    """
    with open(chemin, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Écrit l'en-tête : les clés du dictionnaire
        writer.writerow(data.keys())

        values = [v if isinstance(v, list) else [v] for v in data.values()] #pour transformer tout les element en liste

        # Transposer les colonnes en lignes
        rows = zip(*values) #l'etoile sert a decompacter les element cette a dire [[1,2,3],[a,b,c]] devient [1,2,3],[a,b,c]
        writer.writerows(rows)  # Écrit les lignes

def exporte_pdf(chemin, data):
    """
    Exporte les données en format PDF.
    Les clés et les valeurs seront affichées sous forme de texte.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.cell(200, 10, txt="Exportation des données", ln=True, align="C")
    pdf.ln(10)  # Saut de ligne

    for cle, valeur in data.items():
        pdf.cell(0, 10, txt=f"{cle}: {valeur}", ln=True)
    pdf.output(chemin)
    #print(f"Données exportées en PDF : {chemin}")

def exporte_docx(chemin, data):
    """
    Exporte les données en format Word (.docx).
    Chaque clé-valeur sera écrite sous forme de paragraphes.
    """
    doc = Document()
    doc.add_heading("Exportation des données", level=1)

    for cle, valeur in data.items():
        doc.add_paragraph(f"{cle}: {valeur}")

    doc.save(chemin)
    #print(f"Données exportées en DOCX : {chemin}")

# Exemple d'utilisation
data = {
        "nom": "Alice",
        "âge": 25,
        "profession": "Développeuse",
        "ville": "Paris"
    }


#exporte_json("data.json", data)
#exporte_txt("data.txt", data)
#exporte_csv_column("datac.csv", data)
#exporte_csv_row("datar.csv", data)

#exporte_pdf("data.pdf", data)
#exporte_docx("data.docx", data)
