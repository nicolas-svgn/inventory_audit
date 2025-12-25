# src/audit_logic.py
import pandas as pd
import os

def load_and_clean_data(data_dir):
    # Chemins vers les fichiers
    path_art = os.path.join(data_dir, 'ARTOKM.csv')
    path_fam = os.path.join(data_dir, 'Famille.csv')
    path_pos = os.path.join(data_dir, 'PositionOKM.csv')

    if not os.path.exists(path_art):
        raise FileNotFoundError(f"ERREUR : Le fichier {path_art} est introuvable.")
    if not os.path.exists(path_fam):
        raise FileNotFoundError(f"ERREUR : Le fichier {path_fam} est introuvable.")
    if not os.path.exists(path_pos):
        raise FileNotFoundError(f"ERREUR : Le fichier {path_pos} est introuvable.")
    

    try:
        # Chargement
        df_art = pd.read_csv(path_art, sep=',', encoding='utf-8-sig')
        df_fam = pd.read_csv(path_fam, sep=',', encoding='utf-8-sig')
        df_pos = pd.read_csv(path_pos, sep=',', encoding='utf-8-sig')
    except Exception as e:
        raise ValueError(f"Erreur de lecture du fichier : {e}")

    # --- NETTOYAGE CRITIQUE ---

    # 1. On force les colonnes de liaison en STRING immédiatement
    # 2. On applique strip() pour enlever les espaces
    
    df_pos['Code article'] = df_pos['Code article'].astype(str).str.strip()
    df_art['CODE ARTICLE'] = df_art['CODE ARTICLE'].astype(str).str.strip()

    # 4. Nettoyage des familles (toujours en String)
    df_art['FAMILLE'] = df_art['FAMILLE'].astype(str).str.strip()
    df_fam['famille'] = df_fam['famille'].astype(str).str.strip()

    print(f"   -> ARTOKM chargé : {df_art.shape[0]} lignes")
    print(f"   -> Famille chargé : {df_fam.shape[0]} lignes")
    print(f"   -> Position chargé : {df_pos.shape[0]} lignes")

    return df_art, df_fam, df_pos

def run_audit(df_art, df_fam, df_pos):
    # Jointure pour Q1 et Q2
    df_merged = pd.merge(df_pos, df_art, left_on='Code article', right_on='CODE ARTICLE', how='inner')
    
    # Q1: Arrêtés (1) et Stock > 0
    q1 = df_merged[(df_merged['ARRETE OUI = 1\nNON = 2'] == 1) & (df_merged['en stock'] > 0)]
    
    # Q2: Actifs (2) et Stock <= 0
    q2 = df_merged[(df_merged['ARRETE OUI = 1\nNON = 2'] == 2) & (df_merged['en stock'] <= 0)]
    
    # Q3: Hors référentiel (on utilise une jointure LEFT pour voir les NaN)
    df_q3 = pd.merge(df_pos, df_art[['CODE ARTICLE', 'FAMILLE']], left_on='Code article', right_on='CODE ARTICLE', how='left')
    familles_valides = df_fam['famille'].unique()
    q3 = df_q3[~df_q3['FAMILLE'].isin(familles_valides)]
    
    return q1, q2, q3