import streamlit as st
from reportlab.lib.pagesizes import A4 #A4 215x315
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm, cm
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor
from reportlab.lib import colors 
from reportlab.platypus import Image, Paragraph, Table
from reportlab.platypus.tables import Table
#from reportlab.plattypus import SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY,  TA_LEFT
#from tkinter.ttk import Style
#import PDF_Images as PDF_I
import json
import os
from sympy import *
#import perceived_intensity as pi


mesesDic = {
    "01":'enero',
    "02":'febrero',
    "03":'marzo',
    "04":'abril',
    "05":'mayo',
    "06":'junio',
    "07":'julio',
    "08":'agosto',
    "09":'septiembre',
    "10":'octubre',
    "11":'noviembre',
    "12":'diciembre'}
color_int = {
    "1":"#e0dcf4",
    "2":"#e0dcf4",
    "3":"#a0d4fc",
    "4":"#08fcfc",
    "5":"#00ff00",
    "6":"#ffff00",
    "7":"#ffaa00",
    "8":"#ff0000"
}

opt_map_ip = {
    "1":"#e0dcf4",
    "2":"#e0dcf4"
}
EMS_98 ={
    "1":"No sentido.",
    "2":"Sentido por muy pocas personas en reposo.",
    "3":"Sentido por pocas personas. Balanceo de objetos colgantes.",
    "4":"Sentido por muchas personas en el interior de edificaciones y por pocas en el exterior. Las ventanas, puertas y platos vibran.",
    "5":" Algunas personas se asustan y corren a la calle. Objetos pequeños se desplazan. Vaivén de puertas o ventanas. Leves grietas en casos aislados.",
    "6":"Algunas personas pierden el equilibrio. Algunos objetos caen. Muchas edificaciones presentan daños leves. ",
    "7":"Los muebles pesados se desplazan. Muchos edificios presentan grietas y caída de revestimiento de los muros.",
    "8":"Muchas personas tienen dificultad para mantenerse de pie. Caen objetos pesados. Las estructuras antiguas y débiles pueden colapsar.",
    "9":"Pánico general. Muchas construcciones débiles colapsan. Incluso los edificios ordinarios bien construidos muestran daños serios: fallas graves en los muros y fallas estructurales parciales.",
    "10":"Muchos edificios ordinarios bien construidos colapsan. ",
    "11":"La mayoría de los edificios ordinarios bien construidos colapsan, incluso algunos con buen diseño sismorresistente son destruidos.",
    "12":"Casi todos los edificios son destruidos."
}





width, height = A4

