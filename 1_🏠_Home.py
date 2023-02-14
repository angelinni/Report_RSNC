import streamlit as st
from PIL import Image
import pages.Report_Event.mkPDF as mkPDF
import pages.Report_Event.web_inf as web_inf
import pages.Report_Event.plot_info as plot_info




st.set_page_config(
    page_title="REPORTES RSNC",
    page_icon="〰️",
)



st.session_state["mkPDF"] = mkPDF
st.session_state["web_inf"] = web_inf
st.session_state["plot_info"] = plot_info
st.write("# Bienvenido a Reportes RSNC!")


image = Image.open('pages/Report_Event/Simbolo_SGC_Blanco.png')
st.sidebar.image(image)
st.markdown(
    """
    Reportes RSNC es una aplicación web que nos ayudará a generar diferentes tipos de reportes, boletines o informes necesarios para el monitoreo sismologico en la RSNC.
    
    Se cuenta con __ aplicaciones diferentes con las siguientes funciones:

    ### 〰️ Report Event

    La aplicación genera una ficha en formato PDF con toda la informaciòn relevante de un evento destacado como lo son:

    - **Información General**
    - **Aceleración**
    - **Intensidad Instrumental**
    - **Intensidad percibida**
    - **Reporte de daños**
    - **Efectos de la naturaleza**
    - **Sismicidad historica**

    La informaciòn hasta Intensidad percibida se tomará directamente de la página [sgc/sismos](https://www.sgc.gov.co/sismos) con solo ingresar el ID del evento, el resto es necesario ingresarla manualmente.


    ### Calidad de Estaciones

    
    
"""
)
