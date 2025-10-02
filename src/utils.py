#!/usr/bin/python3

"""
Utilidades generales del proyecto.

Este módulo contiene funciones auxiliares reutilizables:
- Manejo de fechas y horas
- Parseo de archivos XML de JUnit
"""

from datetime import datetime
import xml.etree.ElementTree as ET


def get_now() -> str:
    """
    Obtiene la fecha y hora actual formateada.

    Returns:
        str: Fecha y hora en formato "YYYY-MM-DD HH:MM"
    """
    
    ahora = datetime.now()
    fecha_hora = ahora.strftime("%Y-%m-%d %H:%M")
    return fecha_hora


def parse_junit_xml(xml_file: str) -> dict:
    """
    Parsea un archivo JUnit XML y extrae métricas de tests.

    Args:
        xml_file (str): Ruta al archivo XML de JUnit

    Returns:
        dict: Diccionario con métricas:
            - total (int): Total de tests
            - failures (int): Tests fallidos
            - errors (int): Tests con errores
            - skipped (int): Tests omitidos
            - time (float): Tiempo de ejecución
            - passed (int): Tests pasados (calculado)

    Raises:
        ET.ParseError: Si el archivo XML está mal formado
    """
    
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Determinar elemento testsuite
        if root.tag == 'testsuite':
            testsuite = root
        else:
            testsuite = root.find('testsuite')

        # Extraer métricas del XML
        total_tests = int(testsuite.get('tests', 0))
        failures = int(testsuite.get('failures', 0))
        errors = int(testsuite.get('errors', 0))
        skipped = int(testsuite.get('skipped', 0))
        time_tests = float(testsuite.get('time', 0))

        # Calcular tests pasados
        passed = total_tests - failures - errors - skipped

        junit_xml_parsed = {
            'total': total_tests,
            'failures': failures,
            'errors': errors,
            'skipped': skipped,
            'time': time_tests,
            'passed': passed
        }

    except FileNotFoundError:
        print(f"[-] ERROR: No se ha encontrado {xml_file}")

        # Retornar valores por defecto en caso de error
        return {
            'total': 0,
            'failures': 0,
            'errors': 1,
            'skipped': 0,
            'time': 0.0,
            'passed': 0
        }

    except ET.ParseError as e:
        print(f"[-] ERROR: Error al parsear el XML: {e}")
        raise

    else:
        return junit_xml_parsed
