import paramiko
import time
from typing import Dict, Optional

class SSHClient:
    def __init__(self, host: str, username: str, password: str, timeout: int = 30):
        self.host = host
        self.username = username
        self.password = password
        self.timeout = timeout
        self.client: Optional[paramiko.SSHClient] = None
        self.channel = None

    def connect(self) -> bool:
        """Estabelece conexão SSH"""
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(
                self.host,
                username=self.username,
                password=self.password,
                timeout=self.timeout,
                look_for_keys=False,
                allow_agent=False
            )
            return True
        except Exception as e:
            raise ConnectionError(f"Falha na conexão SSH: {str(e)}")

    def get_config(self) -> str:
        """Obtém a configuração do equipamento"""
        try:
            channel = self.client.invoke_shell()
            channel.settimeout(self.timeout)
            time.sleep(1)
            
            # Limpa buffer inicial
            if channel.recv_ready():
                channel.recv(4096)
            
            # Envia comando
            channel.send('show running-config\n')
            time.sleep(1)
            
            buffer = ''
            end_time = time.time() + self.timeout
            
            while time.time() < end_time:
                if channel.recv_ready():
                    chunk = channel.recv(4096).decode('utf-8', errors='ignore')
                    buffer += chunk
                    
                    if '--More--' in chunk:
                        channel.send(' ')
                        time.sleep(0.1)
                    
                    if chunk.strip().endswith('#'):
                        time.sleep(0.5)
                        if not channel.recv_ready():
                            break
                else:
                    time.sleep(0.1)
            
            return buffer
            
        finally:
            if channel:
                channel.close()

    def close(self):
        """Fecha a conexão SSH"""
        if self.client:
            self.client.close()