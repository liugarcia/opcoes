import ftplib
import zipfile
import pandas as pd
from datetime import datetime

hoje = datetime.now().strftime('%Y%m%d')
arquivo_zip = f'op{hoje}.zip'

try:
    # Conecta ao FTP da B3
    ftp = ftplib.FTP('ftp.b3.com.br')
    ftp.login()
    ftp.cwd('/marketdata/Opcao/')

    with open(arquivo_zip, 'wb') as f:
        ftp.retrbinary(f'RETR {arquivo_zip}', f.write)

    ftp.quit()

    # Extrai o CSV do ZIP
    with zipfile.ZipFile(arquivo_zip, 'r') as zip_ref:
        zip_ref.extractall()
        for nome_csv in zip_ref.namelist():
            df = pd.read_csv(nome_csv, sep=';', encoding='latin1')
            df = df[df['Especificacao do Ativo'].str.contains('PETR4', na=False)]

            df = df[[
                'Especificacao do Ativo',
                'Tipo de Opcao',
                'Preco de Exercicio',
                'Data de Vencimento',
                'Preco de Fechamento'
            ]]

            df.to_json('opcoes.json', orient='records', force_ascii=False)

except Exception as e:
    print(f"Erro: {e}")
