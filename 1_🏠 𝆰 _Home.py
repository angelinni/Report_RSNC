import streamlit as st
from PIL import Image


#Report Event
import pages.Report_Event.mkPDF as mkPDF
import pages.Report_Event.web_inf as web_inf
import pages.Report_Event.plot_info as plot_info

st.session_state["mkPDF"] = mkPDF
st.session_state["web_inf"] = web_inf
st.session_state["plot_info"] = plot_info

#Reporte Calidad de estaciones
import pages.Report_CalEst.create_doc as create_doc
import pages.Report_CalEst.plot_CalEst as plot_CalEst

st.session_state["create_doc"] = create_doc
st.session_state["plot_CalEst"] = plot_CalEst

#Aplicacion
from pages.Aplicativo.General import Principal
from pages.Aplicativo.Epocas import PrincipalEp
import pages.Aplicativo.Comparaciones as comp

st.session_state["Principal"] = Principal
st.session_state["PrincipalEp"] = PrincipalEp
st.session_state["comp"] = comp






st.set_page_config(
    page_title="REPORTES RSNC",
    page_icon="〰️",
)

st.write("# Bienvenido a Reportes RSNC!")

image = Image.open('pages/Report_Event/Simbolo_SGC_Blanco.png')
st.sidebar.image(image)
st.markdown(
    """
    Reportes RSNC es una aplicación web que nos ayudará a generar diferentes tipos de reportes, boletines o informes necesarios para el monitoreo sismologico en la RSNC.
    
    Se cuenta con 3 aplicaciones diferentes con las siguientes funciones:

    ### 📇 Ficha de evento destacado

    La aplicación genera una ficha en formato PDF con toda la informaciòn relevante de un evento destacado como lo son:

    - **Información General**
    - **Aceleración**
    - **Intensidad Instrumental**
    - **Intensidad percibida**
    - **Reporte de daños**
    - **Efectos de la naturaleza**
    - **Sismicidad historica**

    La informaciòn hasta Intensidad percibida se tomará directamente de la página [sgc/sismos](https://www.sgc.gov.co/sismos) con solo ingresar el ID del evento, el resto es necesario ingresarla manualmente.


    ### 📡 Calidad de Estaciones

    La aplicación muestra consultas por fechas y genera informes semestrales y mensuales en formato docx 
    con la información de funcionamiento y calidad de cada estación en tiempo real, mostrando por estación datos de disponibilidad, gaps, overlaps, 
    offset, picos y ppsd. Además, el sismólogo y electronico encargado puede ingresar sus observaciones del estado actual de cada estación.

    Las opciónes de consulta y reporte son las siguientes:

    - **Consulta Por fecha**
    - **Informe semestral**
    - **Informe mensual**
    - **Estado Actual**

    ### ✅  Verificador de Estaciones en SIIGEO

    El sistema de generación de reportes y gráficos de las estaciones tiene como objetivo ayudar a los usuarios a comprender las 
    funcionalidades para la gestión de la información de las estaciones de la red de monitoreo dentro del Sistema de Información de Instrumentación 
    de Geoamenazas (SIIGeo). Además, el aplicativo es capaz de generar gráficos y reportes basados en los filtros seleccionados por el usuario, 
    también puede verificar si existen inconsistencias en los datos que están siendo evaluados, cuenta con tres modulos para consulta y verificación:

    - **Reporte general**
    - **Reporte epoca**
    - **Verificador**



    
    
"""
)
