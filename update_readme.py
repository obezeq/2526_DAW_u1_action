#!/usr/bin/python3

# Automatizacion con GitHub Actions

# ──────────────────────────────────────────────────────────────────

# Dependencies

import subprocess
import xml.etree.ElementTree as ET
from utils import get_now

# ──────────────────────────────────────────────────────────────────

def parse_junit_xml(xml_file: str) -> dict:
    """Parseamos el archivo JUnit XML y extramemos la información que nos sea útil.

    Args:
        xml_file (str): The XML File Route

    Returns:
        dict: El JUnit XML parsed
    """
    
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        if (root.tag == 'testsuite'):
            testsuite = root
        else:
            testsuite = root.find('testsuite')
            
        total_tests = int(testsuite.get('tests', 0))
        failures = int(testsuite.get('failures', 0))
        errors = int(testsuite.get('errors', 0))
        skipped = int(testsuite.get('skipped', 0))
        time_tests = float(testsuite.get('time', 0))
        passed = total_tests - failures - errors - skipped
            
        junit_xml_parsed = {
            'total': total_tests,
            'failures': failures,
            'errors': errors,
            'skipped': skipped,
            'time': time_tests,
            'passed': passed
        }
        
    except FileNotFoundError as e:
        
        print(f"[-] ERROR: No se ha encontrado {xml_file}")
        
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
    
def generate_report(status: str, info: dict):
    """Generar el reporte report.md con la info de los tests

    Args:
        status (str): El estado de los tests
        info (dict): La info de los tests
    """
    
    fecha_hora = get_now()
    report = f"""# Test Report ({fecha_hora})

- **Total tests:** {info['total']}
- **Tests pasados:** {info['passed']} ✅
- **Tests fallidos:** {info['failures']} ❌
- **Tests con errores:** {info['errors']}
- **Tests omitidos:** {info['skipped']} 

## Tiempo de ejecución
- Duración total: {info['time']:.2f} segundos

## Estado

{status}
"""
    
    with open("report.md", 'w', encoding='utf-8') as f:
        f.write(report)

# ──────────────────────────────────────────────────────────────────

def generate_badge(status: str, info: dict):
    """Generamos un badge SVG con el estado de los tests.

    Args:
        status (str): Estado de los tests
        info (dict): Informacion de los tests
    """
    
    passed = info.get("passed")
    total = info.get("total")
    
    color = None
    mensaje = None
    
    if (total == 0):
        color = "#9f9f9f"
        mensaje = "no tests"
    elif (passed == total):
        color = "#4c1"
        mensaje = f"{passed}/{total} passing"
    elif (passed < total):
        color = "#e05d44"
        mensaje = f"{passed}/{total} passing"
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="150" height="20">
    <linearGradient id="b" x2="0" y2="100%">
        <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
        <stop offset="1" stop-opacity=".1"/>
    </linearGradient>
    <mask id="a">
        <rect width="150" height="20" rx="3" fill="#fff"/>
    </mask>
    <g mask="url(#a)">
        <path fill="#555" d="M0 0h50v20H0z"/>
        <path fill="{color}" d="M50 0h100v20H50z"/>
        <path fill="url(#b)" d="M0 0h150v20H0z"/>
    </g>
    <g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">
        <text x="25" y="15" fill="#010101" fill-opacity=".3">tests</text>
        <text x="25" y="14">tests</text>
        <text x="100" y="15" fill="#010101" fill-opacity=".3">{mensaje}</text>
        <text x="100" y="14">{mensaje}</text>
    </g>
</svg>'''
    
    with open("badge.svg", 'w', encoding='utf-8') as f:
        f.write(svg)

# ──────────────────────────────────────────────────────────────────

def run_tests() -> tuple[str, dict]:
    """Esta funcion ejecutara los tests y generara un reporte XML.

    Returns:
        tuple: (status, info_dict)
    """
    
    xml_file = "test-results.xml"
    result = subprocess.run(
        ["pytest", f"--junitxml={xml_file}", "-v"],
        capture_output=True,
        text=True
    )
    
    info = parse_junit_xml(xml_file)
    
    if result.returncode == 0:
        status = f"✅ Tests correctos"
    else:
        status = f"❌ Tests fallidos"
        
    """ try:
        subprocess.check_call(["pytest", "-q"])
        status = f"✅ Tests correctos"
    except subprocess.CalledProcessError:
        status = f"❌ Tests fallidos" """
        
    return status, info

def update_readme(status: str):
    
    fecha_hora = get_now()
    linea_historial = f"- {status[:2]} {fecha_hora} - {status[2:].strip()}\n"
    
    with open("README.md", "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        new_lines.append(line)
        if line.strip() == "## Estado de los tests":
            new_lines.append(linea_historial)

    with open("README.md", "w", encoding="utf-8") as f:
        f.writelines(new_lines)

# ──────────────────────────────────────────────────────────────────

# Main
if __name__ == "__main__":
    
    status, info = run_tests()
    generate_badge(status, info)
    update_readme(status)
    generate_report(status, info)
