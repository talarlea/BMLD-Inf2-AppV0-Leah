import pandas as pd
import streamlit as st
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# Session State initialisieren
if "history" not in st.session_state:
    st.session_state["history"] = pd.DataFrame(columns=["Zeit", "ECTS", "Durchschnitt", "Bestanden"])

st.set_page_config(page_title="Meine App", page_icon=":material/home:")

data_manager = DataManager(
    fs_protocol='webdav',
    fs_root_folder='bmld_app'
)
login_manager = LoginManager(data_manager)
login_manager.login_register()

if 'data_df' not in st.session_state:
    st.session_state['data_df'] = data_manager.load_user_data(
        'data.csv',
        initial_value=pd.DataFrame(),
    )

pg_home = st.Page("views/home.py", title="Home", icon=":material/home:", default=True)
pg_second = st.Page("views/Did_I_Pass_Calculator.py", title="Did I pass? - Calculator", icon=":material/info:")

pg = st.navigation([pg_home, pg_second])
pg.run()

