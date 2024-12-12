import os
import re
import time
from datetime import datetime
import paramiko
from .ftp import upload_to_ftp
from .config import load_settings

def backup_device(device_info: dict) -> bool:
    """Realiza o backup de um dispositivo"""
    hostname = device_info['hostname']
    username = device_info['username']
    password = device_info['password']
    device_name = device_info['name']
    
    # Criar nome de pasta seguro para o dispositivo
    device_folder = re.sub(r'[^\w-]', '', device_name)
    settings = load_settings()
    
    # Define a pasta base dos backups
    backup_base = "backup_local_devices_datacom"  # Mantendo o nome da pasta por compatibilidade
    
    try:
        print(f"[INFO] Iniciando conexão SSH com o dispositivo {device_name}...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, username=username, password=password)
        print(f"[INFO] Conexão SSH estabelecida com sucesso para {device_name}.")
        
        channel = client.invoke_shell()
        print(f"[INFO] Canal SSH aberto para {device_name}. Enviando comandos...")
        time.sleep(1)
        channel.recv(1024)  # Limpa o buffer inicial
        channel.send('show running-config\n')
        time.sleep(1)
        
        buffer = ''
        start_time = time.time()
        while True:
            if channel.recv_ready():
                chunk = channel.recv(4096).decode('utf-8', errors='ignore')
                buffer += chunk
                if '--More--' in chunk:
                    channel.send(' ')
                    time.sleep(0.5)
            elif time.time() - start_time > 30 or buffer.strip().endswith('#'):
                break
        
        print(f"[INFO] Comando executado com sucesso para {device_name}. Coletando dados...")
        
        # Limpar o output
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        clean_buffer = ansi_escape.sub('', buffer)
        clean_buffer = re.sub(r'--More--|\r', '', clean_buffer)
        
        # Remove o comando inicial e linhas vazias do início
        lines = clean_buffer.split('\n')
        while lines and (not lines[0].strip() or 'show running-config' in lines[0].lower()):
            lines.pop(0)
        clean_buffer = '\n'.join(lines).strip()
        
        # Remove o prompt do final (linha com #)
        lines = clean_buffer.split('\n')
        if lines and lines[-1].strip().endswith('#'):
            lines.pop()
        clean_buffer = '\n'.join(lines).strip()
        
        now = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
        filename = f'backup-{device_folder}-{now}.txt'
        
        full_path = os.path.join(backup_base, device_folder)
        os.makedirs(full_path, exist_ok=True)
        local_path = os.path.join(full_path, filename)
        
        with open(local_path, 'w', encoding='utf-8') as f:
            f.write(clean_buffer)
        print(f"[INFO] Backup salvo localmente com sucesso para {device_name}: {local_path}")
        
        # Upload para FTP
        remote_path = os.path.join(device_folder, filename)
        upload_to_ftp(settings['ftp_settings'], local_path, remote_path)
        
        return True
    except Exception as e:
        print(f"[ERROR] Ocorreu um erro para {device_name}: {e}")
        raise
    finally:
        client.close()
        print(f"[INFO] Conexão SSH encerrada para {device_name}.")