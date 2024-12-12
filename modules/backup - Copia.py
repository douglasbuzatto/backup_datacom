import os
import re
import time
from datetime import datetime
from typing import Dict
from .ssh import SSHClient
from .ftp import FTPManager
from .config import load_settings

class BackupManager:
    def __init__(self):
        self.settings = load_settings()
        self.ftp = FTPManager(self.settings['ftp_settings'])

    def backup_olt(self, olt: Dict) -> bool:
        """
        Realiza o backup de uma OLT específica
        
        Args:
            olt: Dicionário com informações da OLT
        """
        hostname = olt['hostname']
        username = olt['username']
        password = olt['password']
        olt_name = olt['name']
        
        # Criar nome de pasta seguro para a OLT
        olt_folder = re.sub(r'[^\w-]', '', olt_name)
        
        try:
            print(f"[INFO] Iniciando conexão SSH com a OLT {olt_name}...")
            ssh = SSHClient(hostname, username, password)
            ssh.connect()
            print(f"[INFO] Conexão SSH estabelecida com sucesso para {olt_name}.")
            
            # Obter a configuração
            config = ssh.get_config()
            print(f"[INFO] Comando 'show running-config' executado com sucesso para {olt_name}.")
            
            # Salvar arquivo local
            now = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
            filename = f'backup-{olt_folder}-{now}.txt'
            
            os.makedirs(olt_folder, exist_ok=True)
            local_path = os.path.join(olt_folder, filename)
            
            with open(local_path, 'w', encoding='utf-8') as f:
                f.write(config)
            print(f"[INFO] Backup salvo localmente com sucesso para {olt_name}: {local_path}")
            
            # Upload para FTP
            remote_path = os.path.join(olt_folder, filename)
            self.ftp.upload_file(local_path, remote_path)
            
            return True
            
        except Exception as e:
            raise Exception(f"Erro no backup da OLT {olt_name}: {str(e)}")
        finally:
            ssh.close()
            print(f"[INFO] Conexão SSH encerrada para {olt_name}.")

    def close(self):
        """Método mantido para compatibilidade"""
        pass