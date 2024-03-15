from glob import glob
import pandas as pd
import numpy as np
import PyPDF2
import re


"""""
Objetivo: Leitura, tratamento e processamento de notas de corretam PDF (SINOCAR)
"""""

def Get_File_Name ():
    files = sorted(glob(r'./notas/*.pdf'))
    for file in files:
        print(file)
        Read_File(file)


def Read_File (file_name) : 
    try:    
        with open(file_name, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)

            # Inicializar listas para armazenar os dados extraídos
            datas = []
            valores = []
            
            # Iterar sobre cada página do PDF
            for page_num in range(1):
                page = reader.pages[page_num]
                text = page.extract_text()
                print(text)
                # Procurar por padrões de data e valor usando expressões regulares
                pattern_data = r'\d{2}/\d{2}/\d{4}'
                pattern_valor = r'R\$\s*\d[\d\.,]*\d'
                matches_data = re.findall(pattern_data, text)
                matches_valor = re.findall(pattern_valor, text)
                
                # Adicionar as correspondências à lista de dados
                datas.extend(matches_data)
                valores.extend(matches_valor)
        # Criar DataFrame com os dados extraídos
        df = pd.DataFrame({'Data': datas, 'Total líquido da nota': valores})
        print(df)
    except Exception as e:
        print("Erro:",e)    





   
        
Get_File_Name()