# Smart Insole Project

###### This project aimed to design a system capable of displaying the real-time pressure distribution under a foot. The  portable system is attached to the user's ankle and it integrates an insole I found online. The insole contains 16 force sensors whose electrical resistance is inversely proportional to the applied pressure. By measuring the voltage of a sensor, the force can be estimated using the resistance-force curve provided by the manufacturer.

###### The 16 voltages are periodically measured using an ESP-32 and a 16:1 multiplexer. The data is then sent to the destination computer via Bluetooth BLE (in the PressureSole_BT.ino script). The system is powered by a 6V battery through the ESP-32's internal voltage regulator.

###### On the destination computer, the script RealTimePressure.py receives the data via Bluetooth and displays it in real time using an OpenCV window, which is refreshed periodically. On average, the display is updated  14 times per second, with virtually no latency between foot movement and the displayed image.

## Hardware used

### Insole: 
##### https://film-sensor.com/product/pressure-mapping-fs-ins-16z/

### ESP32-­WROOM­-32D:
##### https://www.amazon.ca/ESP-WROOM-32-NodeMCU-Bluetooth-Development-Microcontroller/dp/B0CHBMFJBQ/ref=asc_df_B0CHBMFJBQ/?tag=googleshopc0c-20&linkCode=df0&hvadid=706724917350&hvpos=&hvnetw=g&hvrand=715331247207770120&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9061022&hvtargid=pla-2296980982282&mcid=e5815f314ce13fcb83038a545092174f&gad_source=1&th=1

### 16:1 multiplexer:
##### https://www.digikey.ca/en/products/detail/sparkfun-electronics/BOB-09056/5673767

### FFC connector:
##### https://www.digikey.ca/en/products/detail/gct/FFC3B07-20-T/10657038

### Resistors:
##### https://www.digikey.ca/en/products/detail/yageo/RC0603FR-13430KL/17012744



