import mysql.connector
from faker import Faker
import random
from datetime import datetime



db_config = {
    "host": "localhost",
    "user": "root",
    "password": "houdhoud",
}
 

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS SecureDataCorp")
cursor.execute("USE SecureDataCorp")
 
fake = Faker(["fr_FR"])  
 
tables = {
    "patients": """
        CREATE TABLE IF NOT EXISTS patients (
            patient_id INT AUTO_INCREMENT PRIMARY KEY,
            nom VARCHAR(50) NOT NULL,
            prenom VARCHAR(50) NOT NULL,
            date_naissance DATE NOT NULL,
            num_secu VARCHAR(15) NOT NULL UNIQUE,
            adresse VARCHAR(100),
            telephone VARCHAR(20)
        )
    """,
    "dossiers_medicaux": """
        CREATE TABLE IF NOT EXISTS dossiers_medicaux (
            dossier_id INT AUTO_INCREMENT PRIMARY KEY,
            patient_id INT NOT NULL,
            date_consultation DATE NOT NULL,
            diagnostic TEXT NOT NULL,
            prescription TEXT,
            FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
        )
    """,
    "analyses_labo": """
        CREATE TABLE IF NOT EXISTS analyses_labo (
            analyse_id INT AUTO_INCREMENT PRIMARY KEY,
            patient_id INT NOT NULL,
            date_analyse DATE NOT NULL,
            type_analyse VARCHAR(50),
            resultats TEXT,
            FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
        )
    """,
    "facturation": """
        CREATE TABLE IF NOT EXISTS facturation (
            facture_id INT AUTO_INCREMENT PRIMARY KEY,
            patient_id INT NOT NULL,
            date_facture DATE NOT NULL,
            montant DECIMAL(10,2),
            mode_paiement VARCHAR(20),
            ref_assurance VARCHAR(30),
            FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
        )
    """
}
 

for table_name, query in tables.items():
    cursor.execute(query)
 
def insert_patients(n):
    """Génère et insère des patients fictifs avec correction du format de la date."""
    for _ in range(n):
        date_naissance = fake.date_of_birth(minimum_age=20, maximum_age=90)
        date_naissance = date_naissance.strftime("%Y-%m-%d")  # ✅ Convertir au bon format

        cursor.execute(
            "INSERT INTO patients (nom, prenom, date_naissance, num_secu, adresse, telephone) VALUES (%s, %s, %s, %s, %s, %s)",
            (fake.last_name(), fake.first_name(), date_naissance, fake.ssn(), fake.address(), fake.phone_number())
        )
    conn.commit()


def insert_dossiers_medicaux(n):
    """Génère et insère des dossiers médicaux fictifs."""
    cursor.execute("SELECT patient_id FROM patients")
    patients_ids = [row[0] for row in cursor.fetchall()]
 
    diagnostics = ["Grippe", "Fracture", "Allergie", "Diabète", "Migraine", "COVID-19", "Asthme", "Infection Urinaire"]
    prescriptions = ["Paracétamol", "Ibuprofène", "Insuline", "Antihistaminique", "Antibiotiques", "Vitamine C", "Rien"]
 
    for _ in range(n):
        cursor.execute(
            "INSERT INTO dossiers_medicaux (patient_id, date_consultation, diagnostic, prescription) VALUES (%s, %s, %s, %s)",
            (random.choice(patients_ids), fake.date_this_decade(), random.choice(diagnostics), random.choice(prescriptions))
        )
    conn.commit()
 
def insert_analyses_labo(n):
    """Génère et insère des analyses de laboratoire fictives."""
    cursor.execute("SELECT patient_id FROM patients")
    patients_ids = [row[0] for row in cursor.fetchall()]
 
    types_analyse = ["Sang", "Urine", "IRM", "Échographie", "Radiographie", "Scanner", "Test PCR"]
    resultats = ["Normal", "Anomalie détectée", "À surveiller", "Résultats en attente", "Urgence"]
 
    for _ in range(n):
        cursor.execute(
            "INSERT INTO analyses_labo (patient_id, date_analyse, type_analyse, resultats) VALUES (%s, %s, %s, %s)",
            (random.choice(patients_ids), fake.date_this_decade(), random.choice(types_analyse), random.choice(resultats))
        )
    conn.commit()
 
def insert_facturation(n):
    """Génère et insère des factures fictives."""
    cursor.execute("SELECT patient_id FROM patients")
    patients_ids = [row[0] for row in cursor.fetchall()]
 
    modes_paiement = ["Carte Bancaire", "Espèces", "Chèque", "Virement"]
    assurances = ["ASSUR-1234", "ASSUR-5678", "ASSUR-9012", "ASSUR-3456", "Mutuelle XYZ"]
 
    for _ in range(n):
        cursor.execute(
            "INSERT INTO facturation (patient_id, date_facture, montant, mode_paiement, ref_assurance) VALUES (%s, %s, %s, %s, %s)",
            (random.choice(patients_ids), fake.date_this_decade(), round(random.uniform(20, 500), 2), random.choice(modes_paiement), random.choice(assurances))
        )
    conn.commit()
 

insert_patients(100)
insert_dossiers_medicaux(100)
insert_analyses_labo(100)
insert_facturation(100)
 
print("✅ 100 lignes de données insérées dans chaque table avec succès !")
 

cursor.close()
conn.close()
