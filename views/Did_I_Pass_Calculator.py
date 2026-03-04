import streamlit as st
import pandas as pd

st.title("Did I pass? - Calculator")

st.write("Der ECTS‑Notenrechner ermöglicht es, den persönlichen Notendurchschnitt einer Modulgruppe zu berechnen. " \
"Dazu werden für jedes Fach die erzielte Note und die entsprechende ECTS‑Gewichtung eingetragen." \
"Aus diesen Angaben wird automatisch der gewichtete Durchschnitt ermittelt, sodass auf einen Blick ersichtlich ist, ob die Modulgruppe bestanden wurde oder nicht.")


default_data = pd.DataFrame({
    "Fach": [""],
    "ECTS": [1.0],
    "Note": [4.00]
})

with st.form("ects_form"):
    df = st.data_editor(
        default_data,
        num_rows="dynamic",
        column_config={
            "Note": st.column_config.NumberColumn("Note", min_value=1.0, max_value=6.0, step=0.01),
            "ECTS": st.column_config.NumberColumn("ECTS", min_value=0.5, max_value=30.0, step=0.5)
        }
    )
    submitted = st.form_submit_button("Berechnen")

if submitted:
    if len(df) > 0:
        ges_ects = df["ECTS"].sum()
        durchschnitt = (df["ECTS"] * df["Note"]).sum() / ges_ects
        st.metric("Durchschnitt", round(durchschnitt, 2))
    
        if durchschnitt > 4:
         st.balloons()
        else:
            st.warning("Leider nicht bestanden. Versuche es erneut!")   