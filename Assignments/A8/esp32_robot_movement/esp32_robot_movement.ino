// // Pin Definitions (ESP32-S3 Feather)
// #define FL_IN1 9   // Front Left IN1
// #define FL_IN2 10   // Front Left IN2
// #define FL_ENA 11   // Front Left PWM

// #define FR_IN1 5   // Front Right IN1
// #define FR_IN2 6    // Front Right IN2
// #define FR_ENA 4    // Front Right PWM

// #define RL_IN1 16    // Rear Left IN1
// #define RL_IN2 17    // Rear Left IN2
// #define RL_ENA 18    // Rear Left PWM

// #define RR_IN1 14   // Rear Right IN1
// #define RR_IN2 15   // Rear Right IN2
// #define RR_ENA 8   // Rear Right PWM

// void setup() {
//   // Configure pins as outputs
//   pinMode(FL_IN1, OUTPUT);
//   pinMode(FL_IN2, OUTPUT);
//   pinMode(FL_ENA, OUTPUT);

//   pinMode(FR_IN1, OUTPUT);
//   pinMode(FR_IN2, OUTPUT);
//   pinMode(FR_ENA, OUTPUT);

//   pinMode(RL_IN1, OUTPUT);
//   pinMode(RL_IN2, OUTPUT);
//   pinMode(RL_ENA, OUTPUT);

//   pinMode(RR_IN1, OUTPUT);
//   pinMode(RR_IN2, OUTPUT);
//   pinMode(RR_ENA, OUTPUT);
// }

// void loop() {
//   // Move forward
//   moveForward(100);
//   delay(5000);

// }

// void moveForward(int speed) {
//   // All wheels move forward
//   analogWrite(FL_ENA, speed);
//   digitalWrite(FL_IN1, HIGH);
//   digitalWrite(FL_IN2, LOW);

//   analogWrite(FR_ENA, speed);
//   digitalWrite(FR_IN1, HIGH);
//   digitalWrite(FR_IN2, LOW);

//   analogWrite(RL_ENA, speed);
//   digitalWrite(RL_IN1, HIGH);
//   digitalWrite(RL_IN2, LOW);

//   analogWrite(RR_ENA, speed);
//   digitalWrite(RR_IN1, LOW);
//   digitalWrite(RR_IN2, HIGH);
// }






// Pin Definitions for ESP32-S3 Feather with L298N
#define FL_IN1 9   // Front Left IN1
#define FL_IN2 10  // Front Left IN2
#define FL_ENA 11  // Front Left PWM

#define FR_IN1 5   // Front Right IN1
#define FR_IN2 6   // Front Right IN2
#define FR_ENA 4   // Front Right PWM

#define RL_IN1 16  // Rear Left IN1
#define RL_IN2 17  // Rear Left IN2
#define RL_ENA 18  // Rear Left PWM

#define RR_IN1 14  // Rear Right IN1
#define RR_IN2 15  // Rear Right IN2
#define RR_ENA 8   // Rear Right PWM

// Define PWM Parameters
const int pwmFreq = 1000;          // PWM frequency
const int pwmResolution = 8;      // PWM resolution (8 bits = 0 to 255)

// Define PWM channels for motors
const int pwmFL = 0;  // Front Left
const int pwmFR = 1;  // Front Right
const int pwmRL = 2;  // Rear Left
const int pwmRR = 3;  // Rear Right

// Define Direction Byte for Mecanum Modes
const byte MEC_STRAIGHT_FORWARD = B10101010;
const byte MEC_STRAIGHT_BACKWARD = B01010101;
const byte MEC_SIDEWAYS_RIGHT = B01101001;
const byte MEC_SIDEWAYS_LEFT = B10010110;
const byte MEC_ROTATE_CLOCKWISE = B01100110;
const byte MEC_ROTATE_COUNTERCLOCKWISE = B10011001;

