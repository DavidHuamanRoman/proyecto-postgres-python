import os
import sys

def git_automatico():
    # 1. Verificamos si el usuario escribió un mensaje
    if len(sys.argv) < 2:
        print("⚠️  Falta el mensaje del commit.")
        print('Uso correcto: python git_aut.py "Tu mensaje aqui"')
        return

    # El mensaje es el segundo argumento (el primero es el nombre del script)
    mensaje = sys.argv[1]

    print(f"\n🚀 Iniciando subida automática: '{mensaje}'...\n")

    # 2. Ejecutamos los comandos en orden
    # os.system envía comandos a la terminal como si los escribieras tú
    
    print("--- 1. GIT ADD ---")
    codigo1 = os.system("git add .")
    if codigo1 != 0: return # Si falla, paramos

    print("\n--- 2. GIT COMMIT ---")
    # Usamos f-string para meter tu mensaje dentro del comando
    codigo2 = os.system(f'git commit -m "{mensaje}"') 
    if codigo2 != 0: return

    print("\n--- 3. GIT PUSH ---")
    codigo3 = os.system("git push")
    
    if codigo3 == 0:
        print("\n✅ ¡Todo subido exitosamente a GitHub!")
    else:
        print("\n❌ Hubo un error al subir.")

if __name__ == "__main__":
    git_automatico()