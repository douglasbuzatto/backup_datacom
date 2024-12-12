import platform
import subprocess
from typing import Dict, Tuple

def test_ping(host: str, count: int = 4) -> Tuple[bool, Dict[str, float]]:
    """
    Testa conectividade com um host usando ping
    
    Args:
        host: Endereço IP ou hostname
        count: Número de pings a serem enviados
        
    Returns:
        Tuple[bool, Dict]: Status e estatísticas do ping
    """
    system = platform.system().lower()
    
    if system == "windows":
        ping_cmd = ['ping', '-n', str(count), host]
    else:
        ping_cmd = ['ping', '-c', str(count), host]
        
    try:
        result = subprocess.run(ping_cmd, 
                              capture_output=True, 
                              text=True, 
                              timeout=10)
        
        # Analisa a saída para extrair estatísticas
        output = result.stdout.lower()
        success = "bytes=32" in output if system == "windows" else "64 bytes" in output
        
        # Extrai estatísticas básicas
        stats = {
            "packets_sent": count,
            "packets_received": output.count("bytes=32" if system == "windows" else "64 bytes"),
            "packet_loss": 0.0,
            "min_time": 0.0,
            "avg_time": 0.0,
            "max_time": 0.0
        }
        
        if success:
            stats["packet_loss"] = (count - stats["packets_received"]) / count * 100
            
        return success, stats
        
    except subprocess.TimeoutExpired:
        return False, {"error": "Timeout"}
    except Exception as e:
        return False, {"error": str(e)}