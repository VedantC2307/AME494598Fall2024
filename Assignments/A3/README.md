# Assignment 3: DHT11 Sensor with ESP32 and AWS EC2

## Due Date: Sep 30th, Before Midnight

## Overview
This assignment covers the following tasks:
1. Connecting a DHT11 sensor to the ESP32 and reading temperature and humidity values.
2. Sending the sensor data over HTTP to a server running on an AWS EC2 instance.
3. Configuring the EC2 server to receive test data using an HTTP server.

## Tasks Breakdown
### 1. Connecting the DHT11 Sensor to the ESP32
- **Hardware Setup:** 
  - Connect the DHT11 sensor to the ESP32 as follows:
    - VCC (3.3V) on DHT11 to 3V3 on ESP32.
    - GND on DHT11 to GND on ESP32.
    - DATA on DHT11 to any GPIO pin on ESP32 (e.g., GPIO 4).
  - Note: Make sure to use a pull-up resistor (10kΩ) between the DATA and VCC lines.
- **Code:**
  - The provided code reads temperature and humidity values from the DHT11 sensor using the ESP32.
  - The Arduino code is available in the repository: [DHT11Default.ino](https://github.com/VedantC2307/AME494598Fall2024/tree/main/Assignments/A3/DHT11Default/DHT11Default.ino).

### 2. Sending Data Over HTTP to an AWS EC2 Instance
- The ESP32 code sends the sensor data over HTTP POST requests to the server hosted on the EC2 instance.
- **Code Details:**
  - The ESP32 connects to a Wi-Fi network.
  - It sends an HTTP POST request containing the temperature and humidity data to the EC2 server's IP address and port.
  - Code available in the repository.
  
### 3. Configuring the EC2 Server to Receive Data
- The AWS EC2 instance is set up to receive HTTP POST requests.
- **Steps:**
  1. Install a simple HTTP server using `http-server` on the EC2 instance.
  2. Configure the EC2 security group to allow incoming HTTP traffic on the required port.
  3. Run the HTTP server and listen for incoming data from the ESP32.
- Screenshots of the configuration and code details are included in the repository.

## Resources
- [DHT11Default.ino](https://github.com/VedantC2307/AME494598Fall2024/tree/main/Assignments/A3/DHT11Default/DHT11Default.ino)
- Additional resources used during the assignment are linked in the [assignment description](https://gist.github.com/tejaswigowda/f289e9bff13d152876e8d4b3281142f8).

## How to Run the Project
1. Connect the DHT11 sensor to the ESP32 as per the wiring instructions.
2. Flash the `DHT11Default.ino` code to the ESP32.
3. On the EC2 instance, start the HTTP server to listen for incoming data.
4. The ESP32 will automatically send temperature and humidity data to the EC2 server at regular intervals.

## Acknowledgments
- The assignment description and additional resources are provided by the course.
