from glob import glob
import pandas as pd
import numpy as np
import PyPDF2
import re

def standardize_values(valor_texto: str) -> float:
    """
    Converte uma string de valor monetário para float.
    Exemplo: '1.234,56 D' -> -1234.56
             '250,00 C' -> 250.00
    """
    if not valor_texto:
        return 0.0

    # Determina se o valor é débito (negativo)
    sinal = -1.0 if "D" in valor_texto.upper() else 1.0

    # Remove caracteres não numéricos, exceto a vírgula
    numero_limpo = re.sub(r"[^\d,]", "", valor_texto)

    # Substitui a vírgula por ponto para conversão para float
    numero_limpo = numero_limpo.replace(",", ".")

    if not numero_limpo:
        return 0.0

    return float(numero_limpo) * sinal

def converter () :
    """
    Leitura, tratamento e processamento de Notas de Corretagem pdf para xlsx

    """
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
                        index = text.index(texto_alvo) 
                        linha = text[index:].split('\n')[1]
                        df[df.columns[0]] = [linha]
                        #print(linha) 

                    texto_alvo = 'Valor dos negócios'
                    if texto_alvo in text:
                        index = text.index(texto_alvo)
                        for i in range(1,6):
                            linha = standardize_values(text[index:].split('\n')[i])
                            df[df.columns[i]] = [linha]
                            #print(linha)      
                    
                    texto_alvo = 'Taxas BM&F (emol+f.gar)'
                    if texto_alvo in text:
                        index = text.index(texto_alvo)
                        for i in range(5):
                            linha = standardize_values(text[index:].split('\n')[i+1])
                            df[df.columns[6+i]] = [linha]
                            #print(linha)    
                        
                    texto_alvo = 'Total de custos operacionais'
                    if texto_alvo in text:
                        index = text.index(texto_alvo)
                        for i in range(6):
                            linha = standardize_values(text[index:].split('\n')[i+1])
                            df[df.columns[11+i]] = [linha]
                            #print(linha)

                    texto_alvo = 'Total líquido da nota'
                    if texto_alvo in text:
                        index = text.index(texto_alvo)
                        for i in range(6):
                            linha = standardize_values(text[index:].split('\n')[i+1])
                            df[df.columns[17 + i]] = [linha]
                            #print(linha)  

                    df_page = pd.concat([df_page,df],ignore_index=True)
        
        df_page.drop(columns=['NAN'],inplace=True)
        #df.loc[:, df.columns != 'Data'] = df.loc[:, df.columns != 'Data'].apply(lambda x: x.str.replace(',', '.')).astype(float)
        #df_page.loc[df_page['IRRF Day Trade (proj.)'] < 0.01, 'Total líquido da nota'] *= -1
        print("Arquivos lidos com sucesso !")
        sheet_name = r'./notas/notas.xlsx' 
        df_new = df_page[['Valor dos negócios','IRRF Day Trade (proj.)', 'Total de custos operacionais','Total líquido da nota']]
        # Criando um writer para o arquivo Excel / Salvar datarame planilha  
        with pd.ExcelWriter(sheet_name) as writer:
            df_page.to_excel(writer, sheet_name='Sheet', index=False)
            df_new.to_excel(writer, sheet_name='Sheet2', index=False)
            print("Planilha criada com sucesso !")

    except Exception as e:
        print("Erro:", e)    


if __name__ == "__main__":
   converter()