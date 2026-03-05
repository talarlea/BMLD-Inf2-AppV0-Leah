import streamlit as st
import pandas as pd

from views.functions_Pass import (
    create_default_dataframe,
    berechne_durchschnitt,
    zeige_ergebnis,
    zeige_status,
    zeige_statistik,
    zeige_diagramm,
    download_csv,
    validiere_daten
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
        zeige_diagramm(df)
        download_csv(df)