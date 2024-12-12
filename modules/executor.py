from concurrent.futures import ThreadPoolExecutor, as_completed
from .backup import backup_device
from .config import load_settings

# Emojis para status
STATUS = {
    'success': '✅',
    'error': '❌',
    'info': 'ℹ️',
    'warning': '⚠️',
    'connecting': '🔄',
    'saving': '💾',
    'uploading': '📤',
    'done': '🎉'
}

def execute_backups(selected_devices=None):
    """
    Executa backups em paralelo
    
    Returns:
        list: Lista de mensagens de log
    """
    messages = []
    settings = load_settings()
    devices = selected_devices if selected_devices is not None else settings.get('olts', [])
    
    if not devices:
        return [f"{STATUS['warning']} Nenhum dispositivo configurado para backup!"]
    
    messages.append(f"{STATUS['info']} Iniciando processo de backup...")
    
    with ThreadPoolExecutor(max_workers=len(devices)) as executor:
        futures = []
        for device in devices:
            future = executor.submit(backup_device, device)
            futures.append((device['name'], future))
        
        for device_name, future in futures:
            try:
                result = future.result()
                messages.append(f"{STATUS['success']} Backup do dispositivo {device_name} concluído com sucesso")
            except Exception as e:
                messages.append(f"{STATUS['error']} Falha no backup do dispositivo {device_name}: {str(e)}")
    
    messages.append(f"\n{STATUS['done']} Processo de backup finalizado!")
    return messages