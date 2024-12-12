import json
import os
from typing import Dict, List, Any

CONFIG_DIR = "config"
CONFIG_FILE = os.path.join(CONFIG_DIR, "olt_config.json")

def ensure_config_dir():
    """Garante que o diretório de configuração existe"""
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

def load_settings() -> Dict[str, Any]:
    """Carrega todas as configurações"""
    ensure_config_dir()
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return create_default_settings()

def load_devices() -> List[Dict[str, Any]]:
    """Carrega a lista de dispositivos configurados"""
    settings = load_settings()
    return settings.get('olts', [])  # Mantendo 'olts' para compatibilidade

def save_settings(settings: Dict[str, Any]):
    """Salva todas as configurações"""
    ensure_config_dir()
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=4)

def create_default_settings() -> Dict[str, Any]:
    """Cria configurações padrão quando não existe arquivo"""
    settings = {
        "ftp_settings": {
            "server": "10.34.250.7",
            "user": "route_cfg",
            "password": "bakroute",
            "base_path": "routecfg/DATACOM-BACKUPS"
        },
        "global_settings": {
            "ssh_timeout": 30,
            "buffer_size": 4096,
            "max_retries": 3,
            "retry_delay": 5,
            "max_workers": 6
        },
        "backup_settings": {
            "local_backup_path": "backups",
            "keep_local_copies": True,
            "days_to_keep": 30
        },
        "olts": []  # Lista inicial vazia
    }
    save_settings(settings)
    return settings