import streamlit as st
import os.path
import pandas as pd
import requests
import os
import errno
import os.path
#from General import Principal
#from Epocas import PrincipalEp
#import Comparaciones as comp



# Configuración inicial del módulo
st.set_page_config(
    page_title = 'Reporte general de las estaciones',
    page_icon = os.path.dirname(os.path.abspath(__file__))+'Imagenes/Logo.png',
    layout = 'wide',
    initial_sidebar_state='expanded',
    menu_items={
        'About': 'El sistema de generación de reportes y gráficos de las estaciones fue desarrollado por **Cristian David Vargas Avellaneda** con la colaboración del grupo de sismología y el grupo de sistemas. Este aplicativo tiene como objetivo ayudar a los usuarios a comprender las funcionalidades para la gestión de la información de las estaciones de la red de monitoreo dentro del Sistema de Información de Instrumentación de Geoamenazas (SIIGeo). Además, el aplicativo es capaz de generar gráficos y reportes basados en los filtros seleccionados por el usuario, también puede verificar si existen inconsistencias en los datos que están siendo evaluados. **Si encuentra un error la persona que quedara acargo del código sera Angel Daniel Agudelo (adagudelo@sgc.gov.co)**'
    }
)

##cabiar tema?

#dark = '''
#<style>
#    .stApp {
#    background-color: black;
#    }
#</style>
#'''

#light = '''
#<style>
#    .stApp {primary-color: white;
#    background-color: white;
#    }
#</style>'''

#st.markdown(light, unsafe_allow_html=True)

#leer librerias
@st.cache_resource
def libr_rv():
    Principal = st.session_state["Principal"]
    PrincipalEp = st.session_state["PrincipalEp"] 
    comp = st.session_state["comp"] 
    
    return Principal, PrincipalEp, comp

Principal, PrincipalEp, comp = libr_rv()



opt_modulos = st.sidebar.selectbox("Modulos",["Reporte general","Reporte epoca","Verificador"])

# Crea la carpeta en la que se guardaran todos los reportes que genere el aplicativo
#ruta_actual = os.getcwd()
try:
    os.mkdir(os.path.dirname(os.path.abspath(__file__))+'/Aplicativo/Reportes')
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
try:
    os.mkdir(os.path.dirname(os.path.abspath(__file__))+'/Aplicativo/Base')
except OSError as e:
    if e.errno != errno.EEXIST:
        raise



if opt_modulos == "Reporte general":

    st.title('Reporte general de las estaciones en SIIGEO', help='Este módulo trabaja con el reporte general de las estaciones en formato ".xlsx", este contiene toda la información de las estaciones de la red de monitoreo')
    ruta = os.path.dirname(os.path.abspath(__file__))+'/Aplicativo/Base/General.xlsx'

    if os.path.exists(ruta) == False:
    #if 'general' not in st.session_state:
        url = requests.get('https://siigeo.sgc.gov.co/stations/staAllExcelView', verify=False)
        open(ruta, 'wb').write(url.content)
        #st.session_state['general'] = True
    
    
    

    with st.container():
        if ruta is not None:
            df = pd.read_excel(io = ruta)
            df = df.sort_values('IDENTIFICADOR')

            principal = Principal(df)
            st.subheader('Datos cargados:')
            principal.visualizar()

            if st.button("Actualizar del SIIGEO", type="primary", key="b_act_gen"):
                url = requests.get('https://siigeo.sgc.gov.co/stations/staAllExcelView', verify=False)
                open(ruta, 'wb').write(url.content)
            st.write(" ")
            st.write("_________")



            # Se crean las 4 secciones del módulo
            tab1, tab2, tab3, tab4 = st.tabs(['Reporte general con filtros', 'Estaciones instaladas por año', 'Estaciones retiradas por año', 'Acumulado de estaciones por año'])

            # Sección "Reporte general con filtros"
            with tab1:
                principal.seccion_uno()
                #principal.mapa()
            
            # Sección "Estaciones instaladas por año"
            with tab2:
                principal.seccion_dos()
            
            # Sección "Estaciones instaladas por año"
            with tab3:
                principal.seccion_tres()
            
            # Sección "Acumulado de estaciones por año"
            with tab4:
                principal.seccion_cuatro()

if opt_modulos == "Reporte epoca":

    st.title('Reporte épocas de las estaciones en SIIGEO', help='Este módulo trabaja con el reporte épocas de las estaciones en formato ".xlsx", este contiene toda la información de las épocas o el histórico de la instrumentación de las estaciones de la red de monitoreo.')
    ruta = os.path.dirname(os.path.abspath(__file__))+'/Aplicativo/Base/Epocas.xlsx'

    if os.path.exists(ruta) == False:
    #if 'epocas' not in st.session_state:
        url = requests.get('https://siigeo.sgc.gov.co/stations/staExcelAllCodLocation', verify=False)
        open(ruta, 'wb').write(url.content)
        #st.session_state['epocas'] = True

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

            principal = PrincipalEp(df)
            st.subheader('Datos cargados:')
            principal.visualizar()

            if st.button("Actualizar del SIIGEO", type="primary", key="b_act_epoc"):
                url = requests.get('https://siigeo.sgc.gov.co/stations/staExcelAllCodLocation', verify=False)
                open(ruta, 'wb').write(url.content)
            st.write(" ")
            st.write("_________")

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

