import streamlit as st
import pandas as pd
import requests
import os
import errno
from Comparaciones import *

# Configuración inicial del módulo
st.set_page_config(
    page_title = 'Verificador',
    page_icon = 'Imagenes/Logo.png',
    layout = 'wide',
    initial_sidebar_state = 'expanded'
)

# Crea la carpeta en la que se guardaran todos los reportes que genere el aplicativo
ruta_actual = os.getcwd()
try:
    os.mkdir('Reportes')
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
try:
    os.mkdir('Base')
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
    
with st.container():
    st.title('Verificador', help='Este módulo del aplicativo trabajara con los reportes general, NSCL y documentos en formato .xlsx que se puede descargar desde SIIGEO. Cada uno de los reportes podra ser verficado en la sección que le corresponda.')
    
    tab1, tab2, tab3 = st.tabs(['Reporte general','Reporte NSCL','Revisión de documentos'])

    with tab1:
        with st.container():
            st.subheader('Reporte general', help='Esta sección trabaja con el reporte general de las estaciones en formato ".xlsx", este contiene toda la información de las estaciones de la red de monitoreo.')

            ruta_uno = 'Base/General.xlsx'
            if 'verificador_uno' not in st.session_state:
                url_uno = requests.get('https://siigeo.sgc.gov.co/stations/staAllExcelView', verify=False)
                open(ruta_uno, 'wb').write(url_uno.content)
                st.session_state['verificador_uno'] = True

            if ruta_uno is not None:

                df_uno = pd.read_excel(
                    io=ruta_uno,
                    engine='openpyxl'
                )

                verificar_uno(df_uno)
    
    with tab2:
        with st.container():
            st.subheader('Reporte NSCL', help='Esta sección trabaja con el reporte NSCL de las estaciones en formato ".xlsx", este contiene toda la instrumentación de las estaciones de la red de monitoreo.')

            ruta_dos = 'Base/NSCL.xlsx'
            if 'verificador_dos' not in st.session_state:
                url_dos = requests.get('https://siigeo.sgc.gov.co/stations/staReportCodLocInstrumen', verify=False)
                open(ruta_dos, 'wb').write(url_dos.content)
                st.session_state['verificador_dos'] = True
                
            if ruta_dos is not None:

                df_dos = pd.read_excel(
                    io=ruta_dos,
                    engine='openpyxl'
                )

                verificar_dos(df_dos)
    
    with tab3:
        with st.container():
            st.subheader('Revisión de documentos', help='Esta sección trabaja con el reporte documentos de las estaciones en formato ".xlsx", este contiene la informacion de los documentos asociados a las estaciones de la red de monitoreo, ejemplo: Dataless, Historico de la estacion, etc.')

            # Carga el archivo Excel Documentos
            ruta_tres = 'Base/Documentos.xlsx'
            if 'verificador_tres' not in st.session_state:
                url_tres = requests.get('https://siigeo.sgc.gov.co/stations/stationExcelFile', verify=False)
                open(ruta_tres, 'wb').write(url_tres.content)
                st.session_state['verificador_tres'] = True

            if ruta_tres is not None:

                df_tres = pd.read_excel(
                    io=ruta_tres,
                    engine='openpyxl'
                )

                verificar_tres(df_tres)