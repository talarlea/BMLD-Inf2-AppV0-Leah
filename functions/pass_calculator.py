from datetime import datetime
import pytz

def berechne_durchschnitt(df):
    ges_ects = df["ECTS"].sum()

    if ges_ects == 0:
        return 0, 0

    durchschnitt = (df["ECTS"] * df["Note"]).sum() / ges_ects
    return ges_ects, durchschnitt


def ist_bestanden(durchschnitt, grenze=4.0):
    return durchschnitt >= grenze


def zeige_statistik(df):
    if len(df) == 0:
        return

    beste_note = df["Note"].max()
    schlechteste_note = df["Note"].min()
    anzahl_faecher = len(df)

    st.subheader("Statistik")
    st.write(f"Anzahl Fächer: {anzahl_faecher}")
    st.write(f"Beste Note: {beste_note}")
    st.write(f"Schlechteste Note: {schlechteste_note}")

def download_csv(df):
    csv = df.to_csv(index=False)

    st.download_button(
        label="CSV herunterladen",
        data=csv,
        file_name="noten_ects.csv",
        mime="text/csv"
    )

def validiere_daten(df):
    if df["ECTS"].sum() == 0:
        st.warning("Die ECTS dürfen nicht 0 sein.")
        return False

    if df["Note"].isnull().any():
        st.warning("Bitte alle Noten ausfüllen.")
        return False

    return True
