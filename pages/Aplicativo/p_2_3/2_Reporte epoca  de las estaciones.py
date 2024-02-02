import streamlit as st
import pandas as pd
import requests
import os
import errno
from Epocas import Principal

# Configuracion de la pagina
st.set_page_config(
    page_title='Reporte epoca de las estaciones',
    page_icon = 'Imagenes/Logo.png',
    layout = 'wide',
    initial_sidebar_state='expanded'
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
    
st.title('Reporte épocas de las estaciones', help='Este módulo trabaja con el reporte épocas de las estaciones en formato ".xlsx", este contiene toda la información de las épocas o el histórico de la instrumentación de las estaciones de la red de monitoreo.')
ruta = 'Base/Epocas.xlsx'

if 'epocas' not in st.session_state:
    url = requests.get('https://siigeo.sgc.gov.co/stations/staExcelAllCodLocation', verify=False)
    open(ruta, 'wb').write(url.content)
    st.session_state['epocas'] = True

with st.container():
    if ruta is not None:
        df = pd.read_excel(io = ruta)
        df = df.sort_values('ID ESTACION')

        df['CODIGO LOCALIZACION'] = df['CODIGO LOCALIZACION'].replace(
            {
                0: '00',
                10: '10',
                11: '11',
                20: '20',
                30: '30',
                40: '40'
            }
        )

        principal = Principal(df)
        st.subheader('Datos cargados:')
        principal.visualizar()

        # Se crean las 3 secciones del módulo
        tab1, tab2, tab3 = st.tabs(['Reporte épocas con filtros', 'Reporte tipo de adquisición', 'Reporte cambio tipo adquisición'])

        # Sección "Reporte épocas con filtros"
        with tab1:
            principal.seccion_uno()
        
        # Sección "Reporte tipo de adquisición"
        with tab2:
            principal.seccion_dos()
        
        # Sección "Reporte cambio tipo adquisición"
        with tab3:
            principal.seccion_tres()