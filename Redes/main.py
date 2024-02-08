import subprocess
import os

def ejecutar_script(script_path):
    """Ejecuta un script de Python ubicado en 'script_path'."""
    try:
        subprocess.run(["python", script_path], check=True)
        print(f"Script {script_path} ejecutado exitosamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar {script_path}: {e}")

def main():
    directorio_actual = os.path.dirname(os.path.abspath(__file__))

    # Define el nombre de cada script en el orden que deben ser ejecutados
    scripts = [
        "JSONtoNetwork.py",
        "ConexionNudosCctt.py",
        "MigracionAtributos.py",
        "NetworktoJSON.py",
        "UpdateOriginalJSON.py"
    ]

    for script in scripts:
        script_path = os.path.join(directorio_actual, script)
        ejecutar_script(script_path)

if __name__ == "__main__":
    main()
