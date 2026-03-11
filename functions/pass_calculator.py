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
