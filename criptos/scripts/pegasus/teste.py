#!/usr/bin/env python3
# Shebang line - indica que este script deve ser executado com Python 3

# Pegasus v1.2 - Created by thakur2309
# Use for Educational Purpose Only
# Deobfuscated and rebuilt

import subprocess  # Para executar comandos do sistema
import shutil      # Para operações de arquivo e encontrar executáveis
import sys         # Para acessar funções do sistema como exit()
import os          # Para comandos do sistema operacional (clear screen)
import time        # Para pausas/delays no código
import re          # Para expressões regulares (não usado neste código)

# ----------------- Config / Colors -----------------
# Códigos ANSI para colorir a saída no terminal
GREEN = "\033[1;32m"   # Verde brilhante
YELLOW = "\033[1;33m"  # Amarelo brilhante
RED = "\033[1;31m"     # Vermelho brilhante
CYAN = "\033[1;36m"    # Ciano brilhante
RESET = "\033[0m"      # Reseta a cor para o padrão

# Arte ASCII do logo Pegasus
BANNER = r"""
██████╗  █████╗  ██████╗  █████╗ ███████╗██╗   ██╗███████╗
██╔══██╗██╔══██╗██╔════╝ ██╔══██╗██╔════╝██║   ██║██╔════╝
██████╔╝███████║██║  ███╗███████║███████╗██║   ██║███████╗
██╔═══╝ ██╔══██║██║   ██║██╔══██║╚════██║██║   ██║╚════██║
██║     ██║  ██║╚██████╔╝██║  ██║███████║╚██████╔╝███████║
╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚══════╝
"""

# Linhas de cabeçalho que aparecem abaixo do banner
HEADER_LINES = [
    "              Pegasus v1.2  ",
    "          Created by GPWeb",
    "      Use for Educational Purpose Only"
]

# ----------------- Helpers -----------------
def check_dependency(cmd_name, apt_pkg_name=None):
    """
    Verifica se um comando está disponível no sistema
    cmd_name: nome do comando (ex: 'adb')
    apt_pkg_name: nome do pacote apt (não usado, mantido para compatibilidade)
    Retorna: True se o comando existe, False caso contrário
    """
    path = shutil.which(cmd_name)  # Procura o executável no PATH do sistema
    return bool(path)  # Retorna True se encontrou, False se None

