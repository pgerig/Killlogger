# Hardware Keylogger

**ADVERTENCIA: Este repositorio es exclusivamente para fines educativos y pruebas en entornos controlados.**

### Qué hace
- Captura todas las teclas pulsadas en Windows
- Las envía en tiempo real a un Arduino (o clon CH340) conectado por USB
- Totalmente silencioso cuando se compila con `--noconsole --windowed`
- Incluye combinación de salida: **Ctrl + Shift + G**

### Requisitos
- Windows 10/11
- Python 3.12 + pywin32 + pyserial
- Arduino Uno / Nano / clon CH340

### Uso rápido
1. Conecta el Arduino con el sketch `Keylog.ino`
2. Ejecuta `keylog.py` o el ya compilado `keylog_compiled.exe`
3. Todo lo que escribas aparecerá en el Monitor Serie (9600 baudios)

### Compilar tú mismo (recomendado)
```bat
compile.bat
