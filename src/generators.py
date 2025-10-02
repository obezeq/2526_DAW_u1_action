#!/usr/bin/python3

"""
Generadores de archivos de salida.
"""

from .utils import get_now


def generate_report(status: str, info: dict) -> None:
    """
    Genera el archivo report.md con información detallada de los tests.

    Args:
        status (str): Estado de los tests
        info (dict): Info de los tests
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


def generate_badge(status: str, info: dict) -> None:
    """
    Genera un badge SVG con el estado visual de los tests.

    El badge muestra:
    - Color verde (#4c1) si todos los tests pasan
    - Color rojo (#e05d44) si algún test falla
    - Color gris (#9f9f9f) si no hay tests
    - Texto con ratio de tests (ej: "4/5 passing")

    Args:
        status (str): Estado de los tests
        info (dict): Diccionario con métricas de los tests
    """
    
    passed = info.get("passed")
    total = info.get("total")

    if total == 0:
        color = "#9f9f9f"
        mensaje = "no tests"
    elif passed == total:
        color = "#4c1"
        mensaje = f"{passed}/{total} passing"
    else:
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

    with open("badge.svg", "w", encoding="utf-8") as f:
        f.write(svg)


def update_readme(status: str) -> None:
    """
    Actualiza el README.md añadiendo una nueva línea al historial de tests.

    Args:
        status (str): Estado de los tests
    """
    
    fecha_hora = get_now()
    linea_historial = f"- {status[:2]} {fecha_hora} - {status[2:].strip()}\n"

    # Leer README actual
    with open("README.md", "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Construir nuevo README con historial añadido
    new_lines = []
    for line in lines:
        new_lines.append(line)
        if line.strip() == "## Estado de los tests":
            new_lines.append(linea_historial)

    # Guardar README actualizado
    with open("README.md", "w", encoding="utf-8") as f:
        f.writelines(new_lines)
