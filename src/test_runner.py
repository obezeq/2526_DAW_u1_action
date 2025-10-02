#!/usr/bin/python3

"""
Módulo para ejecutar tests con pytest.

Este módulo se encarga de:
- Ejecutar pytest con configuración JUnit XML
- Parsear los resultados
- Retornar estado y métricas de los tests
"""

import subprocess
from .utils import parse_junit_xml


def run_tests() -> tuple[str, dict]:
    """
    Ejecuta los tests con pytest y retorna el estado y la información.

    Genera un archivo JUnit XML temporal con los resultados,
    lo parsea para extraer métricas, y determina el estado general.

    Returns:
        tuple[str, dict]: Una tupla con:
            - status (str): Estado de los tests
            - info (dict): Diccionario con métricas:
                - total (int): Total de tests ejecutados
                - passed (int): Tests que pasaron
                - failures (int): Tests que fallaron
                - errors (int): Tests con errores
                - skipped (int): Tests omitidos
                - time (float): Tiempo de ejecución en segundos
    """
    
    xml_file = "test-results.xml"

    # Ejecutar pytest con reporte JUnit XML
    result = subprocess.run(
        ["pytest", f"--junitxml={xml_file}", "-v"],
        capture_output=True,
        text=True
    )

    # Parsear resultados del XML
    info = parse_junit_xml(xml_file)

    # Determinar estado según código de salida
    if result.returncode == 0:
        status = "✅ Tests correctos"
    else:
        status = "❌ Tests fallidos"

    return status, info
