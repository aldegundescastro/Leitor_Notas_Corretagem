from glob import glob
import pandas as pd
import numpy as np
import PyPDF2
import re



def Read_File () :
    # Criar dataframes
    head = ['Data','Venda disponível','Compra disponível','Venda Opções','Compra Opções','Valor dos negócios',
            'IRRF','IRRF Day Trade (proj.)','Taxa operacional','Taxa registro BM&F','Taxas BM&F (emol+f.gar)',
            'NAN','+Outros Custos','Impostos','Ajuste de posição','Ajuste day trade','Total de custos operacionais',
            'Outros','IRRF operacional','Total Conta Investimento','Total Conta Normal','Total liquido (#)','Total líquido da nota']
    df = pd.DataFrame(columns = head)
    df_page = pd.DataFrame(columns = head)
    df_file = pd.DataFrame(columns = head)
    df_files = pd.DataFrame(columns = head) 
    
    try:
        # Obter lista com nome dos arquivos    
        files = sorted(glob(r'./notas/*.pdf'))
        for file_name in files:
            print(file_name)
            with open(file_name, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                num_pages = len(reader.pages)

                # Iterar sobre cada página do PDF
                for page_num in range(num_pages):
                    page = reader.pages[page_num]
                    text = str(page.extract_text())
                    #print(text)

                    texto_alvo = 'Data pregão'
                    if texto_alvo in text:                              
                        #print(texto_alvo)
                        index = text.index(texto_alvo) 
                        linha = text[index:].split('\n')[1]
                        df[df.columns[0]] = [linha]
                        #print(linha) 

                    texto_alvo = 'Valor dos negócios'
                    if texto_alvo in text:
                        #print(texto_alvo)
                        index = text.index(texto_alvo)
                        for i in range(1,6):
                            linha = text[index:].split('\n')[i][:4]
                            df[df.columns[i]] = [linha]
                            #print(linha)      
                    
                    texto_alvo = 'Taxas BM&F (emol+f.gar)'
                    if texto_alvo in text:
                        #print(texto_alvo)
                        index = text.index(texto_alvo)
                        for i in range(5):
                            linha = text[index:].split('\n')[i+1][:4]
                            df[df.columns[6+i]] = [linha]
                            #print(linha)    
                        
                    texto_alvo = 'Total de custos operacionais'
                    if texto_alvo in text:
                        #print(texto_alvo)
                        index = text.index(texto_alvo)
                        for i in range(6):
                            linha = text[index:].split('\n')[i+1][:4]
                            df[df.columns[11+i]] = [linha]
                            #print(linha)

                    texto_alvo = 'Total líquido da nota'
                    if texto_alvo in text:
                        #print(texto_alvo)
                        index = text.index(texto_alvo)
                        for i in range(6):
                            linha = text[index:].split('\n')[i+1][:4]
                            df[df.columns[17 + i]] = [linha]
                            #print(linha)  

                    df_page = pd.concat([df_page,df],ignore_index=True)
        
        df_page.drop(columns=['NAN'],inplace=True)
        #df.loc[:, df.columns != 'Data'] = df.loc[:, df.columns != 'Data'].apply(lambda x: x.str.replace(',', '.')).astype(float)
        #df_page.loc[df_page['IRRF Day Trade (proj.)'] < 0.01, 'Total líquido da nota'] *= -1
        print("Arquivos lidos com sucesso !")
        sheet_name = 'notas.xlsx'
        df_new = df_page[['Valor dos negócios','IRRF Day Trade (proj.)', 'Total de custos operacionais','Total líquido da nota']]
        
        # Criando um writer para o arquivo Excel / Salvar datarame planilha  
        with pd.ExcelWriter(sheet_name) as writer:
            df_page.to_excel(writer, sheet_name='Sheet', index=False)
            df_new.to_excel(writer, sheet_name='Sheet2', index=False)
            print("Planilha criada com sucesso !")

    except Exception as e:
        print("Erro:", e)    


if __name__ == "__main__":
   Read_File()