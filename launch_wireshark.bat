@echo off
echo [*] Launching Multi-Agent DPI Engine (Wireshark)
echo [*] Target Interface: Wi-Fi
echo [*] Filter: tcp port 80 or tcp port 443
"C:\Program Files\Wireshark\Wireshark.exe" -i 4 -k
pause
