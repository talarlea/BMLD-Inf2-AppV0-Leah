import streamlit as st
import pandas as pd
from datetime import datetime

from functions.pass_calculator import (
    berechne_durchschnitt,
    ist_bestanden,
)

# ---------------- FUNCTIONS ---------------- #

def create_default_dataframe():
    return pd.DataFrame({
        "Fach": [""],
        "ECTS": [1.0],
        "Note": [4.00]
    })


def zeige_ergebnis(ects, durchschnitt):
    st.write(f"Gesamte ECTS: {ects}")
    st.metric("Durchschnitt", round(durchschnitt, 2))


def validiere_daten(df):

    if len(df) == 0:
        st.error("Bitte mindestens ein Fach hinzufügen.")
        return False

    if df["ECTS"].isnull().any() or df["Note"].isnull().any():
        st.error("Bitte alle Felder ausfüllen.")
        return False

    if (df["ECTS"] <= 0).any():
        st.error("ECTS müssen größer als 0 sein.")
        return False

    return True


def zeige_status(durchschnitt):
    if ist_bestanden(durchschnitt):
        st.success("Bestanden! Herzlichen Glückwunsch!")
        st.balloons()
    else:
        st.error("Leider nicht bestanden. Versuche es erneut!")


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


@st.dialog("Nicht bestanden")
def exmatrikulation_dialog():
    st.warning("Der Notendurchschnitt liegt unter 4.00.")
    st.write("Was möchtest du tun?")

    col1, col2 = st.columns(2)

    with col1:
        st.link_button(
            "👉 Exmatrikulation hier lang!",
            "https://www.zhaw.ch/storage/lsfm/studium/_formulare-merkblaetter/austritt-merkblatt.pdf"
        )


# ---------------- UI ---------------- #

st.title("Did I pass? - Calculator")

st.write(
    "Der ECTS-Notenrechner ermöglicht es, den persönlichen Notendurchschnitt "
    "einer Modulgruppe zu berechnen. Dazu werden für jedes Fach die erzielte "
    "Note und die entsprechende ECTS-Gewichtung eingetragen. "
    "Aus diesen Angaben wird automatisch der gewichtete Durchschnitt ermittelt."
)

default_data = create_default_dataframe()

# ---------------- FORM ---------------- #

with st.form("ects_form"):
    df = st.data_editor(
        default_data,
        num_rows="dynamic",
        column_config={
            "Note": st.column_config.NumberColumn(
                "Note",
                min_value=1.0,
                max_value=6.0,
                step=0.01
            ),
            "ECTS": st.column_config.NumberColumn(
                "ECTS",
                min_value=0.5,
                max_value=30.0,
                step=0.5
            )
        }
    )

    submitted = st.form_submit_button("Berechnen")

# ---------------- LOGIC ---------------- #

if submitted:
    if validiere_daten(df):

        ges_ects, durchschnitt = berechne_durchschnitt(df)

        # --- HISTORY SPEICHERN ---
        neuer_eintrag = pd.DataFrame([{
            "Zeit": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "ECTS": ges_ects,
            "Durchschnitt": round(durchschnitt, 2),
            "Bestanden": ist_bestanden(durchschnitt)
        }])

        st.session_state["data_df"] = pd.concat(
            [st.session_state["data_df"], neuer_eintrag],
            ignore_index=True
        )

        zeige_ergebnis(ges_ects, durchschnitt)
        zeige_status(durchschnitt)
        zeige_statistik(df)
        download_csv(df)

        if durchschnitt < 4.0:
            exmatrikulation_dialog()

# ---------------- HISTORY ---------------- #

if not st.session_state["data_df"].empty:

    st.divider()
    st.subheader("Berechnungshistorie")

    st.dataframe(
        st.session_state["data_df"],
        use_container_width=True
    )

    if st.button("Historie löschen"):
        st.session_state["data_df"] = pd.DataFrame()
        st.rerun()