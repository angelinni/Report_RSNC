![SGC](images/sgc_logo.png)<!-- .element width="700"-->

# Reportes RSNC
Reportes RSNC es una aplicación web que nos ayudará a generar diferentes tipos de reportes, boletines o informes necesarios para el monitoreo sismologico en la RSNC.

Cuenta con 3 aplicaciones diferentes con las siguientes funciones:

# Reporte Calidad Estacion Report_CalEst

La aplicación genera graficas dinamicas de consultas por fechas y genera informes semestrales y mensuales en formato docx 
con la información de funcionamiento y calidad de cada estación en tiempo real, mostrando por estación datos de disponibilidad, gaps, overlaps, offset, picos y ppsd. Además, 
el sismólogo encargado puede ingresar sus observaciones del estado de cada estación. Esta apliación reune desarrollos de Miguel Lizarazo en la toma de datos de estaciones y Monica Acosta con SIIGEO.

Las opciónes de consulta y reporte son las siguientes:

Consulta Por fecha
Informe semestral
Informe mensual
Estado Actual

# Ficha de evento destacado

La aplicación genera una ficha en formato PDF con toda la informaciòn relevante de un evento destacado como lo son:

Información General
Aceleración
Intensidad Instrumental
Intensidad percibida
Reporte de daños
Efectos de la naturaleza
Sismicidad historica
La informaciòn hasta Intensidad percibida se tomará directamente de la página sgc/sismos con solo ingresar el ID del evento, el resto es necesario ingresarla manualmente.

# erificador de Estaciones en SIIGEO

El sistema de generación de reportes y gráficos de las estaciones tiene como objetivo ayudar a los usuarios a comprender las funcionalidades para la gestión de la información de las estaciones de la red de monitoreo dentro del Sistema de Información de Instrumentación de Geoamenazas (SIIGeo). Además, el aplicativo es capaz de generar gráficos y reportes basados en los filtros seleccionados por el usuario, también puede verificar si existen inconsistencias en los datos que están siendo evaluados, cuenta con tres modulos para consulta y verificación:

Reporte general
Reporte epoca
Verificador

## 1. Instalacio linux

### - Python
Python Versión 3.10 en adelante. 
```bash
sudo apt-get install python3.10
```

Tener virtualenv en python.
```bash
python3.7 -m pip install virtualenv
```

#### Instalación con pip 
```bash
python3.10 -m virtualenv env_rep
source env_rep/bin/activate
pip install -r requirements.txt
```

## Autor

- Angel Agudelo adagudelo@sgc.gov.co
