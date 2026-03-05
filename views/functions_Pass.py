import streamlit as st
import pandas as pd


def create_default_dataframe():
    """Erstellt die Starttabelle für die Eingabe."""
    return pd.DataFrame({
        "Fach": [""],
        "ECTS": [1.0],
        "Note": [4.00]
    })

def berechne_durchschnitt(df):
    """Berechnet gesamte ECTS und gewichteten Notendurchschnitt."""
    ges_ects = df["ECTS"].sum()

    if ges_ects == 0:
        return 0, 0

    durchschnitt = (df["ECTS"] * df["Note"]).sum() / ges_ects
    return ges_ects, durchschnitt


def ist_bestanden(durchschnitt, grenze=4.0):
    """Prüft ob bestanden wurde."""
    return durchschnitt >= grenze


def zeige_ergebnis(ects, durchschnitt):
    """Zeigt die wichtigsten Kennzahlen."""
    st.write(f"Gesamte ECTS: {ects}")
    st.metric("Durchschnitt", round(durchschnitt, 2))


def zeige_status(durchschnitt):
    """Zeigt bestanden / nicht bestanden."""
    if ist_bestanden(durchschnitt):
        st.success("Bestanden! Herzlichen Glückwunsch!")
        st.balloons()
    else:
        st.error("Leider nicht bestanden. Versuche es erneut!")

def zeige_statistik(df):
    """Zeigt zusätzliche Statistiken."""
    if len(df) == 0:
        return

    beste_note = df["Note"].min()
    schlechteste_note = df["Note"].max()
    anzahl_faecher = len(df)

    st.subheader("Statistik")
    st.write(f"Anzahl Fächer: {anzahl_faecher}")
    st.write(f"Beste Note: {beste_note}")
    st.write(f"Schlechteste Note: {schlechteste_note}")

def zeige_diagramm(df):
    """Visualisiert die Noten."""
    if len(df) == 0:
        return

    st.subheader("Notenübersicht")

    if "Fach" in df.columns:
        chart_df = df.set_index("Fach")
    else:
        chart_df = df

    st.bar_chart(chart_df["Note"])

def download_csv(df):
    """Ermöglicht Download der Tabelle als CSV."""
    csv = df.to_csv(index=False)

    st.download_button(
        label="CSV herunterladen",
        data=csv,
        file_name="noten_ects.csv",
        mime="text/csv"
    )

def validiere_daten(df):
    """Überprüft Eingabedaten auf Fehler."""
    if df["ECTS"].sum() == 0:
        st.warning("Die ECTS dürfen nicht 0 sein.")
        return False

    if df["Note"].isnull().any():
        st.warning("Bitte alle Noten ausfüllen.")
        return False

    return True