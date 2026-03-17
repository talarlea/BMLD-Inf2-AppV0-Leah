from datetime import datetime
import pytz

def berechne_durchschnitt(df):
    # Schutz bei ungültigen Daten
    if "ETCS" not in df.columns or "Note" not in df.columns:
        raise ValueError("DataFrame benötigt Spalten 'ECTS' und 'Noten'.")
    
    df = df.dropna(subset=["ECTS", "Note"])  # Entferne Zeilen mit fehlenden Werten

    ges_ects = df["ECTS"].sum()
    if ges_ects <= 0:
        return {
            "Zeit": get_timestamp(),
            "ECTS": 0,
            "Durchschnitt": 0,
            "Bestanden": False
        }

def ist_bestanden(durchschnitt, grenze=4.0):
    return durchschnitt >= grenze

def get_timestamp():
    tz = pytz.timezone('Europe/Zurich')
    return datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
