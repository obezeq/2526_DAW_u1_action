#!/usr/bin/python3

"""
Script principal para actualizar README con resultados de tests.
Este script orquesta todo el flujo.

Uso:
    python update_readme.py
"""

# Dependencies
from src.test_runner import run_tests
from src.generators import generate_report, generate_badge, update_readme
from src.utils import is_scheduled_action


# Main
def main():
    """
    Función principal que orquesta la ejecución de tests y generación de reportes.

    Flujo:
        1. Ejecuta tests y obtiene status + info
        2. Genera badge.svg (visual)
        3. Actualiza README.md (historial)
        4. Genera report.md (detalles)
    """
    print("[*] Ejecutando tests...")
    status, info = run_tests()
    
    # Detectamos el tipo de ejecucion
    is_scheduled = is_scheduled_action()
    tipo_ejecucion = "automática (schedule)" if is_scheduled else "manual/push"
    
    print(f"[*] Tipo de ejecucion: {tipo_ejecucion}")
    print(f"[*] Estado: {status}")
    print(f"[*] Tests pasados: {info['passed']}/{info['total']}")

    print("[*] Generando badge...")
    generate_badge(status, info)

    print("[*] Actualizando README...")
    update_readme(status, is_scheduled)

    print("[*] Generando reporte...")
    generate_report(status, info)

    print("[+] Proceso completado exitosamente :D")


if __name__ == "__main__":
    main()
