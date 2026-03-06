import streamlit as st
import pandas as pd

from views.functions_Pass import (
    create_default_dataframe,
    berechne_durchschnitt,
    zeige_ergebnis,
    zeige_status,
    zeige_statistik,
    download_csv,
    validiere_daten
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

st.title("Did I pass? - Calculator")

st.write(
    "Der ECTS-Notenrechner ermöglicht es, den persönlichen Notendurchschnitt "
    "einer Modulgruppe zu berechnen. Dazu werden für jedes Fach die erzielte "
    "Note und die entsprechende ECTS-Gewichtung eingetragen. "
    "Aus diesen Angaben wird automatisch der gewichtete Durchschnitt ermittelt."
)

default_data = create_default_dataframe()

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


if submitted:
    if validiere_daten(df):

        ges_ects, durchschnitt = berechne_durchschnitt(df)

        zeige_ergebnis(ges_ects, durchschnitt)
        zeige_status(durchschnitt)
        zeige_statistik(df)
        download_csv(df)

        if durchschnitt < 4.0:
            exmatrikulation_dialog()