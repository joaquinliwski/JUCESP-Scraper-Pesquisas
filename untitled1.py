# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 10:55:57 2023

@author: Joaquin
"""

import os
import pandas as pd

#%% OPEN FILES 

directory = "C:/Users/Joaquin/Desktop/UdeSA/Tesis/Datos/CSV Files"
os.chdir(directory)

#RAIS
# Get list of file names
file_list = [file for file in os.listdir(directory) if "employee" in file]
# Concatenate data frames
df_list = []
for file in file_list:
    file_path = os.path.join(directory, file)
    df = pd.read_csv(file_path)  
    df_list.append(df)
RAIS = pd.concat(df_list)
# Delete original data frames from memory
del df_list[:]


#PDFs
# Get list of file names
file_list = [file for file in os.listdir(directory) if "trial" in file]
# Concatenate data frames
df_list = []
for file in file_list:
    file_path = os.path.join(directory, file)
    df = pd.read_csv(file_path)  
    df_list.append(df)
PDFs = pd.concat(df_list)
# Delete original data frames from memory
del df_list[:]

#Ownership
ownership = pd.read_csv('partners_nov2022.csv')


