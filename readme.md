# DATA-CAT (Network Configuration Backup Tool)

Uma ferramenta robusta para backup automático de configurações de dispositivos Datacom (OLTs e Switches).

## Características
- 📦 Backup automático de múltiplos dispositivos
- 🔍 Seleção individual ou em massa de dispositivos
- 🌐 Teste de conectividade integrado
- 💾 Armazenamento local e remoto (FTP)
- ⚙️ Interface amigável para gerenciamento de dispositivos

## Requisitos
- Python 3.6 ou superior
- Biblioteca paramiko para conexões SSH

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/data-cat.git
cd data-cat
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Configuração

1. Configure os dispositivos através do menu da aplicação ou edite diretamente o arquivo `config/olt_config.json`:
```json
{
    "ftp_settings": {
        "server": "seu_servidor_ftp",
        "user": "seu_usuario",
        "password": "sua_senha",
        "base_path": "caminho/no/ftp"
    },
    "devices": [
        {
            "name": "DEVICE-01",
            "hostname": "192.168.1.1",
            "username": "admin",
            "password": "senha",
            "enabled": true
        }
    ]
}
```

## Uso

1. Execute o programa:
```bash
python main.py
```

2. Use o menu interativo para:
   - Realizar backup de todos os dispositivos
   - Selecionar dispositivos específicos
   - Testar conectividade
   - Gerenciar dispositivos
   - Configurar FTP

## Estrutura de Diretórios

```
data-cat/
├── config/
│   └── olt_config.json
├── modules/
│   ├── __init__.py
│   ├── backup.py
│   ├── config.py
│   ├── ftp.py
│   ├── network.py
│   └── ssh.py
├── interface/
│   ├── __init__.py
│   ├── banner.py
│   ├── menu.py
│   └── terminal.py
└── main.py
```

## Backups

Os backups são salvos em duas localizações:

1. Local:
   - Diretório: `backup_local_devices_datacom/`
   - Um subdiretório para cada dispositivo
   - Formato do arquivo: `backup-DEVICENAME-DATE_TIME.txt`

2. FTP:
   - Estrutura similar à local
   - Organizado por dispositivo
   - Mantém histórico de backups

## Desenvolvedor

- **Douglas Buzatto**
- Versão: 1.0.0-beta
- Atualização: Dezembro 2024

## Licença

Este projeto está sob a licença MIT.
