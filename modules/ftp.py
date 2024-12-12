from ftplib import FTP  # Adicionando importação
import os
from typing import Dict, Optional

def upload_to_ftp(ftp_settings: dict, local_file: str, remote_file: str) -> bool:
    """Upload direto para FTP"""
    try:
        with FTP(ftp_settings['server']) as ftp:
            ftp.login(user=ftp_settings['user'], passwd=ftp_settings['password'])
            
            print(f"📡 Conectado ao servidor FTP...")
            
            # Navegar para o diretório base
            ftp.cwd(ftp_settings['base_path'])
            
            # Ajusta o caminho remoto para incluir DEVICES_DATACOM
            remote_folder = os.path.join('DEVICES_DATACOM', os.path.dirname(remote_file))
            try:
                ftp.cwd(remote_folder)
            except:
                # Cria a estrutura de diretórios
                for folder in remote_folder.split(os.sep):
                    if folder:
                        try:
                            ftp.cwd(folder)
                        except:
                            print(f"📁 Criando pasta: {folder}")
                            ftp.mkd(folder)
                            ftp.cwd(folder)
            
            # Fazer o upload do arquivo
            print(f"📤 Enviando arquivo...")
            with open(local_file, 'rb') as file:
                ftp.storbinary(f'STOR {os.path.basename(remote_file)}', file)
                
        print(f"✅ Arquivo {local_file} enviado com sucesso para o FTP.")
        return True
    except Exception as e:
        print(f"❌ Falha no upload FTP do arquivo {local_file}: {e}")
        raise