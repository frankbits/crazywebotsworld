# Webots Installation und Setup-Anleitung 
## 1. Webots Installation

Lade den Webots-Installer herunter und folge den Installationsanweisungen:  
[Webots](https://cyberbotics.com/)

Für erste Schritte und eine Einführung in Webots:  
[Getting Started Guide](https://cyberbotics.com/doc/guide/getting-started-with-webots)

# 2. Den THA Branch dieses repositories clonen/herunterladen

Stelle sicher, dass du den **tha** Branch dieses Repositories klonst oder herunterlädst:

```bash
git clone -b tha https://github.com/DynamicSwarms/crazywebotsworld.git
```

# 3. Crazyflie Welt aus diesem Repository öffnen

Die Welt befinet sich in `crazywebotsworld/worlds/crazyflie.wbt`

❗ Achte darauf beim schließen/verändern der Welt diese nicht abzuspeichern, sodass Crazyflie und Zauberstab immer in Ursprungsposition starten. 

# 4. Controller für Crazyflie und Zauberstab (Wand) bauen

### Crazyflie Controller
1. Rechtsklick auf die Crazyflie im Scene-Tree und wähle **Edit Controller**.
2. Klicke auf das Zahnradsymbol über dem Codefenster, um den Controller zu bauen.
3. Wenn "Reset World?" erscheint, wähle **Reset**.

### Zauberstab Controller (Controllable Wand):
1. Wiederhole die oben genannten Schritte für den Zauberstab.

# 5. Externen Controller starten

Hilfreich, nicht notwendig:
[Externe Controller ausführen](https://cyberbotics.com/doc/guide/running-extern-robot-controllers?tab-os=windows)

Bei mehreren Webots-Instanzen im selben Netzwerk kann es sein, dass der Port von Webots automatisch angepasst wird. 
Der korrekte Port wird beim öffnen der Welt in der Webots-Console angezeigt.

### Windows:
1. Kopiere die Datei `webots-controller.exe` aus dem Pfad `C:\Program Files\Webots\msys64\mingw64\bin` in das `crazywebotsworld` Verzeichnis.
2. Controller starten:

   ```bash
   .\webots-controller.exe --protocol=tcp --ip-address=127.0.0.1 --port=1234 --robot-name=cf0_ros_ctrl .\crazyflie_example.py
   ```

### Linux

1. Setze den `WEBOTS_HOME` Pfad: 
    ```bash
    export WEBOTS_HOME=/usr/local/webots
    ```

2. Controller starten: 
    ```bash
    $WEBOTS_HOME/webots-controller --protocol=tcp --ip-address=127.0.0.1 --port=1234 --robot-name=cf0_ros_ctrl crazyflie_example.py
    ```

### macOS
1. Setze den `WEBOTS_HOME` Pfad: 
    ```bash
    export WEBOTS_HOME=/pfad/zu/webots
    ```
2. Controller starten: 
    ```bash
    $WEBOTS_HOME/Contents/MacOS/webots-controller --protocol=tcp --ip-address=127.0.0.1 --port=1234 --robot-name=cf0_ros_ctrl crazyflie_example.py
    ```








