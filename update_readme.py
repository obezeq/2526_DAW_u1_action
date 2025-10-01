import subprocess
from datetime import datetime

def get_now() -> str:
    ahora = datetime.now()
    fecha_hora = ahora.strftime("%Y-%m-%d %H:%M")
    return fecha_hora

def run_tests() -> str:
    try:
        subprocess.check_call(["pytest", "-q"])
        return f"✅ Tests correctos"
    except subprocess.CalledProcessError:
        return f"❌ Tests fallidos"

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

if __name__ == "__main__":
    status = run_tests()
    update_readme(status)
