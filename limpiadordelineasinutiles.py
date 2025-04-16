"""
Este script elimina las líneas vacías de los archivos Markdown y TXT, excepto dentro de los bloques de código.
"""
import argparse
import os

def main():
    """
    Función principal del script.
    Configura el analizador de argumentos y procesa el directorio especificado.
    """
    parser = argparse.ArgumentParser(description="Elimina las líneas vacías de los archivos Markdown y TXT, excepto dentro de los bloques de código.")
    parser.add_argument("directory", help="El directorio a procesar recursivamente.")
    args = parser.parse_args()

    process_directory(args.directory)

def process_directory(directory):
    """
    Procesa recursivamente el directorio especificado para eliminar líneas vacías de los archivos Markdown y TXT.

    Args:
        directory (str): El directorio a procesar.
    """
    processed_count = 0
    error_files = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".md", ".txt")):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    cleaned_content = clean_empty_lines(content)

                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(cleaned_content)

                    processed_count += 1
                except Exception as e:
                    error_files.append((file_path, str(e)))
                    print(f"Error al procesar el archivo {file_path}: {e}") # Imprime el error en español

    print(f"Se procesaron {processed_count} archivos.")
    if error_files:
        print("Los siguientes archivos no pudieron ser procesados:")
        for file_path, error in error_files:
            print(f"- {file_path}: {error}")

def clean_empty_lines(content):
    """
    Elimina las líneas vacías de un texto, excepto dentro de los bloques de código.

    Args:
        content (str): El texto a limpiar.

    Returns:
        str: El texto limpio.
    """
    in_code_block = False  # Indica si estamos dentro de un bloque de código
    lines = [line.strip() for line in content.splitlines()] # Elimina espacios en blanco al principio y al final de cada línea
    cleaned_lines = []

    for line in lines:
        if line.startswith("```"):
            in_code_block = not in_code_block
            cleaned_lines.append(line)
        elif in_code_block:
            cleaned_lines.append(line)
        elif line:
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)

if __name__ == "__main__":
    main()