#!/usr/bin/env python3
"""
Script principal para o sistema de backup de OLTs Datacom
"""
from interface.menu import Menu
import sys

def main():
    try:
        menu = Menu()
        menu.main_menu()
    except KeyboardInterrupt:
        print("\nPrograma encerrado pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(f"\nErro crítico: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()