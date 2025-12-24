import os
from src.audit_logic import load_and_clean_data, run_audit

# Configuration des chemins
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

def main():
    print(f"--- Démarrage de l'audit (Python 3.10.12) ---")
    
    # Création du dossier output s'il n'existe pas
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Dossier créé : {OUTPUT_DIR}")

    try:
        # 1. Chargement et nettoyage
        df_art, df_fam, df_pos = load_and_clean_data(DATA_DIR)
        
        # 2. Analyse
        q1, q2, q3 = run_audit(df_art, df_fam, df_pos)
        
        # 3. Exportation
        q1.to_csv(os.path.join(OUTPUT_DIR, 'q1_arretes_en_stock.csv'), index=False, encoding='utf-8-sig')
        q2.to_csv(os.path.join(OUTPUT_DIR, 'q2_actifs_sans_stock.csv'), index=False, encoding='utf-8-sig')
        q3.to_csv(os.path.join(OUTPUT_DIR, 'q3_familles_hors_referentiel.csv'), index=False, encoding='utf-8-sig')
        
        print("\nRésultats de l'analyse :")
        print(f"Q1 - Articles arrêtés en stock : {len(q1)}")
        print(f"Q2 - Articles actifs hors stock : {len(q2)}")
        print(f"Q3 - Articles famille hors réf (incl. NaN) : {len(q3)}")
        print(f"\nFichiers CSV générés avec succès dans : {OUTPUT_DIR}")

    except Exception as e:
        print(f"Erreur durant l'exécution : {e}")

if __name__ == "__main__":
    main()