// Define PWM Motor Speed Variables
int rf_PWM = 100;  // Right Front Motor
int lf_PWM = 100;  // Left Front Motor
int rr_PWM = 100;  // Right Rear Motor
int lr_PWM = 100;  // Left Front Motor


void setup() {
  // Configure motor control pins as outputs
  pinMode(FL_IN1, OUTPUT);
  pinMode(FL_IN2, OUTPUT);
  pinMode(FL_ENA, OUTPUT);

  pinMode(FR_IN1, OUTPUT);
  pinMode(FR_IN2, OUTPUT);
  pinMode(FR_ENA, OUTPUT);

  pinMode(RL_IN1, OUTPUT);
  pinMode(RL_IN2, OUTPUT);
  pinMode(RL_ENA, OUTPUT);

  pinMode(RR_IN1, OUTPUT);
  pinMode(RR_IN2, OUTPUT);
  pinMode(RR_ENA, OUTPUT);

  // Setup PWM channels
  ledcSetup(pwmFL, pwmFreq, pwmResolution);
  ledcSetup(pwmFR, pwmFreq, pwmResolution);
  ledcSetup(pwmRL, pwmFreq, pwmResolution);
  ledcSetup(pwmRR, pwmFreq, pwmResolution);

  // Attach PWM channels to motor enable pins
  ledcAttachPin(FL_ENA, pwmFL);
  ledcAttachPin(FR_ENA, pwmFR);
  ledcAttachPin(RL_ENA, pwmRL);
  ledcAttachPin(RR_ENA, pwmRR);
}

void loop() {
  // Test different movements
  moveMotors(150,150, 150, 150, MEC_STRAIGHT_FORWARD); // Move Forward
  delay(2000);
  stopMotors();
  delay(1000);

  // moveMotors(200, 200, 200, 200, MEC_STRAIGHT_BACKWARD); // Move Backward
  // delay(2000);
  // stopMotors();
  // delay(1000);

  // // moveMotors(200, 200, 200, 200, MEC_SIDEWAYS_RIGHT); // Move Sideways Right
  // // delay(2000);
  // // stopMotors();
  // // delay(1000);

  moveMotors(lf_PWM, rf_PWM, lr_PWM, rr_PWM, MEC_ROTATE_CLOCKWISE); // Rotate Clockwise
  delay(3000);
  stopMotors();
  delay(15000);
}

// Function to move motors
void moveMotors(int speedFL, int speedFR, int speedRL, int speedRR, byte direction) {
  // Front Left Motor
  digitalWrite(FL_IN1, bitRead(direction, 7));
  digitalWrite(FL_IN2, bitRead(direction, 6));
  ledcWrite(pwmFL, abs(speedFL));

  // Front Right Motor
  digitalWrite(FR_IN1, bitRead(direction, 5));
  digitalWrite(FR_IN2, bitRead(direction, 4));
  ledcWrite(pwmFR, abs(speedFR));

  // Rear Left Motor
  digitalWrite(RL_IN1, bitRead(direction, 3));
  digitalWrite(RL_IN2, bitRead(direction, 2));
  ledcWrite(pwmRL, abs(speedRL));

  // Rear Right Motor
  digitalWrite(RR_IN1, bitRead(direction, 1));
  digitalWrite(RR_IN2, bitRead(direction, 0));
  ledcWrite(pwmRR, abs(speedRR));
}

// Function to stop all motors
void stopMotors() {
  // Stop all motors
  ledcWrite(pwmFL, 0);
  ledcWrite(pwmFR, 0);
  ledcWrite(pwmRL, 0);
  ledcWrite(pwmRR, 0);

  digitalWrite(FL_IN1, LOW);
  digitalWrite(FL_IN2, LOW);
  digitalWrite(FR_IN1, LOW);
  digitalWrite(FR_IN2, LOW);
  digitalWrite(RL_IN1, LOW);
  digitalWrite(RL_IN2, LOW);
  digitalWrite(RR_IN1, LOW);
  digitalWrite(RR_IN2, LOW);
}
