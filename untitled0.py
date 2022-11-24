# -*- coding: utf-8 -*-
"""
Scraper Pesquisas - Junta Comercial do Estado de Sao Paulo

https://www.jucesponline.sp.gov.br/

Created on Wed Nov  2 12:53:23 2022

@author: Joaquin Liwski
"""

#Import Libraries
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.select import Select
import calendar
import pandas as pd
import time
import re
import winsound


#Frequency for beep
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second


                                                                     

#LOOP OVER YEAR AND MONTH, EACH TIME YOU'LL HAVE TO ENTER CAPTCHA
#for year in list(range(2000,2023,1)):
#    for month in list(range(1,13,1)):
driver5 = webdriver.Chrome(executable_path = r'C:\Program Files\chromedriver.exe') #Execute driver
months = range(6,9,1)
for month in months:
    year=2019
    types1 = [ "1", "2"]
    types2 = ["6", "7", "8", "9", "10","3", "4", "5",
             "11", "12", "13", "14", "15", "16", "17", "18", "19",
             "20", "21", "9999"]
    
    #Create data frame to fill
    df = pd.DataFrame(columns=['NIRE', 'Empresa', 'Município', 'Month','Year'])

    
    #Loop over business types
    for type in types2:
        #Get Web Page
        driver5.get('https://www.jucesponline.sp.gov.br/BuscaAvancada.aspx?IDProduto=') #Open web page
        
            
        #Date variable - LAST DAY OF MONTH 
        _, last_day = calendar.monthrange(year, month)
        #Select Type
        txtTipo = Select(driver5.find_element("id",'ctl00_cphContent_frmBuscaAvancada_ddlTipoEmpresa')) #Select ID Tipo de Empresa
        txtTipo.select_by_value(type) #By value
        #txtTipo.select_by_visibleText("Empresário") #By text
        #txtTipo.select_by_index(1) #By index
        
        #Select Date Inicio
        txtMunicipio = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_txtDataAberturaInicio')
        initmonth= '01/'+str("%02d" % month)+'/'+str(year)
        txtMunicipio.send_keys(initmonth)
        
        #Select Date Fim
        txtMunicipio = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_txtDataAberturaFim')
        endmonth= str(last_day)+'/'+str("%02d" % month)+'/'+str(year)
        txtMunicipio.send_keys(endmonth)
        
        #Select all firms created (not only the active ones) "Mostrar somente empresas ativas"
        chkActive = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_chkAtivas').click()
        btPesquisar = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_btPesquisar')
        btPesquisar.click()
        seconds=10
        try:
            data_table = WebDriverWait(driver5,seconds).until(EC.presence_of_element_located((By.ID,'ctl00_cphContent_gdvResultadoBusca_gdvContent')))
              
            #Defining conditions for loop while month-year
            totalpageresult=0
            lastpageresult=2
            #In loop I'll redefine them, I just need them to be different, thats the condition to keep looping
            
            #While looping month-year
            while int(lastpageresult) != int(totalpageresult):
                #Scrape table from a page
                time.sleep(1)
                tabletemp = pd.read_html(driver5.find_element('xpath','//*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent"]').get_attribute('outerHTML'))[0]
                tabletemp = tabletemp.drop(tabletemp.columns[3], axis=1)
                tabletemp['Month']= str(month)
                tabletemp['Year'] = str(year)
                if type == "1":
                    tabletemp['Type']="Empresario"
                elif type == "2":
                    tabletemp['Type']="Sociedade Limitada"
                elif type == "3":
                    tabletemp['Type']="Sociedade por Acoes"
                elif type == "4":
                    tabletemp['Type']="Cooperativa"
                elif type == "5":
                    tabletemp['Type']="Consorcio"
                elif type == "6":
                    tabletemp['Type']="Grupo"
                elif type == "7":
                    tabletemp['Type']="Comandita Simple"
                elif type == "8":
                    tabletemp['Type']="Comandita por Acoes"
                elif type == "9":
                    tabletemp['Type']="Capital Industria"
                elif type == "10":
                    tabletemp['Type']="Solidaria"
                elif type == "11":
                    tabletemp['Type']="Armazens Gerais Ltda"
                elif type == "12":
                    tabletemp['Type']="Empresa Estrangeira"
                elif type == "13":
                    tabletemp['Type']="Binacional Ltda"
                elif type == "14":
                    tabletemp['Type']="Sociedade em Nome Coletivo"
                elif type == "15":
                    tabletemp['Type']="Empresa Publica"
                elif type == "16":
                    tabletemp['Type']="Subsidiaria Integral"
                elif type == "17":
                    tabletemp['Type']="Sociedade em Conta de Participacao"
                elif type == "18":
                    tabletemp['Type']="Armazens Gerais S/A"
                elif type == "19":
                    tabletemp['Type']="Binacional S/A"
                elif type == "21":
                    tabletemp['Type']="Armazens Gerais Empresario"
                else:
                    tabletemp['Type'] = "Outros"
                
                #Append this page to new table
                df = df.append(tabletemp)
                
                #Changing while condition
                #noninteresting, lastpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResults').text.replace('.',''))
                #totalpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResultCount').text.replace('.',''))[0]
                            
                #Click next page button
                try:
                    driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_btrNext_lbtText').click()
                    time.sleep(1)
                except: 
                    pass 
                #Changing while condition
                noninteresting, lastpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResults').text.replace('.',''))
                totalpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResultCount').text.replace('.',''))[0]
                
                print(f'Month {month} Year {year}, {lastpageresult} rows out of {totalpageresult}. Company Type "{type}"')
            
            #Scrape Last Page
            tabletemp = pd.read_html(driver5.find_element('xpath','//*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent"]').get_attribute('outerHTML'))[0]
            tabletemp = tabletemp.drop(tabletemp.columns[3], axis=1)
            tabletemp['Month']= str(month)
            tabletemp['Year'] = str(year)
            if type == "1":
                tabletemp['Type']="Empresario"
            elif type == "2":
                tabletemp['Type']="Sociedade Limitada"
            elif type == "3":
                tabletemp['Type']="Sociedade por Acoes"
            elif type == "4":
                tabletemp['Type']="Cooperativa"
            elif type == "5":
                tabletemp['Type']="Consorcio"
            elif type == "6":
                tabletemp['Type']="Grupo"
            elif type == "7":
                tabletemp['Type']="Comandita Simple"
            elif type == "8":
                tabletemp['Type']="Comandita por Acoes"
            elif type == "9":
                tabletemp['Type']="Capital Industria"
            elif type == "10":
                tabletemp['Type']="Solidaria"
            elif type == "11":
                tabletemp['Type']="Armazens Gerais Ltda"
            elif type == "12":
                tabletemp['Type']="Empresa Estrangeira"
            elif type == "13":
                tabletemp['Type']="Binacional Ltda"
            elif type == "14":
                tabletemp['Type']="Sociedade em Nome Coletivo"
            elif type == "15":
                tabletemp['Type']="Empresa Publica"
            elif type == "16":
                tabletemp['Type']="Subsidiaria Integral"
            elif type == "17":
                tabletemp['Type']="Sociedade em Conta de Participacao"
            elif type == "18":
                tabletemp['Type']="Armazens Gerais S/A"
            elif type == "19":
                tabletemp['Type']="Binacional S/A"
            elif type == "21":
                tabletemp['Type']="Armazens Gerais Empresario"
            else:
                tabletemp['Type'] = "Outros"
            
            
            #Append this page to new table
            df = df.append(tabletemp)
               
                
            #Scrape table from a LAST page
            #tabletemp = pd.read_html(driver5.find_element('xpath','//*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent"]').get_attribute('outerHTML'))[0]
            #tabletemp = tabletemp.drop(tabletemp.columns[3], axis=1)
            #tabletemp['Month']= str(month)
            #tabletemp['Year'] = str(year)
            
            #Append this LAST page to new table
            #df = df.append(tabletemp)
            
        except:
            pass
        
        #Get ready to introduce new captcha
        winsound.Beep(frequency, duration) #Makes a sound letting you know its time
    for type in types1:
        #Search Until Captcha - Open Driver
        
        #First 10 days
        #Get Web Page
        driver5.get('https://www.jucesponline.sp.gov.br/BuscaAvancada.aspx?IDProduto=') #Open web page
        
            
        #Date variable - LAST DAY OF MONTH 
        _, last_day = calendar.monthrange(year, month)
        #Select Type
        txtTipo = Select(driver5.find_element("id",'ctl00_cphContent_frmBuscaAvancada_ddlTipoEmpresa')) #Select ID Tipo de Empresa
        txtTipo.select_by_value(type) #By value
        #txtTipo.select_by_visibleText("Empresário") #By text
        #txtTipo.select_by_index(1) #By index
        
        #Select Date Inicio
        txtMunicipio = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_txtDataAberturaInicio')
        initmonth= '01/'+str("%02d" % month)+'/'+str(year)
        txtMunicipio.send_keys(initmonth)
        
        #Select Date Fim
        txtMunicipio = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_txtDataAberturaFim')
        endmonth= '02/'+str("%02d" % month)+'/'+str(year)
        txtMunicipio.send_keys(endmonth)
        
        #Select all firms created (not only the active ones) "Mostrar somente empresas ativas"
        chkActive = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_chkAtivas').click()
        btPesquisar = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_btPesquisar')
        btPesquisar.click()
        seconds=10
        try:
            data_table = WebDriverWait(driver5,seconds).until(EC.presence_of_element_located((By.ID,'ctl00_cphContent_gdvResultadoBusca_gdvContent')))
              
            #Defining conditions for loop while month-year
            totalpageresult=0
            lastpageresult=2
            #In loop I'll redefine them, I just need them to be different, thats the condition to keep looping
            
            #While looping month-year
            while int(lastpageresult) != int(totalpageresult):
                #Scrape table from a page
                time.sleep(1)
                tabletemp = pd.read_html(driver5.find_element('xpath','//*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent"]').get_attribute('outerHTML'))[0]
                tabletemp = tabletemp.drop(tabletemp.columns[3], axis=1)
                tabletemp['Month']= str(month)
                tabletemp['Year'] = str(year)
                if type == "1":
                    tabletemp['Type']="Empresario"
                elif type == "2":
                    tabletemp['Type']="Sociedade Limitada"
                elif type == "3":
                    tabletemp['Type']="Sociedade por Acoes"
                elif type == "4":
                    tabletemp['Type']="Cooperativa"
                elif type == "5":
                    tabletemp['Type']="Consorcio"
                elif type == "6":
                    tabletemp['Type']="Grupo"
                elif type == "7":
                    tabletemp['Type']="Comandita Simple"
                elif type == "8":
                    tabletemp['Type']="Comandita por Acoes"
                elif type == "9":
                    tabletemp['Type']="Capital Industria"
                elif type == "10":
                    tabletemp['Type']="Solidaria"
                elif type == "11":
                    tabletemp['Type']="Armazens Gerais Ltda"
                elif type == "12":
                    tabletemp['Type']="Empresa Estrangeira"
                elif type == "13":
                    tabletemp['Type']="Binacional Ltda"
                elif type == "14":
                    tabletemp['Type']="Sociedade em Nome Coletivo"
                elif type == "15":
                    tabletemp['Type']="Empresa Publica"
                elif type == "16":
                    tabletemp['Type']="Subsidiaria Integral"
                elif type == "17":
                    tabletemp['Type']="Sociedade em Conta de Participacao"
                elif type == "18":
                    tabletemp['Type']="Armazens Gerais S/A"
                elif type == "19":
                    tabletemp['Type']="Binacional S/A"
                elif type == "21":
                    tabletemp['Type']="Armazens Gerais Empresario"
                else:
                    tabletemp['Type'] = "Outros"
                
                #Append this page to new table
                df = df.append(tabletemp)
                
                #Changing while condition
                #noninteresting, lastpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResults').text.replace('.',''))
                #totalpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResultCount').text.replace('.',''))[0]
                            
                #Click next page button
                try:
                    driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_btrNext_lbtText').click()
                    time.sleep(1)
                except: 
                    pass 
                #Changing while condition
                noninteresting, lastpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResults').text.replace('.',''))
                totalpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResultCount').text.replace('.',''))[0]
                
                print(f'Month {month} Year {year}, {lastpageresult} rows out of {totalpageresult}. Company Type "{type}"')
            
            #Scrape Last Page
            tabletemp = pd.read_html(driver5.find_element('xpath','//*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent"]').get_attribute('outerHTML'))[0]
            tabletemp = tabletemp.drop(tabletemp.columns[3], axis=1)
            tabletemp['Month']= str(month)
            tabletemp['Year'] = str(year)
            if type == "1":
                tabletemp['Type']="Empresario"
            elif type == "2":
                tabletemp['Type']="Sociedade Limitada"
            elif type == "3":
                tabletemp['Type']="Sociedade por Acoes"
            elif type == "4":
                tabletemp['Type']="Cooperativa"
            elif type == "5":
                tabletemp['Type']="Consorcio"
            elif type == "6":
                tabletemp['Type']="Grupo"
            elif type == "7":
                tabletemp['Type']="Comandita Simple"
            elif type == "8":
                tabletemp['Type']="Comandita por Acoes"
            elif type == "9":
                tabletemp['Type']="Capital Industria"
            elif type == "10":
                tabletemp['Type']="Solidaria"
            elif type == "11":
                tabletemp['Type']="Armazens Gerais Ltda"
            elif type == "12":
                tabletemp['Type']="Empresa Estrangeira"
            elif type == "13":
                tabletemp['Type']="Binacional Ltda"
            elif type == "14":
                tabletemp['Type']="Sociedade em Nome Coletivo"
            elif type == "15":
                tabletemp['Type']="Empresa Publica"
            elif type == "16":
                tabletemp['Type']="Subsidiaria Integral"
            elif type == "17":
                tabletemp['Type']="Sociedade em Conta de Participacao"
            elif type == "18":
                tabletemp['Type']="Armazens Gerais S/A"
            elif type == "19":
                tabletemp['Type']="Binacional S/A"
            elif type == "21":
                tabletemp['Type']="Armazens Gerais Empresario"
            else:
                tabletemp['Type'] = "Outros"
            
            
            #Append this page to new table
            df = df.append(tabletemp)
               
                
            #Scrape table from a LAST page
            #tabletemp = pd.read_html(driver5.find_element('xpath','//*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent"]').get_attribute('outerHTML'))[0]
            #tabletemp = tabletemp.drop(tabletemp.columns[3], axis=1)
            #tabletemp['Month']= str(month)
            #tabletemp['Year'] = str(year)
            
            #Append this LAST page to new table
            #df = df.append(tabletemp)
            
        except:
            pass
        
        #Get ready to introduce new captcha
        winsound.Beep(frequency, duration) #Makes a sound letting you know its time
        
        
        #First 10 days
        #Get Web Page
        driver5.get('https://www.jucesponline.sp.gov.br/BuscaAvancada.aspx?IDProduto=') #Open web page
        
            
        #Date variable - LAST DAY OF MONTH 
        _, last_day = calendar.monthrange(year, month)
        #Select Type
        txtTipo = Select(driver5.find_element("id",'ctl00_cphContent_frmBuscaAvancada_ddlTipoEmpresa')) #Select ID Tipo de Empresa
        txtTipo.select_by_value(type) #By value
        #txtTipo.select_by_visibleText("Empresário") #By text
        #txtTipo.select_by_index(1) #By index
        
        #Select Date Inicio
        txtMunicipio = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_txtDataAberturaInicio')
        initmonth= '03/'+str("%02d" % month)+'/'+str(year)
        txtMunicipio.send_keys(initmonth)
        
        #Select Date Fim
        txtMunicipio = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_txtDataAberturaFim')
        endmonth= '04/'+str("%02d" % month)+'/'+str(year)
        txtMunicipio.send_keys(endmonth)
        
        #Select all firms created (not only the active ones) "Mostrar somente empresas ativas"
        chkActive = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_chkAtivas').click()
        btPesquisar = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_btPesquisar')
        btPesquisar.click()
        seconds=10
        try:
            data_table = WebDriverWait(driver5,seconds).until(EC.presence_of_element_located((By.ID,'ctl00_cphContent_gdvResultadoBusca_gdvContent')))
              
            #Defining conditions for loop while month-year
            totalpageresult=0
            lastpageresult=2
            #In loop I'll redefine them, I just need them to be different, thats the condition to keep looping
            
            #While looping month-year
            while int(lastpageresult) != int(totalpageresult):
                #Scrape table from a page
                time.sleep(1)
                tabletemp = pd.read_html(driver5.find_element('xpath','//*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent"]').get_attribute('outerHTML'))[0]
                tabletemp = tabletemp.drop(tabletemp.columns[3], axis=1)
                tabletemp['Month']= str(month)
                tabletemp['Year'] = str(year)
                if type == "1":
                    tabletemp['Type']="Empresario"
                elif type == "2":
                    tabletemp['Type']="Sociedade Limitada"
                elif type == "3":
                    tabletemp['Type']="Sociedade por Acoes"
                elif type == "4":
                    tabletemp['Type']="Cooperativa"
                elif type == "5":
                    tabletemp['Type']="Consorcio"
                elif type == "6":
                    tabletemp['Type']="Grupo"
                elif type == "7":
                    tabletemp['Type']="Comandita Simple"
                elif type == "8":
                    tabletemp['Type']="Comandita por Acoes"
                elif type == "9":
                    tabletemp['Type']="Capital Industria"
                elif type == "10":
                    tabletemp['Type']="Solidaria"
                elif type == "11":
                    tabletemp['Type']="Armazens Gerais Ltda"
                elif type == "12":
                    tabletemp['Type']="Empresa Estrangeira"
                elif type == "13":
                    tabletemp['Type']="Binacional Ltda"
                elif type == "14":
                    tabletemp['Type']="Sociedade em Nome Coletivo"
                elif type == "15":
                    tabletemp['Type']="Empresa Publica"
                elif type == "16":
                    tabletemp['Type']="Subsidiaria Integral"
                elif type == "17":
                    tabletemp['Type']="Sociedade em Conta de Participacao"
                elif type == "18":
                    tabletemp['Type']="Armazens Gerais S/A"
                elif type == "19":
                    tabletemp['Type']="Binacional S/A"
                elif type == "21":
                    tabletemp['Type']="Armazens Gerais Empresario"
                else:
                    tabletemp['Type'] = "Outros"
                
                #Append this page to new table
                df = df.append(tabletemp)
                
                #Changing while condition
                #noninteresting, lastpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResults').text.replace('.',''))
                #totalpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResultCount').text.replace('.',''))[0]
                            
                #Click next page button
                try:
                    driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_btrNext_lbtText').click()
                    time.sleep(1)
                except: 
                    pass 
                #Changing while condition
                noninteresting, lastpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResults').text.replace('.',''))
                totalpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResultCount').text.replace('.',''))[0]
                
                print(f'Month {month} Year {year}, {lastpageresult} rows out of {totalpageresult}. Company Type "{type}"')
            
            #Scrape Last Page
            tabletemp = pd.read_html(driver5.find_element('xpath','//*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent"]').get_attribute('outerHTML'))[0]
            tabletemp = tabletemp.drop(tabletemp.columns[3], axis=1)
            tabletemp['Month']= str(month)
            tabletemp['Year'] = str(year)
            if type == "1":
                tabletemp['Type']="Empresario"
            elif type == "2":
                tabletemp['Type']="Sociedade Limitada"
            elif type == "3":
                tabletemp['Type']="Sociedade por Acoes"
            elif type == "4":
                tabletemp['Type']="Cooperativa"
            elif type == "5":
                tabletemp['Type']="Consorcio"
            elif type == "6":
                tabletemp['Type']="Grupo"
            elif type == "7":
                tabletemp['Type']="Comandita Simple"
            elif type == "8":
                tabletemp['Type']="Comandita por Acoes"
            elif type == "9":
                tabletemp['Type']="Capital Industria"
            elif type == "10":
                tabletemp['Type']="Solidaria"
            elif type == "11":
                tabletemp['Type']="Armazens Gerais Ltda"
            elif type == "12":
                tabletemp['Type']="Empresa Estrangeira"
            elif type == "13":
                tabletemp['Type']="Binacional Ltda"
            elif type == "14":
                tabletemp['Type']="Sociedade em Nome Coletivo"
            elif type == "15":
                tabletemp['Type']="Empresa Publica"
            elif type == "16":
                tabletemp['Type']="Subsidiaria Integral"
            elif type == "17":
                tabletemp['Type']="Sociedade em Conta de Participacao"
            elif type == "18":
                tabletemp['Type']="Armazens Gerais S/A"
            elif type == "19":
                tabletemp['Type']="Binacional S/A"
            elif type == "21":
                tabletemp['Type']="Armazens Gerais Empresario"
            else:
                tabletemp['Type'] = "Outros"
            
            
            #Append this page to new table
            df = df.append(tabletemp)
               
                
            #Scrape table from a LAST page
            #tabletemp = pd.read_html(driver5.find_element('xpath','//*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent"]').get_attribute('outerHTML'))[0]
            #tabletemp = tabletemp.drop(tabletemp.columns[3], axis=1)
            #tabletemp['Month']= str(month)
            #tabletemp['Year'] = str(year)
            
            #Append this LAST page to new table
            #df = df.append(tabletemp)
            
        except:
            pass
        
        #Get ready to introduce new captcha
        winsound.Beep(frequency, duration) #Makes a sound letting you know its time
        
        
        #First 10 days
        #Get Web Page
        driver5.get('https://www.jucesponline.sp.gov.br/BuscaAvancada.aspx?IDProduto=') #Open web page
        
            
        #Date variable - LAST DAY OF MONTH 
        _, last_day = calendar.monthrange(year, month)
        #Select Type
        txtTipo = Select(driver5.find_element("id",'ctl00_cphContent_frmBuscaAvancada_ddlTipoEmpresa')) #Select ID Tipo de Empresa
        txtTipo.select_by_value(type) #By value
        #txtTipo.select_by_visibleText("Empresário") #By text
        #txtTipo.select_by_index(1) #By index
        
        #Select Date Inicio
        txtMunicipio = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_txtDataAberturaInicio')
        initmonth= '05/'+str("%02d" % month)+'/'+str(year)
        txtMunicipio.send_keys(initmonth)
        
        #Select Date Fim
        txtMunicipio = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_txtDataAberturaFim')
        endmonth= '08/'+str("%02d" % month)+'/'+str(year)
        txtMunicipio.send_keys(endmonth)
        
        #Select all firms created (not only the active ones) "Mostrar somente empresas ativas"
        chkActive = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_chkAtivas').click()
        btPesquisar = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_btPesquisar')
        btPesquisar.click()
        seconds=10
        try:
            data_table = WebDriverWait(driver5,seconds).until(EC.presence_of_element_located((By.ID,'ctl00_cphContent_gdvResultadoBusca_gdvContent')))
              
            #Defining conditions for loop while month-year
            totalpageresult=0
            lastpageresult=2
            #In loop I'll redefine them, I just need them to be different, thats the condition to keep looping
            
            #While looping month-year
            while int(lastpageresult) != int(totalpageresult):
                #Scrape table from a page
                time.sleep(1)
                tabletemp = pd.read_html(driver5.find_element('xpath','//*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent"]').get_attribute('outerHTML'))[0]
                tabletemp = tabletemp.drop(tabletemp.columns[3], axis=1)
                tabletemp['Month']= str(month)
                tabletemp['Year'] = str(year)
                if type == "1":
                    tabletemp['Type']="Empresario"
                elif type == "2":
                    tabletemp['Type']="Sociedade Limitada"
                elif type == "3":
                    tabletemp['Type']="Sociedade por Acoes"
                elif type == "4":
                    tabletemp['Type']="Cooperativa"
                elif type == "5":
                    tabletemp['Type']="Consorcio"
                elif type == "6":
                    tabletemp['Type']="Grupo"
                elif type == "7":
                    tabletemp['Type']="Comandita Simple"
                elif type == "8":
                    tabletemp['Type']="Comandita por Acoes"
                elif type == "9":
                    tabletemp['Type']="Capital Industria"
                elif type == "10":
                    tabletemp['Type']="Solidaria"
                elif type == "11":
                    tabletemp['Type']="Armazens Gerais Ltda"
                elif type == "12":
                    tabletemp['Type']="Empresa Estrangeira"
                elif type == "13":
                    tabletemp['Type']="Binacional Ltda"
                elif type == "14":
                    tabletemp['Type']="Sociedade em Nome Coletivo"
                elif type == "15":
                    tabletemp['Type']="Empresa Publica"
                elif type == "16":
                    tabletemp['Type']="Subsidiaria Integral"
                elif type == "17":
                    tabletemp['Type']="Sociedade em Conta de Participacao"
                elif type == "18":
                    tabletemp['Type']="Armazens Gerais S/A"
                elif type == "19":
                    tabletemp['Type']="Binacional S/A"
                elif type == "21":
                    tabletemp['Type']="Armazens Gerais Empresario"
                else:
                    tabletemp['Type'] = "Outros"
                
                #Append this page to new table
                df = df.append(tabletemp)
                
                #Changing while condition
                #noninteresting, lastpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResults').text.replace('.',''))
                #totalpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResultCount').text.replace('.',''))[0]
                            
                #Click next page button
                try:
                    driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_btrNext_lbtText').click()
                    time.sleep(1)
                except: 
                    pass 
                #Changing while condition
                noninteresting, lastpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResults').text.replace('.',''))
                totalpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResultCount').text.replace('.',''))[0]
                
                print(f'Month {month} Year {year}, {lastpageresult} rows out of {totalpageresult}. Company Type "{type}"')
            
            #Scrape Last Page
            tabletemp = pd.read_html(driver5.find_element('xpath','//*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent"]').get_attribute('outerHTML'))[0]
            tabletemp = tabletemp.drop(tabletemp.columns[3], axis=1)
            tabletemp['Month']= str(month)
            tabletemp['Year'] = str(year)
            if type == "1":
                tabletemp['Type']="Empresario"
            elif type == "2":
                tabletemp['Type']="Sociedade Limitada"
            elif type == "3":
                tabletemp['Type']="Sociedade por Acoes"
            elif type == "4":
                tabletemp['Type']="Cooperativa"
            elif type == "5":
                tabletemp['Type']="Consorcio"
            elif type == "6":
                tabletemp['Type']="Grupo"
            elif type == "7":
                tabletemp['Type']="Comandita Simple"
            elif type == "8":
                tabletemp['Type']="Comandita por Acoes"
            elif type == "9":
                tabletemp['Type']="Capital Industria"
            elif type == "10":
                tabletemp['Type']="Solidaria"
            elif type == "11":
                tabletemp['Type']="Armazens Gerais Ltda"
            elif type == "12":
                tabletemp['Type']="Empresa Estrangeira"
            elif type == "13":
                tabletemp['Type']="Binacional Ltda"
            elif type == "14":
                tabletemp['Type']="Sociedade em Nome Coletivo"
            elif type == "15":
                tabletemp['Type']="Empresa Publica"
            elif type == "16":
                tabletemp['Type']="Subsidiaria Integral"
            elif type == "17":
                tabletemp['Type']="Sociedade em Conta de Participacao"
            elif type == "18":
                tabletemp['Type']="Armazens Gerais S/A"
            elif type == "19":
                tabletemp['Type']="Binacional S/A"
            elif type == "21":
                tabletemp['Type']="Armazens Gerais Empresario"
            else:
                tabletemp['Type'] = "Outros"
            
            
            #Append this page to new table
            df = df.append(tabletemp)
               
                
            #Scrape table from a LAST page
            #tabletemp = pd.read_html(driver5.find_element('xpath','//*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent"]').get_attribute('outerHTML'))[0]
            #tabletemp = tabletemp.drop(tabletemp.columns[3], axis=1)
            #tabletemp['Month']= str(month)
            #tabletemp['Year'] = str(year)
            
            #Append this LAST page to new table
            #df = df.append(tabletemp)
            
        except:
            pass
        
        #Get ready to introduce new captcha
        winsound.Beep(frequency, duration) #Makes a sound letting you know its time
        
        
        #First 10 days
        #Get Web Page
        driver5.get('https://www.jucesponline.sp.gov.br/BuscaAvancada.aspx?IDProduto=') #Open web page
        
            
        #Date variable - LAST DAY OF MONTH 
        _, last_day = calendar.monthrange(year, month)
        #Select Type
        txtTipo = Select(driver5.find_element("id",'ctl00_cphContent_frmBuscaAvancada_ddlTipoEmpresa')) #Select ID Tipo de Empresa
        txtTipo.select_by_value(type) #By value
        #txtTipo.select_by_visibleText("Empresário") #By text
        #txtTipo.select_by_index(1) #By index
        
        #Select Date Inicio
        txtMunicipio = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_txtDataAberturaInicio')
        initmonth= '09/'+str("%02d" % month)+'/'+str(year)
        txtMunicipio.send_keys(initmonth)
        
        #Select Date Fim
        txtMunicipio = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_txtDataAberturaFim')
        endmonth= '13/'+str("%02d" % month)+'/'+str(year)
        txtMunicipio.send_keys(endmonth)
        
        #Select all firms created (not only the active ones) "Mostrar somente empresas ativas"
        chkActive = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_chkAtivas').click()
        btPesquisar = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_btPesquisar')
        btPesquisar.click()
        seconds=10
        try:
            data_table = WebDriverWait(driver5,seconds).until(EC.presence_of_element_located((By.ID,'ctl00_cphContent_gdvResultadoBusca_gdvContent')))
              
            #Defining conditions for loop while month-year
            totalpageresult=0
            lastpageresult=2
            #In loop I'll redefine them, I just need them to be different, thats the condition to keep looping
            
            #While looping month-year
            while int(lastpageresult) != int(totalpageresult):
                #Scrape table from a page
                time.sleep(1)
                tabletemp = pd.read_html(driver5.find_element('xpath','//*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent"]').get_attribute('outerHTML'))[0]
                tabletemp = tabletemp.drop(tabletemp.columns[3], axis=1)
                tabletemp['Month']= str(month)
                tabletemp['Year'] = str(year)
                if type == "1":
                    tabletemp['Type']="Empresario"
                elif type == "2":
                    tabletemp['Type']="Sociedade Limitada"
                elif type == "3":
                    tabletemp['Type']="Sociedade por Acoes"
                elif type == "4":
                    tabletemp['Type']="Cooperativa"
                elif type == "5":
                    tabletemp['Type']="Consorcio"
                elif type == "6":
                    tabletemp['Type']="Grupo"
                elif type == "7":
                    tabletemp['Type']="Comandita Simple"
                elif type == "8":
                    tabletemp['Type']="Comandita por Acoes"
                elif type == "9":
                    tabletemp['Type']="Capital Industria"
                elif type == "10":
                    tabletemp['Type']="Solidaria"
                elif type == "11":
                    tabletemp['Type']="Armazens Gerais Ltda"
                elif type == "12":
                    tabletemp['Type']="Empresa Estrangeira"
                elif type == "13":
                    tabletemp['Type']="Binacional Ltda"
                elif type == "14":
                    tabletemp['Type']="Sociedade em Nome Coletivo"
                elif type == "15":
                    tabletemp['Type']="Empresa Publica"
                elif type == "16":
                    tabletemp['Type']="Subsidiaria Integral"
                elif type == "17":
                    tabletemp['Type']="Sociedade em Conta de Participacao"
                elif type == "18":
                    tabletemp['Type']="Armazens Gerais S/A"
                elif type == "19":
                    tabletemp['Type']="Binacional S/A"
                elif type == "21":
                    tabletemp['Type']="Armazens Gerais Empresario"
                else:
                    tabletemp['Type'] = "Outros"
                
                #Append this page to new table
                df = df.append(tabletemp)
                
                #Changing while condition
                #noninteresting, lastpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResults').text.replace('.',''))
                #totalpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResultCount').text.replace('.',''))[0]
                            
                #Click next page button
                try:
                    driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_btrNext_lbtText').click()
                    time.sleep(1)
                except: 
                    pass 
                #Changing while condition
                noninteresting, lastpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResults').text.replace('.',''))
                totalpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResultCount').text.replace('.',''))[0]
                
                print(f'Month {month} Year {year}, {lastpageresult} rows out of {totalpageresult}. Company Type "{type}"')
            
            #Scrape Last Page
            tabletemp = pd.read_html(driver5.find_element('xpath','//*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent"]').get_attribute('outerHTML'))[0]
            tabletemp = tabletemp.drop(tabletemp.columns[3], axis=1)
            tabletemp['Month']= str(month)
            tabletemp['Year'] = str(year)
            if type == "1":
                tabletemp['Type']="Empresario"
            elif type == "2":
                tabletemp['Type']="Sociedade Limitada"
            elif type == "3":
                tabletemp['Type']="Sociedade por Acoes"
            elif type == "4":
                tabletemp['Type']="Cooperativa"
            elif type == "5":
                tabletemp['Type']="Consorcio"
            elif type == "6":
                tabletemp['Type']="Grupo"
            elif type == "7":
                tabletemp['Type']="Comandita Simple"
            elif type == "8":
                tabletemp['Type']="Comandita por Acoes"
            elif type == "9":
                tabletemp['Type']="Capital Industria"
            elif type == "10":
                tabletemp['Type']="Solidaria"
            elif type == "11":
                tabletemp['Type']="Armazens Gerais Ltda"
            elif type == "12":
                tabletemp['Type']="Empresa Estrangeira"
            elif type == "13":
                tabletemp['Type']="Binacional Ltda"
            elif type == "14":
                tabletemp['Type']="Sociedade em Nome Coletivo"
            elif type == "15":
                tabletemp['Type']="Empresa Publica"
            elif type == "16":
                tabletemp['Type']="Subsidiaria Integral"
            elif type == "17":
                tabletemp['Type']="Sociedade em Conta de Participacao"
            elif type == "18":
                tabletemp['Type']="Armazens Gerais S/A"
            elif type == "19":
                tabletemp['Type']="Binacional S/A"
            elif type == "21":
                tabletemp['Type']="Armazens Gerais Empresario"
            else:
                tabletemp['Type'] = "Outros"
            
            
            #Append this page to new table
            df = df.append(tabletemp)
               
                
            #Scrape table from a LAST page
            #tabletemp = pd.read_html(driver5.find_element('xpath','//*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent"]').get_attribute('outerHTML'))[0]
            #tabletemp = tabletemp.drop(tabletemp.columns[3], axis=1)
            #tabletemp['Month']= str(month)
            #tabletemp['Year'] = str(year)
            
            #Append this LAST page to new table
            #df = df.append(tabletemp)
            
        except:
            pass
        
        #Get ready to introduce new captcha
        winsound.Beep(frequency, duration) #Makes a sound letting you know its time
        
        
        #First 10 days
        #Get Web Page
        driver5.get('https://www.jucesponline.sp.gov.br/BuscaAvancada.aspx?IDProduto=') #Open web page
        
            
        #Date variable - LAST DAY OF MONTH 
        _, last_day = calendar.monthrange(year, month)
        #Select Type
        txtTipo = Select(driver5.find_element("id",'ctl00_cphContent_frmBuscaAvancada_ddlTipoEmpresa')) #Select ID Tipo de Empresa
        txtTipo.select_by_value(type) #By value
        #txtTipo.select_by_visibleText("Empresário") #By text
        #txtTipo.select_by_index(1) #By index
        
        #Select Date Inicio
        txtMunicipio = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_txtDataAberturaInicio')
        initmonth= '14/'+str("%02d" % month)+'/'+str(year)
        txtMunicipio.send_keys(initmonth)
        
        #Select Date Fim
        txtMunicipio = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_txtDataAberturaFim')
        endmonth= '16/'+str("%02d" % month)+'/'+str(year)
        txtMunicipio.send_keys(endmonth)
        
        #Select all firms created (not only the active ones) "Mostrar somente empresas ativas"
        chkActive = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_chkAtivas').click()
        btPesquisar = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_btPesquisar')
        btPesquisar.click()
        seconds=10
        try:
            data_table = WebDriverWait(driver5,seconds).until(EC.presence_of_element_located((By.ID,'ctl00_cphContent_gdvResultadoBusca_gdvContent')))
              
            #Defining conditions for loop while month-year
            totalpageresult=0
            lastpageresult=2
            #In loop I'll redefine them, I just need them to be different, thats the condition to keep looping
            
            #While looping month-year
            while int(lastpageresult) != int(totalpageresult):
                #Scrape table from a page
                time.sleep(1)
                tabletemp = pd.read_html(driver5.find_element('xpath','//*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent"]').get_attribute('outerHTML'))[0]
                tabletemp = tabletemp.drop(tabletemp.columns[3], axis=1)
                tabletemp['Month']= str(month)
                tabletemp['Year'] = str(year)
                if type == "1":
                    tabletemp['Type']="Empresario"
                elif type == "2":
                    tabletemp['Type']="Sociedade Limitada"
                elif type == "3":
                    tabletemp['Type']="Sociedade por Acoes"
                elif type == "4":
                    tabletemp['Type']="Cooperativa"
                elif type == "5":
                    tabletemp['Type']="Consorcio"
                elif type == "6":
                    tabletemp['Type']="Grupo"
                elif type == "7":
                    tabletemp['Type']="Comandita Simple"
                elif type == "8":
                    tabletemp['Type']="Comandita por Acoes"
                elif type == "9":
                    tabletemp['Type']="Capital Industria"
                elif type == "10":
                    tabletemp['Type']="Solidaria"
                elif type == "11":
                    tabletemp['Type']="Armazens Gerais Ltda"
                elif type == "12":
                    tabletemp['Type']="Empresa Estrangeira"
                elif type == "13":
                    tabletemp['Type']="Binacional Ltda"
                elif type == "14":
                    tabletemp['Type']="Sociedade em Nome Coletivo"
                elif type == "15":
                    tabletemp['Type']="Empresa Publica"
                elif type == "16":
                    tabletemp['Type']="Subsidiaria Integral"
                elif type == "17":
                    tabletemp['Type']="Sociedade em Conta de Participacao"
                elif type == "18":
                    tabletemp['Type']="Armazens Gerais S/A"
                elif type == "19":
                    tabletemp['Type']="Binacional S/A"
                elif type == "21":
                    tabletemp['Type']="Armazens Gerais Empresario"
                else:
                    tabletemp['Type'] = "Outros"
                
                #Append this page to new table
                df = df.append(tabletemp)
                
                #Changing while condition
                #noninteresting, lastpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResults').text.replace('.',''))
                #totalpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResultCount').text.replace('.',''))[0]
                            
                #Click next page button
                try:
                    driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_btrNext_lbtText').click()
                    time.sleep(1)
                except: 
                    pass 
                #Changing while condition
                noninteresting, lastpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResults').text.replace('.',''))
                totalpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResultCount').text.replace('.',''))[0]
                
                print(f'Month {month} Year {year}, {lastpageresult} rows out of {totalpageresult}. Company Type "{type}"')
            
            #Scrape Last Page
            tabletemp = pd.read_html(driver5.find_element('xpath','//*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent"]').get_attribute('outerHTML'))[0]
            tabletemp = tabletemp.drop(tabletemp.columns[3], axis=1)
            tabletemp['Month']= str(month)
            tabletemp['Year'] = str(year)
            if type == "1":
                tabletemp['Type']="Empresario"
            elif type == "2":
                tabletemp['Type']="Sociedade Limitada"
            elif type == "3":
                tabletemp['Type']="Sociedade por Acoes"
            elif type == "4":
                tabletemp['Type']="Cooperativa"
            elif type == "5":
                tabletemp['Type']="Consorcio"
            elif type == "6":
                tabletemp['Type']="Grupo"
            elif type == "7":
                tabletemp['Type']="Comandita Simple"
            elif type == "8":
                tabletemp['Type']="Comandita por Acoes"
            elif type == "9":
                tabletemp['Type']="Capital Industria"
            elif type == "10":
                tabletemp['Type']="Solidaria"
            elif type == "11":
                tabletemp['Type']="Armazens Gerais Ltda"
            elif type == "12":
                tabletemp['Type']="Empresa Estrangeira"
            elif type == "13":
                tabletemp['Type']="Binacional Ltda"
            elif type == "14":
                tabletemp['Type']="Sociedade em Nome Coletivo"
            elif type == "15":
                tabletemp['Type']="Empresa Publica"
            elif type == "16":
                tabletemp['Type']="Subsidiaria Integral"
            elif type == "17":
                tabletemp['Type']="Sociedade em Conta de Participacao"
            elif type == "18":
                tabletemp['Type']="Armazens Gerais S/A"
            elif type == "19":
                tabletemp['Type']="Binacional S/A"
            elif type == "21":
                tabletemp['Type']="Armazens Gerais Empresario"
            else:
                tabletemp['Type'] = "Outros"
            
            
            #Append this page to new table
            df = df.append(tabletemp)
               
                
            #Scrape table from a LAST page
            #tabletemp = pd.read_html(driver5.find_element('xpath','//*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent"]').get_attribute('outerHTML'))[0]
            #tabletemp = tabletemp.drop(tabletemp.columns[3], axis=1)
            #tabletemp['Month']= str(month)
            #tabletemp['Year'] = str(year)
            
            #Append this LAST page to new table
            #df = df.append(tabletemp)
            
        except:
            pass
        
        #Get ready to introduce new captcha
        winsound.Beep(frequency, duration) #Makes a sound letting you know its time
        
        
        #First 10 days
        #Get Web Page
        driver5.get('https://www.jucesponline.sp.gov.br/BuscaAvancada.aspx?IDProduto=') #Open web page
        
            
        #Date variable - LAST DAY OF MONTH 
        _, last_day = calendar.monthrange(year, month)
        #Select Type
        txtTipo = Select(driver5.find_element("id",'ctl00_cphContent_frmBuscaAvancada_ddlTipoEmpresa')) #Select ID Tipo de Empresa
        txtTipo.select_by_value(type) #By value
        #txtTipo.select_by_visibleText("Empresário") #By text
        #txtTipo.select_by_index(1) #By index
        
        #Select Date Inicio
        txtMunicipio = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_txtDataAberturaInicio')
        initmonth= '17/'+str("%02d" % month)+'/'+str(year)
        txtMunicipio.send_keys(initmonth)
        
        #Select Date Fim
        txtMunicipio = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_txtDataAberturaFim')
        endmonth= '19/'+str("%02d" % month)+'/'+str(year)
        txtMunicipio.send_keys(endmonth)
        
        #Select all firms created (not only the active ones) "Mostrar somente empresas ativas"
        chkActive = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_chkAtivas').click()
        btPesquisar = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_btPesquisar')
        btPesquisar.click()
        seconds=10
        try:
            data_table = WebDriverWait(driver5,seconds).until(EC.presence_of_element_located((By.ID,'ctl00_cphContent_gdvResultadoBusca_gdvContent')))
              
            #Defining conditions for loop while month-year
            totalpageresult=0
            lastpageresult=2
            #In loop I'll redefine them, I just need them to be different, thats the condition to keep looping
            
            #While looping month-year
            while int(lastpageresult) != int(totalpageresult):
                #Scrape table from a page
                time.sleep(1)
                tabletemp = pd.read_html(driver5.find_element('xpath','//*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent"]').get_attribute('outerHTML'))[0]
                tabletemp = tabletemp.drop(tabletemp.columns[3], axis=1)
                tabletemp['Month']= str(month)
                tabletemp['Year'] = str(year)
                if type == "1":
                    tabletemp['Type']="Empresario"
                elif type == "2":
                    tabletemp['Type']="Sociedade Limitada"
                elif type == "3":
                    tabletemp['Type']="Sociedade por Acoes"
                elif type == "4":
                    tabletemp['Type']="Cooperativa"
                elif type == "5":
                    tabletemp['Type']="Consorcio"
                elif type == "6":
                    tabletemp['Type']="Grupo"
                elif type == "7":
                    tabletemp['Type']="Comandita Simple"
                elif type == "8":
                    tabletemp['Type']="Comandita por Acoes"
                elif type == "9":
                    tabletemp['Type']="Capital Industria"
                elif type == "10":
                    tabletemp['Type']="Solidaria"
                elif type == "11":
                    tabletemp['Type']="Armazens Gerais Ltda"
                elif type == "12":
                    tabletemp['Type']="Empresa Estrangeira"
                elif type == "13":
                    tabletemp['Type']="Binacional Ltda"
                elif type == "14":
                    tabletemp['Type']="Sociedade em Nome Coletivo"
                elif type == "15":
                    tabletemp['Type']="Empresa Publica"
                elif type == "16":
                    tabletemp['Type']="Subsidiaria Integral"
                elif type == "17":
                    tabletemp['Type']="Sociedade em Conta de Participacao"
                elif type == "18":
                    tabletemp['Type']="Armazens Gerais S/A"
                elif type == "19":
                    tabletemp['Type']="Binacional S/A"
                elif type == "21":
                    tabletemp['Type']="Armazens Gerais Empresario"
                else:
                    tabletemp['Type'] = "Outros"
                
                #Append this page to new table
                df = df.append(tabletemp)
                
                #Changing while condition
                #noninteresting, lastpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResults').text.replace('.',''))
                #totalpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResultCount').text.replace('.',''))[0]
                            
                #Click next page button
                try:
                    driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_btrNext_lbtText').click()
                    time.sleep(1)
                except: 
                    pass 
                #Changing while condition
                noninteresting, lastpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResults').text.replace('.',''))
                totalpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResultCount').text.replace('.',''))[0]
                
                print(f'Month {month} Year {year}, {lastpageresult} rows out of {totalpageresult}. Company Type "{type}"')
            
            #Scrape Last Page
            tabletemp = pd.read_html(driver5.find_element('xpath','//*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent"]').get_attribute('outerHTML'))[0]
            tabletemp = tabletemp.drop(tabletemp.columns[3], axis=1)
            tabletemp['Month']= str(month)
            tabletemp['Year'] = str(year)
            if type == "1":
                tabletemp['Type']="Empresario"
            elif type == "2":
                tabletemp['Type']="Sociedade Limitada"
            elif type == "3":
                tabletemp['Type']="Sociedade por Acoes"
            elif type == "4":
                tabletemp['Type']="Cooperativa"
            elif type == "5":
                tabletemp['Type']="Consorcio"
            elif type == "6":
                tabletemp['Type']="Grupo"
            elif type == "7":
                tabletemp['Type']="Comandita Simple"
            elif type == "8":
                tabletemp['Type']="Comandita por Acoes"
            elif type == "9":
                tabletemp['Type']="Capital Industria"
            elif type == "10":
                tabletemp['Type']="Solidaria"
            elif type == "11":
                tabletemp['Type']="Armazens Gerais Ltda"
            elif type == "12":
                tabletemp['Type']="Empresa Estrangeira"
            elif type == "13":
                tabletemp['Type']="Binacional Ltda"
            elif type == "14":
                tabletemp['Type']="Sociedade em Nome Coletivo"
            elif type == "15":
                tabletemp['Type']="Empresa Publica"
            elif type == "16":
                tabletemp['Type']="Subsidiaria Integral"
            elif type == "17":
                tabletemp['Type']="Sociedade em Conta de Participacao"
            elif type == "18":
                tabletemp['Type']="Armazens Gerais S/A"
            elif type == "19":
                tabletemp['Type']="Binacional S/A"
            elif type == "21":
                tabletemp['Type']="Armazens Gerais Empresario"
            else:
                tabletemp['Type'] = "Outros"
            
            
            #Append this page to new table
            df = df.append(tabletemp)
               
                
            #Scrape table from a LAST page
            #tabletemp = pd.read_html(driver5.find_element('xpath','//*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent"]').get_attribute('outerHTML'))[0]
            #tabletemp = tabletemp.drop(tabletemp.columns[3], axis=1)
            #tabletemp['Month']= str(month)
            #tabletemp['Year'] = str(year)
            
            #Append this LAST page to new table
            #df = df.append(tabletemp)
            
        except:
            pass
        
        #Get ready to introduce new captcha
        winsound.Beep(frequency, duration) #Makes a sound letting you know its time
        
        #First 10 days
        #Get Web Page
        driver5.get('https://www.jucesponline.sp.gov.br/BuscaAvancada.aspx?IDProduto=') #Open web page
        
            
        #Date variable - LAST DAY OF MONTH 
        _, last_day = calendar.monthrange(year, month)
        #Select Type
        txtTipo = Select(driver5.find_element("id",'ctl00_cphContent_frmBuscaAvancada_ddlTipoEmpresa')) #Select ID Tipo de Empresa
        txtTipo.select_by_value(type) #By value
        #txtTipo.select_by_visibleText("Empresário") #By text
        #txtTipo.select_by_index(1) #By index
        
        #Select Date Inicio
        txtMunicipio = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_txtDataAberturaInicio')
        initmonth= '20/'+str("%02d" % month)+'/'+str(year)
        txtMunicipio.send_keys(initmonth)
        
        #Select Date Fim
        txtMunicipio = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_txtDataAberturaFim')
        endmonth= '22/'+str("%02d" % month)+'/'+str(year)
        txtMunicipio.send_keys(endmonth)
        
        #Select all firms created (not only the active ones) "Mostrar somente empresas ativas"
        chkActive = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_chkAtivas').click()
        btPesquisar = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_btPesquisar')
        btPesquisar.click()
        seconds=10
        try:
            data_table = WebDriverWait(driver5,seconds).until(EC.presence_of_element_located((By.ID,'ctl00_cphContent_gdvResultadoBusca_gdvContent')))
              
            #Defining conditions for loop while month-year
            totalpageresult=0
            lastpageresult=2
            #In loop I'll redefine them, I just need them to be different, thats the condition to keep looping
            
            #While looping month-year
            while int(lastpageresult) != int(totalpageresult):
                #Scrape table from a page
                time.sleep(1)
                tabletemp = pd.read_html(driver5.find_element('xpath','//*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent"]').get_attribute('outerHTML'))[0]
                tabletemp = tabletemp.drop(tabletemp.columns[3], axis=1)
                tabletemp['Month']= str(month)
                tabletemp['Year'] = str(year)
                if type == "1":
                    tabletemp['Type']="Empresario"
                elif type == "2":
                    tabletemp['Type']="Sociedade Limitada"
                elif type == "3":
                    tabletemp['Type']="Sociedade por Acoes"
                elif type == "4":
                    tabletemp['Type']="Cooperativa"
                elif type == "5":
                    tabletemp['Type']="Consorcio"
                elif type == "6":
                    tabletemp['Type']="Grupo"
                elif type == "7":
                    tabletemp['Type']="Comandita Simple"
                elif type == "8":
                    tabletemp['Type']="Comandita por Acoes"
                elif type == "9":
                    tabletemp['Type']="Capital Industria"
                elif type == "10":
                    tabletemp['Type']="Solidaria"
                elif type == "11":
                    tabletemp['Type']="Armazens Gerais Ltda"
                elif type == "12":
                    tabletemp['Type']="Empresa Estrangeira"
                elif type == "13":
                    tabletemp['Type']="Binacional Ltda"
                elif type == "14":
                    tabletemp['Type']="Sociedade em Nome Coletivo"
                elif type == "15":
                    tabletemp['Type']="Empresa Publica"
                elif type == "16":
                    tabletemp['Type']="Subsidiaria Integral"
                elif type == "17":
                    tabletemp['Type']="Sociedade em Conta de Participacao"
                elif type == "18":
                    tabletemp['Type']="Armazens Gerais S/A"
                elif type == "19":
                    tabletemp['Type']="Binacional S/A"
                elif type == "21":
                    tabletemp['Type']="Armazens Gerais Empresario"
                else:
                    tabletemp['Type'] = "Outros"
                
                #Append this page to new table
                df = df.append(tabletemp)
                
                #Changing while condition
                #noninteresting, lastpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResults').text.replace('.',''))
                #totalpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResultCount').text.replace('.',''))[0]
                            
                #Click next page button
                try:
                    driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_btrNext_lbtText').click()
                    time.sleep(1)
                except: 
                    pass 
                #Changing while condition
                noninteresting, lastpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResults').text.replace('.',''))
                totalpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResultCount').text.replace('.',''))[0]
                
                print(f'Month {month} Year {year}, {lastpageresult} rows out of {totalpageresult}. Company Type "{type}"')
            
            #Scrape Last Page
            tabletemp = pd.read_html(driver5.find_element('xpath','//*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent"]').get_attribute('outerHTML'))[0]
            tabletemp = tabletemp.drop(tabletemp.columns[3], axis=1)
            tabletemp['Month']= str(month)
            tabletemp['Year'] = str(year)
            if type == "1":
                tabletemp['Type']="Empresario"
            elif type == "2":
                tabletemp['Type']="Sociedade Limitada"
            elif type == "3":
                tabletemp['Type']="Sociedade por Acoes"
            elif type == "4":
                tabletemp['Type']="Cooperativa"
            elif type == "5":
                tabletemp['Type']="Consorcio"
            elif type == "6":
                tabletemp['Type']="Grupo"
            elif type == "7":
                tabletemp['Type']="Comandita Simple"
            elif type == "8":
                tabletemp['Type']="Comandita por Acoes"
            elif type == "9":
                tabletemp['Type']="Capital Industria"
            elif type == "10":
                tabletemp['Type']="Solidaria"
            elif type == "11":
                tabletemp['Type']="Armazens Gerais Ltda"
            elif type == "12":
                tabletemp['Type']="Empresa Estrangeira"
            elif type == "13":
                tabletemp['Type']="Binacional Ltda"
            elif type == "14":
                tabletemp['Type']="Sociedade em Nome Coletivo"
            elif type == "15":
                tabletemp['Type']="Empresa Publica"
            elif type == "16":
                tabletemp['Type']="Subsidiaria Integral"
            elif type == "17":
                tabletemp['Type']="Sociedade em Conta de Participacao"
            elif type == "18":
                tabletemp['Type']="Armazens Gerais S/A"
            elif type == "19":
                tabletemp['Type']="Binacional S/A"
            elif type == "21":
                tabletemp['Type']="Armazens Gerais Empresario"
            else:
                tabletemp['Type'] = "Outros"
            
            
            #Append this page to new table
            df = df.append(tabletemp)
               
                
            #Scrape table from a LAST page
            #tabletemp = pd.read_html(driver5.find_element('xpath','//*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent"]').get_attribute('outerHTML'))[0]
            #tabletemp = tabletemp.drop(tabletemp.columns[3], axis=1)
            #tabletemp['Month']= str(month)
            #tabletemp['Year'] = str(year)
            
            #Append this LAST page to new table
            #df = df.append(tabletemp)
            
        except:
            pass
        
        #Get ready to introduce new captcha
        winsound.Beep(frequency, duration) #Makes a sound letting you know its time
        
        
        #First 10 days
        #Get Web Page
        driver5.get('https://www.jucesponline.sp.gov.br/BuscaAvancada.aspx?IDProduto=') #Open web page
        
            
        #Date variable - LAST DAY OF MONTH 
        _, last_day = calendar.monthrange(year, month)
        #Select Type
        txtTipo = Select(driver5.find_element("id",'ctl00_cphContent_frmBuscaAvancada_ddlTipoEmpresa')) #Select ID Tipo de Empresa
        txtTipo.select_by_value(type) #By value
        #txtTipo.select_by_visibleText("Empresário") #By text
        #txtTipo.select_by_index(1) #By index
        
        #Select Date Inicio
        txtMunicipio = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_txtDataAberturaInicio')
        initmonth= '23/'+str("%02d" % month)+'/'+str(year)
        txtMunicipio.send_keys(initmonth)
        
        #Select Date Fim
        txtMunicipio = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_txtDataAberturaFim')
        endmonth= '24/'+str("%02d" % month)+'/'+str(year)
        txtMunicipio.send_keys(endmonth)
        
        #Select all firms created (not only the active ones) "Mostrar somente empresas ativas"
        chkActive = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_chkAtivas').click()
        btPesquisar = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_btPesquisar')
        btPesquisar.click()
        seconds=10
        try:
            data_table = WebDriverWait(driver5,seconds).until(EC.presence_of_element_located((By.ID,'ctl00_cphContent_gdvResultadoBusca_gdvContent')))
              
            #Defining conditions for loop while month-year
            totalpageresult=0
            lastpageresult=2
            #In loop I'll redefine them, I just need them to be different, thats the condition to keep looping
            
            #While looping month-year
            while int(lastpageresult) != int(totalpageresult):
                #Scrape table from a page
                time.sleep(1)
                tabletemp = pd.read_html(driver5.find_element('xpath','//*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent"]').get_attribute('outerHTML'))[0]
                tabletemp = tabletemp.drop(tabletemp.columns[3], axis=1)
                tabletemp['Month']= str(month)
                tabletemp['Year'] = str(year)
                if type == "1":
                    tabletemp['Type']="Empresario"
                elif type == "2":
                    tabletemp['Type']="Sociedade Limitada"
                elif type == "3":
                    tabletemp['Type']="Sociedade por Acoes"
                elif type == "4":
                    tabletemp['Type']="Cooperativa"
                elif type == "5":
                    tabletemp['Type']="Consorcio"
                elif type == "6":
                    tabletemp['Type']="Grupo"
                elif type == "7":
                    tabletemp['Type']="Comandita Simple"
                elif type == "8":
                    tabletemp['Type']="Comandita por Acoes"
                elif type == "9":
                    tabletemp['Type']="Capital Industria"
                elif type == "10":
                    tabletemp['Type']="Solidaria"
                elif type == "11":
                    tabletemp['Type']="Armazens Gerais Ltda"
                elif type == "12":
                    tabletemp['Type']="Empresa Estrangeira"
                elif type == "13":
                    tabletemp['Type']="Binacional Ltda"
                elif type == "14":
                    tabletemp['Type']="Sociedade em Nome Coletivo"
                elif type == "15":
                    tabletemp['Type']="Empresa Publica"
                elif type == "16":
                    tabletemp['Type']="Subsidiaria Integral"
                elif type == "17":
                    tabletemp['Type']="Sociedade em Conta de Participacao"
                elif type == "18":
                    tabletemp['Type']="Armazens Gerais S/A"
                elif type == "19":
                    tabletemp['Type']="Binacional S/A"
                elif type == "21":
                    tabletemp['Type']="Armazens Gerais Empresario"
                else:
                    tabletemp['Type'] = "Outros"
                
                #Append this page to new table
                df = df.append(tabletemp)
                
                #Changing while condition
                #noninteresting, lastpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResults').text.replace('.',''))
                #totalpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResultCount').text.replace('.',''))[0]
                            
                #Click next page button
                try:
                    driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_btrNext_lbtText').click()
                    time.sleep(1)
                except: 
                    pass 
                #Changing while condition
                noninteresting, lastpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResults').text.replace('.',''))
                totalpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResultCount').text.replace('.',''))[0]
                
                print(f'Month {month} Year {year}, {lastpageresult} rows out of {totalpageresult}. Company Type "{type}"')
            
            #Scrape Last Page
            tabletemp = pd.read_html(driver5.find_element('xpath','//*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent"]').get_attribute('outerHTML'))[0]
            tabletemp = tabletemp.drop(tabletemp.columns[3], axis=1)
            tabletemp['Month']= str(month)
            tabletemp['Year'] = str(year)
            if type == "1":
                tabletemp['Type']="Empresario"
            elif type == "2":
                tabletemp['Type']="Sociedade Limitada"
            elif type == "3":
                tabletemp['Type']="Sociedade por Acoes"
            elif type == "4":
                tabletemp['Type']="Cooperativa"
            elif type == "5":
                tabletemp['Type']="Consorcio"
            elif type == "6":
                tabletemp['Type']="Grupo"
            elif type == "7":
                tabletemp['Type']="Comandita Simple"
            elif type == "8":
                tabletemp['Type']="Comandita por Acoes"
            elif type == "9":
                tabletemp['Type']="Capital Industria"
            elif type == "10":
                tabletemp['Type']="Solidaria"
            elif type == "11":
                tabletemp['Type']="Armazens Gerais Ltda"
            elif type == "12":
                tabletemp['Type']="Empresa Estrangeira"
            elif type == "13":
                tabletemp['Type']="Binacional Ltda"
            elif type == "14":
                tabletemp['Type']="Sociedade em Nome Coletivo"
            elif type == "15":
                tabletemp['Type']="Empresa Publica"
            elif type == "16":
                tabletemp['Type']="Subsidiaria Integral"
            elif type == "17":
                tabletemp['Type']="Sociedade em Conta de Participacao"
            elif type == "18":
                tabletemp['Type']="Armazens Gerais S/A"
            elif type == "19":
                tabletemp['Type']="Binacional S/A"
            elif type == "21":
                tabletemp['Type']="Armazens Gerais Empresario"
            else:
                tabletemp['Type'] = "Outros"
            
            
            #Append this page to new table
            df = df.append(tabletemp)
               
                
            #Scrape table from a LAST page
            #tabletemp = pd.read_html(driver5.find_element('xpath','//*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent"]').get_attribute('outerHTML'))[0]
            #tabletemp = tabletemp.drop(tabletemp.columns[3], axis=1)
            #tabletemp['Month']= str(month)
            #tabletemp['Year'] = str(year)
            
            #Append this LAST page to new table
            #df = df.append(tabletemp)
            
        except:
            pass
        
        #Get ready to introduce new captcha
        winsound.Beep(frequency, duration) #Makes a sound letting you know its time
        
        #Middle 10 days
        #Get Web Page
        driver5.get('https://www.jucesponline.sp.gov.br/BuscaAvancada.aspx?IDProduto=') #Open web page
        
            
        #Date variable - LAST DAY OF MONTH 
        _, last_day = calendar.monthrange(year, month)
        #Select Type
        txtTipo = Select(driver5.find_element("id",'ctl00_cphContent_frmBuscaAvancada_ddlTipoEmpresa')) #Select ID Tipo de Empresa
        txtTipo.select_by_value(type) #By value
        #txtTipo.select_by_visibleText("Empresário") #By text
        #txtTipo.select_by_index(1) #By index
        
        #Select Date Inicio
        txtMunicipio = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_txtDataAberturaInicio')
        initmonth= '25/'+str("%02d" % month)+'/'+str(year)
        txtMunicipio.send_keys(initmonth)
        
        #Select Date Fim
        txtMunicipio = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_txtDataAberturaFim')
        endmonth= '27/'+str("%02d" % month)+'/'+str(year)
        txtMunicipio.send_keys(endmonth)
        
        #Select all firms created (not only the active ones) "Mostrar somente empresas ativas"
        chkActive = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_chkAtivas').click()
        btPesquisar = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_btPesquisar')
        btPesquisar.click()
        seconds=10
        try:
            data_table = WebDriverWait(driver5,seconds).until(EC.presence_of_element_located((By.ID,'ctl00_cphContent_gdvResultadoBusca_gdvContent')))
              
            #Defining conditions for loop while month-year
            totalpageresult=0
            lastpageresult=2
            #In loop I'll redefine them, I just need them to be different, thats the condition to keep looping
            
            #While looping month-year
            while int(lastpageresult) != int(totalpageresult):
                #Scrape table from a page
                time.sleep(1)
                tabletemp = pd.read_html(driver5.find_element('xpath','//*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent"]').get_attribute('outerHTML'))[0]
                tabletemp = tabletemp.drop(tabletemp.columns[3], axis=1)
                tabletemp['Month']= str(month)
                tabletemp['Year'] = str(year)
                if type == "1":
                    tabletemp['Type']="Empresario"
                elif type == "2":
                    tabletemp['Type']="Sociedade Limitada"
                elif type == "3":
                    tabletemp['Type']="Sociedade por Acoes"
                elif type == "4":
                    tabletemp['Type']="Cooperativa"
                elif type == "5":
                    tabletemp['Type']="Consorcio"
                elif type == "6":
                    tabletemp['Type']="Grupo"
                elif type == "7":
                    tabletemp['Type']="Comandita Simple"
                elif type == "8":
                    tabletemp['Type']="Comandita por Acoes"
                elif type == "9":
                    tabletemp['Type']="Capital Industria"
                elif type == "10":
                    tabletemp['Type']="Solidaria"
                elif type == "11":
                    tabletemp['Type']="Armazens Gerais Ltda"
                elif type == "12":
                    tabletemp['Type']="Empresa Estrangeira"
                elif type == "13":
                    tabletemp['Type']="Binacional Ltda"
                elif type == "14":
                    tabletemp['Type']="Sociedade em Nome Coletivo"
                elif type == "15":
                    tabletemp['Type']="Empresa Publica"
                elif type == "16":
                    tabletemp['Type']="Subsidiaria Integral"
                elif type == "17":
                    tabletemp['Type']="Sociedade em Conta de Participacao"
                elif type == "18":
                    tabletemp['Type']="Armazens Gerais S/A"
                elif type == "19":
                    tabletemp['Type']="Binacional S/A"
                elif type == "21":
                    tabletemp['Type']="Armazens Gerais Empresario"
                else:
                    tabletemp['Type'] = "Outros"
                
                #Append this page to new table
                df = df.append(tabletemp)
                
                #Changing while condition
                #noninteresting, lastpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResults').text.replace('.',''))
                #totalpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResultCount').text.replace('.',''))[0]
                            
                #Click next page button
                try:
                    driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_btrNext_lbtText').click()
                    time.sleep(1)
                except: 
                    pass 
                #Changing while condition
                noninteresting, lastpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResults').text.replace('.',''))
                totalpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResultCount').text.replace('.',''))[0]
                
                print(f'Month {month} Year {year}, {lastpageresult} rows out of {totalpageresult}. Company Type "{type}"')
            
            #Scrape Last Page
            tabletemp = pd.read_html(driver5.find_element('xpath','//*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent"]').get_attribute('outerHTML'))[0]
            tabletemp = tabletemp.drop(tabletemp.columns[3], axis=1)
            tabletemp['Month']= str(month)
            tabletemp['Year'] = str(year)
            if type == "1":
                tabletemp['Type']="Empresario"
            elif type == "2":
                tabletemp['Type']="Sociedade Limitada"
            elif type == "3":
                tabletemp['Type']="Sociedade por Acoes"
            elif type == "4":
                tabletemp['Type']="Cooperativa"
            elif type == "5":
                tabletemp['Type']="Consorcio"
            elif type == "6":
                tabletemp['Type']="Grupo"
            elif type == "7":
                tabletemp['Type']="Comandita Simple"
            elif type == "8":
                tabletemp['Type']="Comandita por Acoes"
            elif type == "9":
                tabletemp['Type']="Capital Industria"
            elif type == "10":
                tabletemp['Type']="Solidaria"
            elif type == "11":
                tabletemp['Type']="Armazens Gerais Ltda"
            elif type == "12":
                tabletemp['Type']="Empresa Estrangeira"
            elif type == "13":
                tabletemp['Type']="Binacional Ltda"
            elif type == "14":
                tabletemp['Type']="Sociedade em Nome Coletivo"
            elif type == "15":
                tabletemp['Type']="Empresa Publica"
            elif type == "16":
                tabletemp['Type']="Subsidiaria Integral"
            elif type == "17":
                tabletemp['Type']="Sociedade em Conta de Participacao"
            elif type == "18":
                tabletemp['Type']="Armazens Gerais S/A"
            elif type == "19":
                tabletemp['Type']="Binacional S/A"
            elif type == "21":
                tabletemp['Type']="Armazens Gerais Empresario"
            else:
                tabletemp['Type'] = "Outros"
            
            
            #Append this page to new table
            df = df.append(tabletemp)
               
                
            #Scrape table from a LAST page
            #tabletemp = pd.read_html(driver5.find_element('xpath','//*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent"]').get_attribute('outerHTML'))[0]
            #tabletemp = tabletemp.drop(tabletemp.columns[3], axis=1)
            #tabletemp['Month']= str(month)
            #tabletemp['Year'] = str(year)
            
            #Append this LAST page to new table
            #df = df.append(tabletemp)
            
        except:
            pass
        
        #Get ready to introduce new captcha
        winsound.Beep(frequency, duration) #Makes a sound letting you know its time
        
        
        #Last 10 days
        #Get Web Page
        driver5.get('https://www.jucesponline.sp.gov.br/BuscaAvancada.aspx?IDProduto=') #Open web page
        
            
        #Date variable - LAST DAY OF MONTH 
        _, last_day = calendar.monthrange(year, month)
        #Select Type
        txtTipo = Select(driver5.find_element("id",'ctl00_cphContent_frmBuscaAvancada_ddlTipoEmpresa')) #Select ID Tipo de Empresa
        txtTipo.select_by_value(type) #By value
        #txtTipo.select_by_visibleText("Empresário") #By text
        #txtTipo.select_by_index(1) #By index
        
        #Select Date Inicio
        txtMunicipio = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_txtDataAberturaInicio')
        initmonth= '28/'+str("%02d" % month)+'/'+str(year)
        txtMunicipio.send_keys(initmonth)
        
        #Select Date Fim
        txtMunicipio = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_txtDataAberturaFim')
        endmonth= str(last_day)+'/'+str("%02d" % month)+'/'+str(year)
        txtMunicipio.send_keys(endmonth)
        
        #Select all firms created (not only the active ones) "Mostrar somente empresas ativas"
        chkActive = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_chkAtivas').click()
        btPesquisar = driver5.find_element('id','ctl00_cphContent_frmBuscaAvancada_btPesquisar')
        btPesquisar.click()
        seconds=10
        try:
            data_table = WebDriverWait(driver5,seconds).until(EC.presence_of_element_located((By.ID,'ctl00_cphContent_gdvResultadoBusca_gdvContent')))
              
            #Defining conditions for loop while month-year
            totalpageresult=0
            lastpageresult=2
            #In loop I'll redefine them, I just need them to be different, thats the condition to keep looping
            
            #While looping month-year
            while int(lastpageresult) != int(totalpageresult):
                #Scrape table from a page
                time.sleep(1)
                tabletemp = pd.read_html(driver5.find_element('xpath','//*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent"]').get_attribute('outerHTML'))[0]
                tabletemp = tabletemp.drop(tabletemp.columns[3], axis=1)
                tabletemp['Month']= str(month)
                tabletemp['Year'] = str(year)
                if type == "1":
                    tabletemp['Type']="Empresario"
                elif type == "2":
                    tabletemp['Type']="Sociedade Limitada"
                elif type == "3":
                    tabletemp['Type']="Sociedade por Acoes"
                elif type == "4":
                    tabletemp['Type']="Cooperativa"
                elif type == "5":
                    tabletemp['Type']="Consorcio"
                elif type == "6":
                    tabletemp['Type']="Grupo"
                elif type == "7":
                    tabletemp['Type']="Comandita Simple"
                elif type == "8":
                    tabletemp['Type']="Comandita por Acoes"
                elif type == "9":
                    tabletemp['Type']="Capital Industria"
                elif type == "10":
                    tabletemp['Type']="Solidaria"
                elif type == "11":
                    tabletemp['Type']="Armazens Gerais Ltda"
                elif type == "12":
                    tabletemp['Type']="Empresa Estrangeira"
                elif type == "13":
                    tabletemp['Type']="Binacional Ltda"
                elif type == "14":
                    tabletemp['Type']="Sociedade em Nome Coletivo"
                elif type == "15":
                    tabletemp['Type']="Empresa Publica"
                elif type == "16":
                    tabletemp['Type']="Subsidiaria Integral"
                elif type == "17":
                    tabletemp['Type']="Sociedade em Conta de Participacao"
                elif type == "18":
                    tabletemp['Type']="Armazens Gerais S/A"
                elif type == "19":
                    tabletemp['Type']="Binacional S/A"
                elif type == "21":
                    tabletemp['Type']="Armazens Gerais Empresario"
                else:
                    tabletemp['Type'] = "Outros"
                
                #Append this page to new table
                df = df.append(tabletemp)
                
                #Changing while condition
                #noninteresting, lastpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResults').text.replace('.',''))
                #totalpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResultCount').text.replace('.',''))[0]
                            
                #Click next page button
                try:
                    driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_btrNext_lbtText').click()
                    time.sleep(1)
                except: 
                    pass 
                #Changing while condition
                noninteresting, lastpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResults').text.replace('.',''))
                totalpageresult = re.findall('\d+',driver5.find_element('id','ctl00_cphContent_gdvResultadoBusca_pgrGridView_lblResultCount').text.replace('.',''))[0]
                
                print(f'Month {month} Year {year}, {lastpageresult} rows out of {totalpageresult}. Company Type "{type}"')
            
            #Scrape Last Page
            tabletemp = pd.read_html(driver5.find_element('xpath','//*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent"]').get_attribute('outerHTML'))[0]
            tabletemp = tabletemp.drop(tabletemp.columns[3], axis=1)
            tabletemp['Month']= str(month)
            tabletemp['Year'] = str(year)
            if type == "1":
                tabletemp['Type']="Empresario"
            elif type == "2":
                tabletemp['Type']="Sociedade Limitada"
            elif type == "3":
                tabletemp['Type']="Sociedade por Acoes"
            elif type == "4":
                tabletemp['Type']="Cooperativa"
            elif type == "5":
                tabletemp['Type']="Consorcio"
            elif type == "6":
                tabletemp['Type']="Grupo"
            elif type == "7":
                tabletemp['Type']="Comandita Simple"
            elif type == "8":
                tabletemp['Type']="Comandita por Acoes"
            elif type == "9":
                tabletemp['Type']="Capital Industria"
            elif type == "10":
                tabletemp['Type']="Solidaria"
            elif type == "11":
                tabletemp['Type']="Armazens Gerais Ltda"
            elif type == "12":
                tabletemp['Type']="Empresa Estrangeira"
            elif type == "13":
                tabletemp['Type']="Binacional Ltda"
            elif type == "14":
                tabletemp['Type']="Sociedade em Nome Coletivo"
            elif type == "15":
                tabletemp['Type']="Empresa Publica"
            elif type == "16":
                tabletemp['Type']="Subsidiaria Integral"
            elif type == "17":
                tabletemp['Type']="Sociedade em Conta de Participacao"
            elif type == "18":
                tabletemp['Type']="Armazens Gerais S/A"
            elif type == "19":
                tabletemp['Type']="Binacional S/A"
            elif type == "21":
                tabletemp['Type']="Armazens Gerais Empresario"
            else:
                tabletemp['Type'] = "Outros"
            
            
            #Append this page to new table
            df = df.append(tabletemp)
               
                
            #Scrape table from a LAST page
            #tabletemp = pd.read_html(driver5.find_element('xpath','//*[@id="ctl00_cphContent_gdvResultadoBusca_gdvContent"]').get_attribute('outerHTML'))[0]
            #tabletemp = tabletemp.drop(tabletemp.columns[3], axis=1)
            #tabletemp['Month']= str(month)
            #tabletemp['Year'] = str(year)
            
            #Append this LAST page to new table
            #df = df.append(tabletemp)
            
        except:
            pass
        
        #Get ready to introduce new captcha
        winsound.Beep(frequency, duration) #Makes a sound letting you know its time
        
    #SAVE THE DATA FRAME
    try:
        df.to_csv('C:/Users/Joaquin/Desktop/JUCESP-Scraper-Pesquisas/latin1/'+str(year)+'_'+str(month)+'_'+'Pesquisas_Jucesp_latin1.csv',index=False,encoding='latin1')
    except: 
        pass
    df.to_csv('C:/Users/Joaquin/Desktop/JUCESP-Scraper-Pesquisas/utf8/'+str(year)+'_'+str(month)+'_'+'Pesquisas_Jucesp_utf-8.csv',index=False,encoding='utf-8')

        
#Quit Webdriver
driver5.quit()
print("That's all folks!")