def run_cmd(cmd, capture=False):
    """
    Executa um comando no shell
    cmd: string do comando a executar
    capture: se True, captura a saída; se False, mostra no terminal
    Retorna: dependendo do capture, retorna (stdout, stderr) ou código de retorno
    """
    try:
        if capture:
            # Executa e captura stdout/stderr como texto
            res = subprocess.run(cmd, shell=True, check=False, 
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return res.stdout.strip(), res.stderr.strip()  # Retorna saída e erro
        else:
            # Executa e mostra no terminal, retorna código de saída
            return subprocess.call(cmd, shell=True)
    except Exception as e:
        return None  # Em caso de erro, retorna None

def adb_available():
    """Verifica se o ADB (Android Debug Bridge) está instalado"""
    return check_dependency("adb")

def scrcpy_available():
    """Verifica se o scrcpy (espelhamento de tela) está instalado"""
    return check_dependency("scrcpy")

def clear_screen():
    """Limpa a tela do terminal"""
    # Usa 'clear' no Linux/Mac ou 'cls' no Windows
    os.system("clear" if shutil.which("clear") else "cls")

def print_banner():
    """Exibe o banner, cabeçalho e uma linha separadora"""
    clear_screen()  # Limpa a tela primeiro
    print(GREEN + BANNER + RESET)  # Exibe o logo em verde
    for line in HEADER_LINES:  # Para cada linha do cabeçalho
        print(GREEN + line.center(55) + RESET)  # Centraliza e exibe
    print(CYAN + "-"*59 + RESET)  # Linha separadora em ciano
    print()

# ----------------- ADB Helpers -----------------
def adb_devices_list():
    """
    Obtém a lista de dispositivos conectados via ADB
    Retorna: lista de IDs dos dispositivos
    """
    out, err = run_cmd("adb devices", capture=True)  # Executa 'adb devices'
    if out is None:  # Se falhou
        return []
    lines = out.splitlines()  # Divide a saída em linhas
    devices = []
    for line in lines[1:]:  # Pula a primeira linha (cabeçalho)
        line = line.strip()  # Remove espaços
        if line:  # Se não está vazia
            parts = line.split()  # Divide em partes
            devices.append(parts[0])  # Adiciona o ID do dispositivo
    return devices

def ensure_device_connected_prompt():
    """
    Verifica se há dispositivos conectados
    Se não houver, mostra instruções e pede para conectar
    Retorna: True se há dispositivo, False caso contrário
    """
    devices = adb_devices_list()
    if not devices:
        print(RED + "[!] No device detected." + RESET)
        print(YELLOW + "Please connect your device via USB and enable USB Debugging (Developer Options)." + RESET)
        print(YELLOW + "Settings -> Developer options -> USB debugging (enable)." + RESET)
        input("\nPress Enter after connecting device to continue...")
        return False
    return True

# ----------------- Option Implementations -----------------
def option_check_device():
    """Opção 1: Verifica informações do dispositivo conectado"""
    print(CYAN + "\n[+] Checking for connected devices..." + RESET)
    devices = adb_devices_list()
    if not devices:
        print(RED + "[-] No device detected." + RESET)
        print(YELLOW + "Choose option 2 to connect a device or connect via USB and allow debugging on device." + RESET)
        return
    device = devices[0]  # Pega o primeiro dispositivo
    print(GREEN + f"[+] Device found: {device}" + RESET)
    print(CYAN + "[*] Gathering device info..." + RESET)
    
    # Obtém informações do dispositivo via ADB
    model, _ = run_cmd("adb shell getprop ro.product.model", capture=True)
    android_ver, _ = run_cmd("adb shell getprop ro.build.version.release", capture=True)
    battery_info, _ = run_cmd("adb shell dumpsys battery | grep level", capture=True)
    
    # Exibe as informações obtidas
    if model: print(f"Model: {model}")
    if android_ver: print(f"Android: {android_ver}")
    if battery_info: print(f"Battery: {battery_info}")
    else:
        # Fallback para obter info da bateria
        batt, _ = run_cmd("adb shell dumpsys battery", capture=True)
        for line in (batt or "").splitlines():
            if "level" in line:
                print(line.strip())
    print()

def option_connect_device():
    """Opção 2: Conecta dispositivo via Wi-Fi"""
    print(CYAN + "\n[+] Running 'adb devices'..." + RESET)
    devices = adb_devices_list()
    if not devices:
        print(RED + "[-] No device detected via USB." + RESET)
        print(YELLOW + "Please connect your device via USB and enable USB Debugging (Developer Options)." + RESET)
        return
    
    print(GREEN + "[+] Device detected via USB. Switching adb to tcpip mode on port 5555..." + RESET)
    run_cmd("adb tcpip 5555")  # Muda ADB para modo TCP/IP na porta 5555
    
    ip = input("Enter device IP address (e.g. 192.168.1.10): ").strip()
    if not ip:
        print(RED + "No IP provided. Aborting connect." + RESET)
        return
    
    print(CYAN + f"Connecting to {ip}:5555 ..." + RESET)
    out, err = run_cmd(f"adb connect {ip}:5555", capture=True)
    
    # Verifica se conectou com sucesso
    if "connected" in out.lower() or "already" in out.lower():
        print(GREEN + "[+] Connected successfully over Wi-Fi." + RESET)
        run_cmd("adb devices")
    else:
        print(RED + "[-] Could not connect. Output:" + RESET)
        print(out or err)

def option_disconnect_device():
    """Opção 3: Desconecta todas as conexões ADB"""
    print(CYAN + "\n[*] Disconnecting adb connections..." + RESET)
    out, err = run_cmd("adb disconnect", capture=True)
    print(GREEN + "[+] adb disconnect issued." + RESET)
    print("\nCurrent adb devices:")
    run_cmd("adb devices")

def option_screen_recording():
    """Opção 4: Grava a tela do dispositivo"""
    if not ensure_device_connected_prompt():
        return
    
    dur = input("Enter recording duration (e.g. '15s' or '30' for seconds): ").strip()
    if dur.endswith("s"):
        dur_val = dur[:-1]  # Remove o 's' do final
    else:
        dur_val = dur
    
    try:
        dsec = int(dur_val)  # Converte para inteiro
    except:
        print(RED + "Invalid duration. Enter seconds as integer (e.g. 15)." + RESET)
        return
    
    filename = "record.mp4"
    print(CYAN + f"[*] Starting screenrecord for {dsec} seconds..." + RESET)
    cmd = f"adb shell screenrecord --time-limit {dsec} /sdcard/{filename}"
    rc = run_cmd(cmd)
    
    if rc is None:  # Fallback se o comando padrão falhar
        print(YELLOW + "Fallback recording method..." + RESET)
        run_cmd(f"adb shell screenrecord /sdcard/{filename} &")
        time.sleep(dsec)  # Aguarda a duração
        run_cmd("adb shell pkill -f screenrecord")  # Mata o processo
    
    print(CYAN + "[*] Pulling recording to current directory..." + RESET)
    run_cmd(f"adb pull /sdcard/{filename} ./")  # Baixa o arquivo
    
    print(GREEN + f"[+] Recording saved as ./{filename}" + RESET)
    view = input("Do you want to open the recording now? (y/n): ").strip().lower()
    if view == "y":
        opener = shutil.which("xdg-open") or "xdg-open"  # Abridor padrão
        run_cmd(f"{opener} {filename}")

def option_screen_mirror():
    """Opção 5: Espelha a tela usando scrcpy"""
    if not ensure_device_connected_prompt():
        return
    
    if not scrcpy_available():
        print(RED + "[!] scrcpy not found." + RESET)
        print(YELLOW + "Install with: sudo apt install scrcpy -y" + RESET)
        return
    
    print(CYAN + "[*] Launching scrcpy..." + RESET)
    run_cmd("scrcpy")

def option_show_apk_list():
    """Opção 6: Lista todos os APKs instalados"""
    if not ensure_device_connected_prompt():
        return
    
    print(CYAN + "[*] Fetching installed packages..." + RESET)
    out, err = run_cmd("adb shell pm list packages -f", capture=True)
    
    if out:
        print(out)  # Exibe a lista
        save = input("\nDo you want to save the list to apk_list.txt? (y/n): ").strip().lower()
        if save == "y":
            with open("apk_list.txt", "w") as f:  # Salva em arquivo
                f.write(out + "\n")
            print(GREEN + "[+] Saved to ./apk_list.txt" + RESET)
    else:
        print(RED + "No output. Is device connected?" + RESET)

def option_take_screenshot():
    """Opção 7: Tira screenshot do dispositivo"""
    if not ensure_device_connected_prompt():
        return
    
    remote = "/sdcard/screen.png"
    local = "screen.png"
    
    print(CYAN + "[*] Taking screenshot..." + RESET)
    run_cmd(f"adb shell screencap -p {remote}")
    
    print(CYAN + "[*] Pulling screenshot..." + RESET)
    run_cmd(f"adb pull {remote} ./")
    
    print(GREEN + f"[+] Screenshot saved as ./{local}" + RESET)
    view = input("Do you want to open the screenshot now? (y/n): ").strip().lower()
    if view == "y":
        opener = shutil.which("xdg-open") or "xdg-open"
        run_cmd(f"{opener} {local}")

def option_power_off():
    """Opção 8: Desliga o dispositivo"""
    if not ensure_device_connected_prompt():
        return
    
    print(CYAN + "[*] Sending power off command..." + RESET)
    out, err = run_cmd("adb shell reboot -p", capture=True)
    
    if err:
        print(RED + "[-] Error powering off device:" + RESET)
        print(err)
    else:
        print(GREEN + "[+] Device is powering off." + RESET)

def option_install_apk():
    """Opção 9: Instala um APK no dispositivo"""
    if not ensure_device_connected_prompt():
        return
    
    apk_path = input("Enter path to APK file (e.g., ./app.apk): ").strip()
    if not os.path.isfile(apk_path):
        print(RED + "[-] File does not exist." + RESET)
        return
    
    print(CYAN + "[*] Installing APK..." + RESET)
    out, err = run_cmd(f"adb install {apk_path}", capture=True)
    
    if "Success" in out:
        print(GREEN + "[+] APK installed successfully." + RESET)
    else:
        print(RED + "[-] Failed to install APK:" + RESET)
        print(err or out)

def option_delete_apk():
    """Opção 10: Desinstala um APK/package"""
    if not ensure_device_connected_prompt():
        return
    
    package = input("Enter package name to uninstall (e.g., com.example.app): ").strip()
    if not package:
        print(RED + "[-] No package name provided." + RESET)
        return
    
    print(CYAN + "[*] Uninstalling package..." + RESET)
    out, err = run_cmd(f"adb uninstall {package}", capture=True)
    
    if "Success" in out:
        print(GREEN + "[+] Package uninstalled successfully." + RESET)
    else:
        print(RED + "[-] Failed to uninstall package:" + RESET)
        print(err or out)

def option_pull_file():
    """Opção 11: Baixa arquivo do dispositivo"""
    if not ensure_device_connected_prompt():
        return
    
    remote_path = input("Enter remote file path (e.g., /sdcard/file.txt): ").strip()
    local_path = input("Enter local destination path (e.g., ./file.txt): ").strip()
    
    if not remote_path or not local_path:
        print(RED + "[-] Both remote and local paths are required." + RESET)
        return
    
    print(CYAN + "[*] Pulling file..." + RESET)
    out, err = run_cmd(f"adb pull {remote_path} {local_path}", capture=True)
    
    if err and "error" in err.lower():
        print(RED + "[-] Failed to pull file:" + RESET)
        print(err)
    else:
        print(GREEN + f"[+] File pulled to {local_path}" + RESET)

def option_push_file():
    """Opção 12: Envia arquivo para o dispositivo"""
    if not ensure_device_connected_prompt():
        return
    
    local_path = input("Enter local file path (e.g., ./file.txt): ").strip()
    remote_path = input("Enter remote destination path (e.g., /sdcard/file.txt): ").strip()
    
    if not os.path.isfile(local_path):
        print(RED + "[-] Local file does not exist." + RESET)
        return
    if not remote_path:
        print(RED + "[-] Remote path is required." + RESET)
        return
    
    print(CYAN + "[*] Pushing file..." + RESET)
    out, err = run_cmd(f"adb push {local_path} {remote_path}", capture=True)
    
    if err and "error" in err.lower():
        print(RED + "[-] Failed to push file:" + RESET)
        print(err)
    else:
        print(GREEN + f"[+] File pushed to {remote_path}" + RESET)

def option_send_sms():
    """Opção 13: Envia SMS via intent"""
    if not ensure_device_connected_prompt():
        return
    
    phone_number = input("Enter phone number (e.g., +1234567890): ").strip()
    message = input("Enter message to send: ").strip()
    
    if not phone_number or not message:
        print(RED + "[-] Phone number and message are required." + RESET)
        return
    
    message = message.replace('"', '\\"')  # Escapa aspas
    print(CYAN + "[*] Sending SMS..." + RESET)
    out, err = run_cmd(f'adb shell am start -a android.intent.action.SENDTO -d sms:{phone_number} --es sms_body "{message}"', capture=True)
    
    if err:
        print(RED + "[-] Failed to send SMS:" + RESET)
        print(err)
    else:
        print(GREEN + "[+] SMS sent successfully." + RESET)

def option_dump_contacts():
    """Opção 14: Exporta contatos do dispositivo"""
    if not ensure_device_connected_prompt():
        return
    
    print(CYAN + "[*] Dumping contacts..." + RESET)
    out, err = run_cmd("adb shell content query --uri content://contacts/phones/", capture=True)
    
    if out:
        print(out)
        save = input("\nDo you want to save contacts to contacts.txt? (y/n): ").strip().lower()
        if save == "y":
            with open("contacts.txt", "w") as f:
                f.write(out + "\n")
            print(GREEN + "[+] Saved to ./contacts.txt" + RESET)
    else:
        print(RED + "[-] Failed to dump contacts:" + RESET)
        print(err or "No contacts found.")

def option_reboot_device():
    """Opção 15: Reinicia o dispositivo"""
    if not ensure_device_connected_prompt():
        return
    
    print(CYAN + "[*] Sending reboot command..." + RESET)
    out, err = run_cmd("adb shell reboot", capture=True)
    
    if err:
        print(RED + "[-] Error rebooting device:" + RESET)
        print(err)
    else:
        print(GREEN + "[+] Device is rebooting." + RESET)

def option_start_app():
    """Opção 16: Inicia um aplicativo específico"""
    if not ensure_device_connected_prompt():
        return
    
    package = input("Enter package name to start (e.g., com.example.app): ").strip()
    if not package:
        print(RED + "[-] Package name is required." + RESET)
        return
    
    print(CYAN + "[*] Starting application..." + RESET)
    out, err = run_cmd(f"adb shell monkey -p {package} 1", capture=True)
    
    if err:
        print(RED + "[-] Failed to start application:" + RESET)
        print(err)
    else:
        print(GREEN + "[+] Application started." + RESET)

def option_get_device_logs():
    """Opção 17: Obtém logs do dispositivo"""
    if not ensure_device_connected_prompt():
        return
    
    print(CYAN + "[*] Fetching device logs..." + RESET)
    filename = "device_log.txt"
    out, err = run_cmd(f"adb logcat -d > {filename}", capture=True)
    
    if os.path.isfile(filename):
        print(GREEN + f"[+] Logs saved to ./{filename}" + RESET)
        view = input("Do you want to open the logs now? (y/n): ").strip().lower()
        if view == "y":
            opener = shutil.which("xdg-open") or "xdg-open"
            run_cmd(f"{opener} {filename}")
    else:
        print(RED + "[-] Failed to fetch logs:" + RESET)
        print(err)

def option_toggle_wifi():
    """Opção 18: Liga/Desliga Wi-Fi"""
    if not ensure_device_connected_prompt():
        return
    
    state = input("Enter Wi-Fi state (enable/disable): ").strip().lower()
    if state not in ["enable", "disable"]:
        print(RED + "[-] Invalid state. Use 'enable' or 'disable'." + RESET)
        return
    
    print(CYAN + f"[*] {'Enabling' if state == 'enable' else 'Disabling'} Wi-Fi..." + RESET)
    cmd = f"adb shell svc wifi {state}"
    out, err = run_cmd(cmd, capture=True)
    
    if err:
        print(RED + f"[-] Failed to {state} Wi-Fi:" + RESET)
        print(err)
    else:
        print(GREEN + f"[+] Wi-Fi {state}d successfully." + RESET)

def option_check_storage():
    """Opção 19: Verifica informações de armazenamento"""
    if not ensure_device_connected_prompt():
        return
    
    print(CYAN + "[*] Checking storage info..." + RESET)
    out, err = run_cmd("adb shell df", capture=True)
    
    if out:
        print(out)
        save = input("\nDo you want to save storage info to storage_info.txt? (y/n): ").strip().lower()
        if save == "y":
            with open("storage_info.txt", "w") as f:
                f.write(out + "\n")
            print(GREEN + "[+] Saved to ./storage_info.txt" + RESET)
    else:
        print(RED + "[-] Failed to fetch storage info:" + RESET)
        print(err)

def option_take_photo():
    """Opção 20: Tira foto usando câmera"""
    if not ensure_device_connected_prompt():
        return
    
    print(CYAN + "[*] Opening Camera app..." + RESET)
    run_cmd("adb shell am start -a android.media.action.IMAGE_CAPTURE")
    time.sleep(3)  # Aguarda a câmera abrir
    
    print(CYAN + "[*] Capturing photo automatically..." + RESET)
    run_cmd("adb shell input keyevent 27")  # Keyevent 27 = shutter button
    time.sleep(2)  # Aguarda salvar
    
    print(CYAN + "[*] Finding latest photo..." + RESET)
    out, err = run_cmd("adb shell ls -t /sdcard/DCIM/Camera/ | head -1", capture=True)
    
    if not out.strip():
        print(RED + "[-] No photo found in DCIM/Camera." + RESET)
        return
    
    latest = out.strip()
    remote = f"/sdcard/DCIM/Camera/{latest}"
    local = latest
    
    print(CYAN + f"[*] Pulling {latest}..." + RESET)
    run_cmd(f"adb pull {remote} ./")
    
    if os.path.isfile(local):
        print(GREEN + f"[+] Photo saved as {local}" + RESET)
        view = input("Do you want to open the photo now? (y/n): ").strip().lower()
        if view == "y":
            opener = shutil.which("xdg-open") or "xdg-open"
            run_cmd(f"{opener} {local}")
    else:
        print(RED + "[-] Failed to pull photo." + RESET)

# ----------------- Menu / Main Loop -----------------
def show_menu():
    """Exibe o menu principal com todas as opções"""
    print()
    col_space = " " * 11
    print(YELLOW + f"[1] Check Device{col_space}    [2] Connect a Device{col_space}[3] Disconnect Device\n")
    print(YELLOW + f"[4] Screen Recording{col_space}[5] Screen Mirror{col_space}   [6] Show APK List\n")
    print(YELLOW + f"[7] Take Screenshot{col_space} [8] Power Off{col_space}       [9] Install APK\n")
    print(YELLOW + f"[10] Delete APK{col_space}     [11] Pull File{col_space}      [12] Push File\n")
    print(YELLOW + f"[13] Send SMS{col_space}       [14] Dump Contacts{col_space}  [15] Reboot Device\n")
    print(YELLOW + f"[16] Start App{col_space}      [17] Get Device Logs{col_space}[18] Toggle Wi-Fi\n")
    print(YELLOW + f"[19] Check Storage{col_space}  [20] Take Photo{col_space}     [q] Quit\n")
    print()

def dependencies_check():
    """Verifica e mostra as dependências necessárias"""
    print(CYAN + "[*] Checking dependencies..." + RESET)
    deps = [("adb", adb_available()), ("scrcpy", scrcpy_available())]
    for name, available in deps:
        if available:
            print(GREEN + f"[OK] {name} installed" + RESET)
        else:
            print(RED + f"[MISSING] {name} (install: sudo apt install {name} -y)" + RESET)

def main():
    """Função principal que gerencia o loop do programa"""
    print_banner()
    dependencies_check()
    
    while True:
        print()
        show_menu()
        choice = input(GREEN + "Select an option (1-20) or q to quit: " + RESET).strip().lower()
        
        if choice == "q":
            print(CYAN + "Exiting Pegasus. Stay ethical." + RESET)
            break
        
        # Dicionário mapeando opções para funções
        options = {
            "1": option_check_device,
            "2": option_connect_device,
            "3": option_disconnect_device,
            "4": option_screen_recording,
            "5": option_screen_mirror,
            "6": option_show_apk_list,
            "7": option_take_screenshot,
            "8": option_power_off,
            "9": option_install_apk,
            "10": option_delete_apk,
            "11": option_pull_file,
            "12": option_push_file,
            "13": option_send_sms,
            "14": option_dump_contacts,
            "15": option_reboot_device,
            "16": option_start_app,
            "17": option_get_device_logs,
            "18": option_toggle_wifi,
            "19": option_check_storage,
            "20": option_take_photo
        }
        
        if choice in options:
            options[choice]()  # Chama a função correspondente
        else:
            print(RED + "Invalid option. Choose 1-20 or q." + RESET)
        
        input("\nPress Enter to return to menu...")
        print_banner()

# Define run() function to encapsulate main functionality
def run():
    """Encapsula a função principal para tratamento de exceções"""
    try:
        main()
    except KeyboardInterrupt:  # Captura Ctrl+C
        print("\n" + CYAN + "Interrupted. Bye." + RESET)
        sys.exit(0)

if __name__ == "__main__":
    run()  # Executa o programa apenas se for script principal