def mkPDF_report(ID_event):
    canv = canvas.Canvas("Reporte_Sismo_Destacado.pdf", pagesize = A4)     #A4=210x297 mm
    folder="Events/"+ID_event

    def background(ID_event_PDF):
        # Fondo superior recurrente de las paginas
        canv.setFont('Helvetica', 13)
        canv.setFillColor(HexColor("#000000"))
        canv.drawString(85 * mm, 280 * mm, "REPORTE SISMO DESTACADO" )

        with open(folder+"/Data/"+f"inf_general_{ID_event_PDF}.json","r") as json_file: 
            results_IG = json.load(json_file)
        local_date = results_IG[0]["inf_general"][1] 
        location_ev = results_IG[0]["inf_general"][6] 
        
        # Fecha del sismo
        canv.setFont('Helvetica', 9)
        canv.setFillColor(HexColor("#000000"))
        canv.drawString(100 * mm, 275 * mm, "Sismo "+local_date[8:10]+" de "+mesesDic[local_date[5:7]]+" de "+local_date[0:4])
    
        #ID del evento
        canv.setFont('Helvetica', 9)
        canv.setFillColor(HexColor("#000000"))
        canv.drawString(100 * mm, 270 * mm,"ID del Evento: "+ ID_event_PDF)
        
        # Region
        canv.setFont('Helvetica', 9)
        canv.setFillColor(HexColor("#000000"))
        canv.drawString(100 * mm, 265 * mm,local_date[11:19]+" "+location_ev)

        #logo SGC
        logo = ImageReader("PDF_Images/Simbolo_SGC_Color.png")
        canv.drawImage(logo, 10*mm, 250*mm,width = 60*mm, preserveAspectRatio=True)
        
        #Baner inferior 
        baner= ImageReader("PDF_Images/Banner_inferior.png")
        canv.drawImage(baner, 5*mm, -25*mm,width = 210*mm, preserveAspectRatio=True)
    
    #Estilo parrrafos 
    normal_left = ParagraphStyle(name='Normal',alignment=TA_LEFT, fontSize=8)
    normal_justifiy = ParagraphStyle(name='Normal',alignment=TA_JUSTIFY, fontSize=8)    
    
    
    #Page1
    #Parametros generales del sismo
    canv.setFillColor(HexColor("#667f00"))
    canv.rect(0*mm, 250*mm, 630, 25, stroke=0, fill=True)
    canv.setFont('Helvetica', 12)
    canv.setFillColor(HexColor("#ffffff"))
    canv.drawString(40 * mm, 253 * mm, "Parametros generales del sismo" )
    logo_generalidades =ImageReader("PDF_Images/Sismograma_Parámetros generales.png")
    canv.drawImage(logo_generalidades,10 * mm, 234 * mm, width = 18*mm, preserveAspectRatio=True, mask='auto')
    
    #leer los datos guardados
    #Tabla, Datos
    with open(folder+"/Data/"+f"inf_general_{ID_event}.json","r") as json_file: 
        results_IG = json.load(json_file)
    
    #normal.add(ParagraphStyle(alignment=TA_LEFT,))

    local_date = results_IG[0]["inf_general"][1]
    utc_date = results_IG[0]["inf_general"][0]
    location_ev = results_IG[0]["inf_general"][6]
    lat = results_IG[0]["inf_general"][2]        
    lon = results_IG[0]["inf_general"][3]               
    dep = results_IG[0]["inf_general"][4]
    mag = results_IG[0]["inf_general"][5]        
    ubic = results_IG[0]["inf_general"][6]        
    fuente_pg = "Fuente: "+results_IG[0]["inf_general"][7]
    observ_IG= Paragraph("Observaciones: \n"+ results_IG[0]["observaciones"], normal_justifiy)
    revisado_pg = "Revisó: "+results_IG[0]['quien_reviso'].strip(",")

    Date = local_date[0:10]
    Local_Hour =local_date[11:19]
    
    Table_Data= [["Fecha",Date],
                ["Hora local",Local_Hour],
                ["Hora UTC",utc_date],
                ["Latitud",lat],
                ["Longitud",lon],
                ["Magnitud",mag],
                ["Profundidad", dep],
                [observ_IG],
                [fuente_pg],
                [""]]

    table = Table(Table_Data,colWidths=[4*cm,7*cm],
                    rowHeights=[None, None, None, None,None,None,None,4*cm ,None,None,])
    table.setStyle([('ALIGN', (0, 0), (0, 6), 'RIGHT'),
                    ('ALIGN', (1, 0), (1, 6), 'LEFT'),
                    ('GRID', (0,0), (-1,-4), 0.25, colors.green),
                    ('SPAN',(0,-3),(-1,-3)),
                    ('BOX',(0,0),(1,-1),0.25, colors.green),
                    ('BOX',(0,8),(-1,-1),0.25, colors.green),
                    ('BACKGROUND',(0,0),(0, 6),colors.darkgray),
                    ('VALIGN',(0,-3),(-1,-3),'TOP'),
                    ('FONTSIZE', (0, 0), (-1, -1),8)])
    
    table.wrapOn(canv, width, height)
    table.drawOn(canv, 85*mm, 147*mm)   #posicion de la tabla

    #Img Parametros generales del sismo
    Img_g =ImageReader((f"{folder}/Images/Mapc_{ID_event}.gif"))
    canv.drawImage(Img_g, 5* mm, 90* mm, width = 75*mm,preserveAspectRatio=True, mask='auto')

    
    
    #Mecanismo Focal
    if os.path.exists(folder+"/Data/"+f"inf_mecanismofocal_{ID_event}.json") == True:



        canv.setFillColor(HexColor("#667f00"))
        canv.rect(0*mm, 130*mm, 630, 25, stroke=0, fill=True)
        canv.setFont('Helvetica', 12)
        canv.setFillColor(HexColor("#ffffff"))
        canv.drawString( 40* mm, 133 * mm, "Mecanismo Focal" )
        logo_focal =ImageReader("PDF_Images/Mecanismo focal.png")
        canv.drawImage(logo_focal,10 * mm, 124 * mm, width = 9*mm, preserveAspectRatio=True, mask='auto')

        #Leer datos guardados

        with open(folder+"/Data/"+f"inf_mecanismofocal_{ID_event}.json","r") as json_file: ###____________
            results_MF = json.load(json_file)   
        if results_MF[0]["inf_mecanismofocal"][6] !="":
            #Tabla, Datos
            Title="Planos nodales" 
            nodal_planes = " "
            Separador =" "
            Azimuth_P1 = results_MF[0]["inf_mecanismofocal"][0]
            Buzamiento_P1 = results_MF[0]["inf_mecanismofocal"][1]
            Deslizamiento_P1 =  results_MF[0]["inf_mecanismofocal"][2]
            Azimuth_P2 = results_MF[0]["inf_mecanismofocal"][3]
            Buzamiento_P2 = results_MF[0]["inf_mecanismofocal"][4]
            Deslizamiento_P2 = results_MF[0]["inf_mecanismofocal"][5]
            Metodologia=" "
            metodologia = results_MF[0]["inf_mecanismofocal"][6]
            tex_Metodologia = Paragraph(results_MF[0]["inf_mecanismofocal"][7], normal_justifiy)

            Tipo_de_falla = results_MF[0]["tipo_f"]
            Obsv_MF =Paragraph("Observaciones: \n"+results_MF[0]["observaciones"],normal_justifiy)
            
            fuente_mf = "Fuente: "+results_MF[0]["inf_mecanismofocal"][8]
            revisadoMF = "Revisó: "+results_MF[0]['quien_reviso'].strip(",")
            
            #Estilo de la tabla
            Separador=" "
            Table_DataMF= [[Title],
                        [Separador , "Azimut", "Buzamiento", "Deslizamiento"],
                        ["Plano 1", str(Azimuth_P1)+"°", str(Buzamiento_P1)+"°", str(Deslizamiento_P1)+"°"],
                        ["Plano 2", str(Azimuth_P2)+"°", str(Buzamiento_P2)+"°", str(Deslizamiento_P2)+"°"],
                        ["Metodologia", tex_Metodologia],
                        ["Tipo de falla",Tipo_de_falla],
                        [Obsv_MF],
                        [fuente_mf],
                        [""]]

            tableMF = Table(Table_DataMF,colWidths=[2.75*cm,2.75*cm,2.75*cm,2.75*cm],
                        rowHeights=[None,None,None,None,1.5*cm,None,3*cm,None,None])
            tableMF.setStyle([('SPAN',(0,0),(-1,0)),
                            ('SPAN',(1,4),(-1,4)),
                            ('SPAN',(1,5),(-1,5)),
                            ('SPAN',(0,6),(-1,6)),
                            ('SPAN',(0,7),(-1,7)),
                            ('SPAN',(0,8),(-1,8)),
                            ('ALIGN',(0,0),(-1,1),'CENTER'),
                            ('GRID', (0,0), (-1,-3), 0.25, colors.green),
                            ('BOX', (0,0), (-1,-1), 0.25, colors.green),
                            ('BACKGROUND',(0,0),(-1, 1),colors.darkgray),
                            ('BACKGROUND',(0,2),(0, 5),colors.darkgray),
                            ('VALIGN',(0, 0),(-1,-1),'TOP'),
                            ('FONTSIZE', (0, 0), (-1, -1),8)])
            
            tableMF.wrapOn(canv, width, height)
            tableMF.drawOn(canv, 85*mm, 38*mm)   #posicion de la tabla
            
            #plot_Mecanismo_focal
            Img_mf =ImageReader((f"{folder}/Images/ball_{metodologia}_{ID_event}.png"))
            canv.drawImage(Img_mf, 20* mm, 68* mm, width = 35*mm,preserveAspectRatio=True, mask='auto')
            #plor_tipo_de_falla
            if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/fallas/{Tipo_de_falla}.png") == True:

                img_tf = ImageReader(f"fallas/{Tipo_de_falla}.png")
                canv.drawImage(img_tf, 5* mm, 35* mm, width = 70*mm, height = 50*mm, mask='auto')
        else :
            canv.setFillColor(HexColor("#667f00"))
            canv.rect(0*mm, 130*mm, 630, 25, stroke=0, fill=True)
            canv.setFont('Helvetica', 12)
            canv.setFillColor(HexColor("#ffffff"))
            canv.drawString( 40* mm, 133 * mm, "Mecanismo Focal" )
            logo_focal =ImageReader("PDF_Images/Mecanismo focal.png")
            canv.drawImage(logo_focal,10 * mm, 124 * mm, width = 9*mm, preserveAspectRatio=True, mask='auto')


            Tipo_de_falla = results_MF[0]["tipo_f"]
            Obsv_MF =Paragraph("Observaciones: \n"+results_MF[0]["observaciones"],normal_justifiy)
            fuente_mf = "Fuente: "+results_MF[0]["inf_mecanismofocal"][8]
            revisadoMF = "Revisó: "+results_MF[0]['quien_reviso'].strip(",")

            Table_DataMF= [["Tipo de falla",Tipo_de_falla],
                        [Obsv_MF],
                        [fuente_mf],
                        [""]]

            tableMF = Table(Table_DataMF,colWidths=[2.75*cm,8.25*cm],
                        rowHeights=[None,3.5*cm,None,None])
            tableMF.setStyle([('SPAN',(0,1),(-1,1)),
                            ('SPAN',(0,3),(-1,3)),
                            ('GRID', (0,0), (-1,-3), 0.25, colors.green),
                            ('BOX', (0,0), (-1,-1), 0.25, colors.green),
                            ('VALIGN',(0, 0),(-1,-1),'TOP'),
                            ('FONTSIZE', (0, 0), (-1, -1),8)])
            
            tableMF.wrapOn(canv, width, height)
            tableMF.drawOn(canv, 85*mm, 70*mm)   #posicion de la tabla
            #plot_Mecanismo_focal
            Img_mf_f =ImageReader((f"PDF_Images/mecanismo_focal_muestra.png"))
            canv.drawImage(Img_mf_f, 20* mm, 60* mm, width = 50*mm, height = 50*mm,mask=[0, 2, 0, 2, 0, 2])
        


    #Page2
    #Valores de aceleración    

    if  os.path.exists(folder+"/Data/"+f"inf_aceleracion_{ID_event}.json") == True:

        
        #Fondo
        background(ID_event)
        canv.showPage()

        canv.setFillColor(HexColor("#667f00"))
        canv.rect(0*mm, 250*mm, 630, 25, stroke=0, fill=True)
        canv.setFont('Helvetica', 12)
        canv.setFillColor(HexColor("#ffffff"))
        canv.drawString( 40* mm, 253 * mm, "Valores de aceleración" )
        logo_acceleration =ImageReader("PDF_Images/Valores_aceleracion.png")
        canv.drawImage(logo_acceleration,10 * mm, 214 * mm, width = 9*mm,preserveAspectRatio=True,  mask='auto')
        
        #leer datos guardados
        with open(folder+"/Data/"+f"inf_aceleracion_{ID_event}.json","r") as json_file: 
            results_A = json.load(json_file) 

        #Tabla, Datos
        nombre_estacion_min = results_A[0]["inf_aceleracion"][0][0]
        nombre_estacion_min_co =nombre_estacion_min[0:-8].replace(",","\n")
        codigo1 = results_A[0]["inf_aceleracion"][0][1]
        dist_epi1 = results_A[0]["inf_aceleracion"][0][2]
        dist_hip1 = results_A[0]["inf_aceleracion"][0][3]
        ac_ew1 = results_A[0]["inf_aceleracion"][0][4]
        ac_ns1 = results_A[0]["inf_aceleracion"][0][5]
        ac_z1 = results_A[0]["inf_aceleracion"][0][6]    
        ac_max_h1 = results_A[0]["inf_aceleracion"][0][7]
        grav1 = results_A[0]["inf_aceleracion"][0][8]


        nombre_estacion_max = results_A[0]["inf_aceleracion"][1][0]
        nombre_estacion_max_co = nombre_estacion_max[0:-8].replace(",","\n")
        codigo2 = results_A[0]["inf_aceleracion"][1][1]
        dist_epi2 = results_A[0]["inf_aceleracion"][1][2]
        dist_hip2 = results_A[0]["inf_aceleracion"][1][3]
        ac_ew2 = results_A[0]["inf_aceleracion"][1][4]
        ac_ns2 = results_A[0]["inf_aceleracion"][1][5]
        ac_z2 = results_A[0]["inf_aceleracion"][1][6]
        ac_max_h2 = results_A[0]["inf_aceleracion"][1][7]
        grav2 = results_A[0]["inf_aceleracion"][1][8]   
        
        nombre_estacion3 =results_A[0]["datos3"][0]
        nombre_estacion3_co =nombre_estacion3[0:-8].replace(",","\n")
        codigo3=results_A[0]["datos3"][1]
        dist_epi3=results_A[0]["datos3"][2]
        dist_hip3=results_A[0]["datos3"][3]
        ac_ew3=results_A[0]["datos3"][3]
        ac_ns3 =results_A[0]["datos3"][5]
        ac_z3 =results_A[0]["datos3"][6]
        ac_max_h3 = results_A[0]["datos3"][7]
        grav3 = results_A[0]["datos3"][8]           
        
        
        nombre_estacion4 =results_A[0]["datos4"][0]
        nombre_estacion4_co =nombre_estacion4[0:-8].replace(",","\n")        
        codigo4 =results_A[0]["datos4"][1]
        dist_epi4=results_A[0]["datos4"][2]
        dist_hip4=results_A[0]["datos4"][3]
        ac_ew4=results_A[0]["datos4"][4]
        ac_ns4=results_A[0]["datos4"][5]
        ac_z4=results_A[0]["datos4"][6]
        ac_max_h4 = results_A[0]["datos4"][7]
        grav4 = results_A[0]["datos4"][8]   
        
        fuente_a = "Fuente: "+results_A[0]["inf_aceleracion"][1][9]
        observ_A = Paragraph("Observaciones: \n"+results_A[0]["observaciones"],normal_justifiy)
        revisado = "Revisó: "+results_A[0]['quien_reviso'].strip(",")
        styles=getSampleStyleSheet()
        
        convencion1=""
        convencion2=""
        if dist_epi1 < dist_epi2:
            convencion1="Estacion con acel. max."
            convencion2="Estación más cercana"
        else:
            convencion1="Estación más cercana y acel. max."
            convencion2="Segunda estación más cercana"

        #Tabla conf
        Table_Data_Acc= [["ESTACIÓN", " ","DISTANCIAS" ," " ,"ACELERACIONES"],
                    ["Estación","Código","Epicentral\n(km)", "Hipocentral\n(km)","Aceleracion\n maxima", "gravedad(%)"],
                    [nombre_estacion_max_co, codigo2, dist_epi2, dist_hip2, ac_max_h2, grav2 ],
                    [nombre_estacion_min_co, codigo1, dist_epi1, dist_hip1, ac_max_h1, grav1 ],
                    [nombre_estacion3_co, codigo3, dist_epi3, dist_hip3, ac_max_h3, grav3 ],
                    [nombre_estacion4_co, codigo4, dist_epi4, dist_hip4, ac_max_h4, grav4 ],
                    ["",convencion1,"","", convencion2], 
                    [observ_A],
                    [fuente_a],
                    [""]]

        table_Acc = Table(Table_Data_Acc,colWidths=[2.80*cm,1.25*cm,1.8*cm,1.8*cm ,1.8*cm],
                    rowHeights=[0.5*cm,1*cm,1.1*cm,1.1*cm,1.1*cm,1.1*cm,0.4*cm, 2.3*cm,0.5*cm,0.5*cm])
        table_Acc.setStyle([('GRID', (0,0), (-1,-3), 0.25, colors.green),
                        ('SPAN',(0,0),(1,0)),
                        ('SPAN',(2,0),(3,0)),
                        ('SPAN',(4,0),(5,0)),
                        ('SPAN',(1,6),(2,6)),
                        ('SPAN',(1,6),(2,6)),
                        ('SPAN',(4,6),(5,6)),
                        ('SPAN',(0,7),(-1,7)),
                        ('SPAN',(0,8),(-1,8)),                          
                        ('VALIGN',(0,-3),(-1,-3),'TOP'),
                        ('BOTTOMPADDING',(0,2),(0,5),1),
                        ('BOTTOMPADDING',(0,6),(-1,6),1),
                        ('ALIGN',(0,0),(-1,5),'CENTER'),
                        ('BACKGROUND',(0,6),(0,6),colors.red),
                        ('BACKGROUND',(3,6),(3,6),colors.darkseagreen),                        
                        ('BACKGROUND',(0,0),(-1, 1),colors.darkgray),
                        ('BACKGROUND',(0,3),(0,3),colors.darkseagreen),
                        ('BACKGROUND',(0,2),(0,2),colors.red),
                        ('BOX', (0,0), (-1,-1), 0.25, colors.green),
                        ('VALIGN',(0,0),(-1,6),'MIDDLE'),
                        ('FONTSIZE', (0,0), (-1, 5),8),
                        ('FONTSIZE', (0,7), (-1, -1),8),
                        ('FONTSIZE', (0,6), (-1, 6),5)])

      
        table_Acc.wrapOn(canv, width, height)
        table_Acc.drawOn(canv, 85*mm, 152*mm)   #posicion de la tabla
        styles = getSampleStyleSheet()         
        #Titulo mapa aceleraciones
        canv.setFont('Helvetica', 7)
        canv.setFillColor(HexColor("#000000"))
        canv.drawString(28* mm, 240* mm, "Mapa de aceleraciones" )
        #Img aceleraciones
        Img_a =ImageReader(f"{folder}/Images/map_ac_{ID_event}.png")
        canv.drawImage(Img_a, 5* mm, 90* mm, width = 75*mm,preserveAspectRatio=True, mask='auto')
        #Leyenda aceleraciones
        Img_leyenda_acc =ImageReader("PDF_Images/leyenda_ac.png")
        canv.drawImage(Img_leyenda_acc, 27* mm, 70* mm, width = 37*mm,preserveAspectRatio=True, mask='auto')
    
    
    if  os.path.exists(folder+"/Data/"+f"inf_instrumental_{ID_event}.json") == True:
  

        #Intensidad instrumental
        canv.setFillColor(HexColor("#667f00"))
        canv.rect(0*mm, 140*mm, 630, 25, stroke=0, fill=True)
        canv.setFont('Helvetica', 12)
        canv.setFillColor(HexColor("#ffffff"))
        canv.drawString( 40* mm, 143 * mm, "Intensidad instrumental" )
        logo_Instrumental_intensity=ImageReader("PDF_Images/Intensidad instrumental.png")
        canv.drawImage(logo_Instrumental_intensity,10 * mm, 39 * mm, width = 12*mm, preserveAspectRatio=True, mask='auto')

        #Tabla, Datos
        with open(folder+"/Data/"+f"inf_instrumental_{ID_event}.json","r") as json_file:
            results_II = json.load(json_file)
        
        Scale ="Mercalli modificada (MMI)"        
        int_max_romano = results_II[0]["inf_instrumental"][0]        
        movimiento = results_II[0]["inf_instrumental"][1] 
        danno = results_II[0]["inf_instrumental"][2]       
        pga_max = results_II[0]["inf_instrumental"][3]               
        pgv_max = results_II[0]["inf_instrumental"][4]        
        fuente = "Fuente: "+results_II[0]["inf_instrumental"][5]
        observ_ii=  Paragraph("Observaciones: \n"+results_II[0]["observaciones"], normal_justifiy)
        revisado_ii = "Revisó: "+results_II[0]['quien_reviso'].strip(",")
        Description = Paragraph(f"Mapa que muestra el movimiento del terreno por niveles de intensidad y los posibles efectos causados por el sismo, generado de la combinación de registros en sismómetros, acelerógrafos, relaciones de atenuación de la energía sísmica e información sobre condiciones sísmicas locales.", normal_justifiy)


        Table_Data_ii= [["Descripción", Description],
                    ["Escala",Scale],
                    ["Intensidad máxima", int_max_romano],
                    ["Percepción del movimiento",movimiento],
                    ["Daño", danno],
                    ["Máxima aceleración", str(pga_max)+" %g (PGA)"],
                    ["Máxima velocidad", str(pgv_max)+" cm/s"],
                    [observ_ii],
                    [fuente],
                    [""]]

        table_ii = Table(Table_Data_ii,colWidths=[4*cm, 7.25*cm],
                    rowHeights=[2.75*cm,0.5*cm,0.5*cm,1*cm,0.5*cm,0.5*cm,0.5*cm,2.5*cm, 0.5*cm, 0.5*cm])
        table_ii.setStyle([('GRID', (0,0), (-1,-3), 0.25, colors.green),
                        ('BOX', (0,0), (-1,-1), 0.25, colors.green),
                        ('BACKGROUND',(0,0),(0, 6),colors.darkgray),
                        ('SPAN',(0,7),(-1,7)),
                        ('SPAN',(0,8),(-1,8)),
                        ('SPAN',(0,9),(-1,9)),
                        ('VALIGN',(0,0),(-1,-1),'TOP'),
                        ('FONTSIZE', (0, 0), (-1, -1),8)])
        
        table_ii.wrapOn(canv, width, height)
        table_ii.drawOn(canv, 85*mm, 39*mm)   #posicion de la tabla
        styles = getSampleStyleSheet() 
        
        #img_intensidad instrumental
        Img_ii =ImageReader(f"{folder}/Images/map_intensity_{ID_event}.jpg")
        canv.drawImage(Img_ii, 7*mm, -90*mm, width = 70*mm,preserveAspectRatio=True, mask='auto')
		
   
    

    if  os.path.exists(folder+"/Data/"+f"inf_intpercibida_{ID_event}.json") == True:
        #Page3 
        #Intensidad percibida
        
        #Fondo
        background(ID_event)
        canv.showPage()

       
        canv.setFillColor(HexColor("#667f00"))
        canv.rect(0*mm, 250*mm, 630, 25, stroke=0, fill=True)
        canv.setFont('Helvetica', 12)
        canv.setFillColor(HexColor("#ffffff"))
        canv.drawString( 40* mm, 253 * mm, "Intensidad percibida (macrosísmica)" )
        logo_PerceivedInt =ImageReader("PDF_Images/Intensidad macrosísmica.png")
        canv.drawImage(logo_PerceivedInt, 10 * mm, 236 * mm, width = 9*mm,preserveAspectRatio=True, mask='auto')

        #Tabla, Datos
        with open(folder+"/Data/"+f"inf_intpercibida_{ID_event}.json","r") as json_file: 
            results_IP = json.load(json_file)    
        
        image_n_report = Image('PDF_Images/Numero_reportes1.png', 1.257*cm, 1*cm)
        image_centros = Image('PDF_Images/Centros_poblados.png', 1.1061*cm, 1*cm)
        image_muni = Image('PDF_Images/Municipios.png',1.138*cm, 1*cm)
        image_depart = Image('PDF_Images/Departamentos.png',1*cm, 1.294*cm)

        n_reportes = results_IP[0]["inf_intpercibida"][0]
        n_centros_poblados = results_IP[0]["inf_intpercibida"][1]
        n_municipio = results_IP[0]["inf_intpercibida"][2]
        n_departamentos = results_IP[0]["inf_intpercibida"][3]
        int_maxima = results_IP[0]["inf_intpercibida"][4]
        intensidad_reportada = results_IP[0]["inf_intpercibida"][5]
        centro_poblado_max = Paragraph(results_IP[0]["inf_intpercibida"][6], normal_justifiy)
        municipio_max = Paragraph(results_IP[0]["inf_intpercibida"][7], normal_justifiy)
        mun_rep_max = Paragraph(results_IP[0]["inf_intpercibida"][8],normal_justifiy)
        poblados_alejados_max = results_IP[0]["inf_intpercibida"][9]
        descripcion_ip = Paragraph( results_IP[0]["descr_im"],normal_justifiy )
        sent_otros_paises =  Paragraph(results_IP[0]["sent_otros_paises"],normal_justifiy )
        if not sent_otros_paises:
            sent_otros_paises = Paragraph("No fue reportado como sentido en otros paises.", normal_justifiy)        
        replicas_sentidas = Paragraph( results_IP[0]["replicas_sentidas"], normal_justifiy)
        if not replicas_sentidas:
            replicas_sentidas = "Ninguna."
            
        revisado_ip ="Revisó: "+ results_IP[0]['quien_reviso'].strip(",")
        fuente_ip= "Fuente: "+results_IP[0]["inf_intpercibida"][10]

        Table_Data_pi= [["Número de reportes recibidos", n_reportes, image_n_report ],
                    [f"Sitios donde se reportó como \nsentido",f"provenientes de \n"+str(n_centros_poblados)+"\nCentros poblados",image_centros],
                    ["","ubicados en\n"+str(n_municipio)+"\nmunicipios",image_muni],
                    ["","de \n"+str(n_departamentos)+"\ndepartamentos",image_depart],
                    ["Intensidad máxima Reportada",f"{int_maxima}.  {intensidad_reportada}"],
                    [f"Municipios donde se \nreportó la intensidad máxima.", municipio_max],
                    ["Descripción intensidad \nmáxima",Paragraph(EMS_98[str(int_maxima)],normal_justifiy )],
                    [f"Municipios con mayor \nnúmero de reportes.", mun_rep_max ],
                    [f"Centros poblados más alejados \ndel hipocentro donde fue \nreportado como sentido \nel sismo.", poblados_alejados_max],
                    ["Sentido en otros países", sent_otros_paises],
                    [f"Réplicas reportadas \ncomo sentidas", replicas_sentidas ],
                    [fuente_ip],
                    [""]]

        table_pi = Table(Table_Data_pi,colWidths=[4.2*cm, 3.6*cm],
                    rowHeights=[None, None, None , None,1*cm,1*cm, 2.5*cm, None, None, 1*cm, None, 0.5*cm, 0.5*cm])

        table_pi.setStyle([('GRID', (0,4), (-1,-3), 0.25, colors.green),
                    ('GRID', (0,0), (0,1), 0.25, colors.green),
                    ('BOX', (1,0), (-1,0), 0.25, colors.green),
                    ('BACKGROUND',(0,0),(0, -3),colors.darkgray),
                    ('BACKGROUND',(1,4),(1,4), HexColor(color_int[str(int_maxima)])),
                    ('VALIGN',(0,4),(-1,-1),'TOP'),
                    ('VALIGN',(0,0),(-1,2),'MIDDLE'),
                    ('VALIGN',(1,0),(1,-1),'TOP'),                
                    ('ALIGN',(1,0),(1,3),'CENTER'),
                    ('FONTSIZE', (0, 0), (-1, -1),8),
                    ('FONTSIZE', (1, 0), (1, 0),20),
                    ('FONTSIZE', (1, 1), (1, 1),10),
                    ('FONTSIZE', (1, 2), (1, 2),10), 
                    ('FONTSIZE', (1, 3), (1, 3),10),                                 
                    ('SPAN',(0,1),(0,3)),
                    ('SPAN',(1,4),(-1,4)),
                    ('SPAN',(1,5),(-1,5)),
                    ('SPAN',(1,6),(-1,6)),
                    ('SPAN',(1,7),(-1,7)),
                    ('SPAN',(1,8),(-1,8)),
                    ('SPAN',(1,9),(-1,9)),
                    ('SPAN',(1,10),(-1,10)),
                    
                    ('BOX', (0,0), (-1,-1), 0.25, colors.green)])
                    
                    
        table_pi.wrapOn(canv, width, height)
        table_pi.drawOn(canv, 85*mm, 70*mm)   #posicion de la tabla
        styles = getSampleStyleSheet() 
        #Titulo mapa de intensidades
        canv.setFont('Helvetica', 7)
        canv.setFillColor(HexColor("#000000"))
        canv.drawString(25* mm, 235* mm, "Mapa de intensidades" )
        #Img mapa intensidad percibida
        Img_ip =ImageReader(f"{folder}/Images/map_int_perc_{ID_event}.png")
        canv.drawImage(Img_ip, 5* mm, 119* mm, width = 75*mm,preserveAspectRatio=True, mask='auto') ## Si existe el mapa en el visor de sismos 
        #canv.drawImage(Img_ip, 6* mm, 119* mm, width = 75*mm,preserveAspectRatio=True, mask='auto')  ## Si el mapa el tomado del administrador de intensidades     
        #Img convenciones mapa intensidad percibida
        Img_c_ip =ImageReader(f"PDF_Images/leyenda_intensidad_persibida.png")
        canv.drawImage(Img_c_ip, 4* mm, 130* mm, width = 80*mm,preserveAspectRatio=True, mask='auto')
        #Img histograma intensidad percibida
        Img_ihp =ImageReader(f"{folder}/Images/histo_int_percibida_{ID_event}.png")
        canv.drawImage(Img_ihp, 5* mm, 30* mm, width = 75*mm,preserveAspectRatio=True, mask='auto')
        #Leyenda epicentro
        Img_epicentro_pi =ImageReader("PDF_Images/Epicentro_leyenda.jpeg")
        canv.drawImage(Img_epicentro_pi, 5* mm, 132* mm, width = 20*mm,preserveAspectRatio=True, mask='auto')
    #Fondo
    background(ID_event)
    canv.showPage()
    
   
    #Imagenes_GUI
    Dir_img="Events/"+ID_event+"/Images"
    IMGs = os.listdir (Dir_img)
    #IMGs_Natures_Effects=[]



    #Page4
    #Reporte de daños
    """
    if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/inf_repdanos_{ID_event}.json") == True:

        canv.setFillColor(HexColor("#667f00"))
        canv.rect(0*mm, 250*mm, 630, 25, stroke=0, fill=True)
        canv.setFont('Helvetica', 12)
        canv.setFillColor(HexColor("#ffffff"))
        canv.drawString( 40* mm, 253 * mm, "Reporte de daños en infraestructura" )
        logo_Damage =ImageReader("PDF_Images/Reporte daños.png")
        canv.drawImage(logo_Damage, 10 * mm, 209 * mm, width = 8*mm,preserveAspectRatio=True, mask='auto')
        
        with open(folder+"/Data/"+f"inf_repdanos_{ID_event}.json","r") as json_file1: ###____________
                        results_rd = json.load(json_file1)
        #Datos tabla 1
        n_mun = results_rd[0]["n_mun"]
        dis_rd = results_rd[0]["dist_rep"]
        danos = Paragraph(results_rd[0]["danos"], normal_justifiy)
        
        fuente = "Fuente: "+results_rd[0]["fuente"]
        
			
        revisado= results_rd[0]["autor"]

        Table_Damage_report= [[f"Número municipios donde se reportaron \ndaños",n_mun],
                            [f"Distancia hipocentral máxima de reporte \nde daños",dis_rd]]
    
        tableDR = Table(Table_Damage_report, colWidths = [5.5*cm,5.5*cm], rowHeights=[1*cm,1*cm])
        tableDR.setStyle([('GRID', (0,0), (-1,-1), 0.25, colors.green),
                        ('BACKGROUND',(0,0),(0, 1),colors.darkgray),
                        ('VALIGN',(-2,-2),(-1,-1),'TOP'),
                        ('FONTSIZE', (0, 0), (-1, -1),8)])
        
        tableDR.wrapOn(canv, width, height)
        tableDR.drawOn(canv, 85*mm, 225*mm)   #posicion de la tabla
        styles = getSampleStyleSheet()    

        #Datos tabla 2
        report_damage=f"Fisuras y caída en revestimiento, grietas en muros y caída de tejas, fisuras y caída de revestimiento y caída de tejas, fisuras en revestimiento y grietas en muros, fisuras en revestimiento, grietas en muros y caída de revestimiento, fisuras en revestimiento y grietas en muros."
        fuente_dr=""
        autor_dr=""

        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/inf_dep_mun{ID_event}.json") == True:
            with open(folder+"/Data/"+f"inf_dep_mun{ID_event}.json","r") as json_file2: ###____________
                results_dep_mun = json.load(json_file2)

            if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/inf_dep{ID_event}.json") == True:
                with open(folder+"/Data/"+f"inf_dep{ID_event}.json","r") as json_file3: ###____________
                    results = json.load(json_file3)

                
                Table_DataDR= [["Departamento","Municipio"]]
                
                
                author_dr2= ""
                if len (revisado)<2:
                    for author in revisado:
                        author_dr2 += author+","
                    results_rd[0]["autor"] = author_dr2 # autores
                else:
                    pass
                results_dep = results[0]["departamentos"]

                for dep in results_dep:
                    
                    mun = ""
                    municipios = results_dep_mun[0][dep]
                    for m in municipios:
                        mun += m+", "     #municipios

                    Table_DataDR.append([Paragraph(dep,normal_justifiy),Paragraph(mun[:-2], normal_justifiy)])


                Table_DataDR.append(["Daños Reportados",danos])
                Table_DataDR.append([Paragraph(fuente, normal_justifiy)])
                Table_DataDR.append(["Revisó: "+ results_rd[0]["autor"][:-1].strip(",")])
                
                y_position = 150 - ((len(Table_DataDR) - 2.5)*3.2)
                
                tableDR_2 = Table(Table_DataDR, colWidths=[3*cm,8*cm])
                
                tableDR_2.setStyle([('BOX',(0,0),(-1,-1),0.25, colors.green),
                                ('SPAN',(0,-1),(-1,-1)),
                                ('SPAN',(0,-2),(-1,-2)),
                                ('VALIGN',(0,0),(-1,-1),'TOP'),
                                ('BACKGROUND',(0,0),(1, 0),colors.darkgray),
                                ('BACKGROUND',(0,1),(0, -3),colors.darkgray),
                                ('GRID', (0,0), (-1,-3), 0.25, colors.green),
                                ('FONTSIZE', (0, 0), (-1, -1),8)])
                tableDR_2.wrapOn(canv, width, height)
                tableDR_2.drawOn(canv, 85*mm, y_position*mm)   #posicion de la tabla
        
        #Fondo
        background(ID_event)
        canv.showPage()  
    """
        
    #Page5
    #Efectos en la naturaleza
    if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/inf_efnatu_{ID_event}.json") == True:

        canv.setFillColor(HexColor("#667f00"))
        canv.rect(0*mm, 250*mm, 630, 25, stroke=0, fill=True)
        canv.setFont('Helvetica', 12)
        canv.setFillColor(HexColor("#ffffff"))
        canv.drawString( 40* mm, 253 * mm, "Efectos en la naturaleza" )
        logo_Effects =ImageReader("PDF_Images/Efectos_en_la_naturaleza.png")
        canv.drawImage(logo_Effects, 10 * mm, 187 * mm, width = 12*mm,preserveAspectRatio=True, mask='auto')

        Tipo_de_falla = results_MF[0]["tipo_f"]
        Descrip1="Algunos efectos marginales sobre la \nnaturaleza que fueron reportados \nincluye agrietamientos de cientos de\nmetros de longitud y pocos centímetros\nde anchura en terrenos aluviales poco\n compactados y saturados, en la margen\n del río Magdalena"
        Descrip2= "se reportó oleaje anómalo \npor agitación en el río y en piscinas"
        fuente_en = "Fuente: "+results_MF[0]["inf_mecanismofocal"][8]
        revisado_en = "Revisó: "+results_MF[0]['quien_reviso'].strip(",")

        Table_DataMF= [["Efecetos reportados"],
                    ["Tipo ", "Decripción"],
                    ["Agrietamiento del \ntecho", Descrip1],
                    ["Olejae anomalo \n de masas de agua",Descrip2],
                    [fuente_en],
                    [""]]

        tableMF = Table(Table_DataMF,colWidths=[2.80*cm,5.6*cm],
                    rowHeights=[0.5*cm,0.5*cm,3.5*cm,1*cm,1*cm,0.5*cm], repeatRows=1)
        tableMF.setStyle([('SPAN',(0,0),(-1,0)),
                        ('SPAN',(0,-1),(-1,-1)),
                        ('GRID', (0,0), (-1,-3), 0.25, colors.green),
                        ('BACKGROUND',(0,0),(-1, 1),colors.darkgray),
                        ('BOX', (0,0), (-1,-1), 0.25, colors.green),
                        ('ALIGN',(0,0),(1,0),'CENTER'),
                        ('VALIGN',(0, 0),(-1,-1),'TOP'),
                        ('FONTSIZE', (0, 0), (-1, -1),8)])
        
        tableMF.wrapOn(canv, width, height)
        tableMF.drawOn(canv, 110*mm, 175*mm)   #posicion de la tabla


        #Fondo
        background(ID_event)
        canv.showPage()      

 

    #Page6
    #Sismos historicos en la region
    if os.path.exists(os.path.dirname(os.path.abspath(__file__))+f"/Events/{ID_event}/Data/sis_his_{ID_event}.json") == True:
        canv.setFillColor(HexColor("#667f00"))
        canv.rect(0*mm, 250*mm, 630, 25, stroke=0, fill=True)
        canv.setFont('Helvetica', 12)
        canv.setFillColor(HexColor("#ffffff"))
        canv.drawString( 40* mm, 253 * mm, "Sismos historicos en la region" )
        logo_history =ImageReader("PDF_Images/Sismicidad_Historica.png")
        canv.drawImage(logo_history, 10 * mm, 164 * mm, width =7*mm,preserveAspectRatio=True, mask='auto')

        #Fondo
        background(ID_event)
        canv.showPage()  


    pi.perceived_intensity(ID_event)

    canv.save()