if opt_modulos == "Verificador":

    with st.container():
        st.title('Verificador de estaciones en SIIGEO', help='Este módulo del aplicativo trabajara con los reportes general, NSCL y documentos en formato .xlsx que se puede descargar desde SIIGEO. Cada uno de los reportes podra ser verficado en la sección que le corresponda.')
        
        tab1, tab2, tab3 = st.tabs(['Reporte general','Reporte NSCL','Revisión de documentos'])

        with tab1:
            with st.container():
                st.subheader('Reporte general', help='Esta sección trabaja con el reporte general de las estaciones en formato ".xlsx", este contiene toda la información de las estaciones de la red de monitoreo.')

                ruta_uno = os.path.dirname(os.path.abspath(__file__))+'/Aplicativo/Base/General.xlsx'
                if os.path.exists(ruta_uno) == False:
                #if 'verificador_uno' not in st.session_state:
                    url_uno = requests.get('https://siigeo.sgc.gov.co/stations/staAllExcelView', verify=False)
                    open(ruta_uno, 'wb').write(url_uno.content)
                    #st.session_state['verificador_uno'] = True

                if st.button("Actualizar del SIIGEO", type="primary", key="b_act_1"):
                    url_uno = requests.get('https://siigeo.sgc.gov.co/stations/staAllExcelView', verify=False)
                    open(ruta_uno, 'wb').write(url_uno.content)
                st.write(" ")
                st.write("_________")
                if ruta_uno is not None:

                    df_uno = pd.read_excel(
                        io=ruta_uno,
                        engine='openpyxl'
                    )

                    comp.verificar_uno(df_uno)
        
        with tab2:
            with st.container():
                st.subheader('Reporte NSCL', help='Esta sección trabaja con el reporte NSCL de las estaciones en formato ".xlsx", este contiene toda la instrumentación de las estaciones de la red de monitoreo.')

                ruta_dos = os.path.dirname(os.path.abspath(__file__))+'/Aplicativo/Base/NSCL.xlsx'
                if os.path.exists(ruta_dos) == False:
                #if 'verificador_dos' not in st.session_state:
                    url_dos = requests.get('https://siigeo.sgc.gov.co/stations/staReportCodLocInstrumen', verify=False)
                    open(ruta_dos, 'wb').write(url_dos.content)
                    #st.session_state['verificador_dos'] = True

                if st.button("Actualizar del SIIGEO", type="primary", key="b_act_2"):
                    url_dos = requests.get('https://siigeo.sgc.gov.co/stations/staReportCodLocInstrumen', verify=False)
                    open(ruta_dos, 'wb').write(url_dos.content)
                st.write(" ")
                st.write("_________")
                    
                if ruta_dos is not None:

                    df_dos = pd.read_excel(
                        io=ruta_dos,
                        engine='openpyxl'
                    )

                    comp.verificar_dos(df_dos)
        
        with tab3:
            with st.container():
                st.subheader('Revisión de documentos', help='Esta sección trabaja con el reporte documentos de las estaciones en formato ".xlsx", este contiene la informacion de los documentos asociados a las estaciones de la red de monitoreo, ejemplo: Dataless, Historico de la estacion, etc.')

                # Carga el archivo Excel Documentos
                ruta_tres = os.path.dirname(os.path.abspath(__file__))+'/Aplicativo/Base/Documentos.xlsx'
                if os.path.exists(ruta_tres) == False:
                #if 'verificador_tres' not in st.session_state:
                    url_tres = requests.get('https://siigeo.sgc.gov.co/stations/stationExcelFile', verify=False)
                    open(ruta_tres, 'wb').write(url_tres.content)
                    #st.session_state['verificador_tres'] = True

                if st.button("Actualizar del SIIGEO", type="primary", key="b_act_3"):
                    url_tres = requests.get('https://siigeo.sgc.gov.co/stations/stationExcelFile', verify=False)
                    open(ruta_tres, 'wb').write(url_tres.content)
                st.write(" ")
                st.write("_________")

                if ruta_tres is not None:

                    df_tres = pd.read_excel(
                        io=ruta_tres,
                        engine='openpyxl'
                    )

                    comp.verificar_tres(df_tres)
st.sidebar.write(" ")
st.sidebar.write("______")
st.sidebar.write(" ")
st.sidebar.write(" ")
st.sidebar.write(" ")
with st.sidebar.expander("**Sobre la app**"):
        st.write("""
                **Verificador de estaciones en SIIGEO**\n 
                """)
        st.write(""" 
                El sistema de generación de reportes y gráficos de las estaciones fue desarrollado por Cristian David Vargas Avellaneda 
                con la colaboración del grupo de sismología y el grupo de sistemas [Repositorio Github](https://github.com/CristianDavid313/Aplicativo). Este aplicativo tiene como objetivo ayudar a los usuarios 
                a comprender las funcionalidades para la gestión de la información de las estaciones de la red de monitoreo dentro del Sistema 
                de Información de Instrumentación de Geoamenazas (SIIGeo). Además, el aplicativo es capaz de generar gráficos y reportes basados 
                en los filtros seleccionados por el usuario, también puede verificar si existen inconsistencias en los datos que están siendo 
                evaluados. 
                
      """)
        st.write("__________")
        st.write("**Si encuentra un error por favor comunicarse con  Angel Daniel Agudelo adagudelo@sgc.gov.co**")
        st.write("**Actualización, enero de 2024**")
