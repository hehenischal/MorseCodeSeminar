const int buzzerPin = 9;  // Pin connected to the buzzer

void setup() {
  Serial.begin(9600);
  pinMode(buzzerPin, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    char c = Serial.read();
    Serial.write(c);
    switch (c) {
      case '1':
        // Dot: short beep
        digitalWrite(buzzerPin, HIGH);
        digitalWrite(LED_BUILTIN, HIGH);
        delay(200); // Adjust duration as needed
        digitalWrite(buzzerPin, LOW);
        digitalWrite(LED_BUILTIN, LOW);
        delay(1000); // Adjust pause between signals as needed
        break;
      case '2':
        // Dash: long beep
        digitalWrite(buzzerPin, HIGH);
        digitalWrite(LED_BUILTIN, HIGH);
        delay(2000); // Adjust duration as needed
        digitalWrite(buzzerPin, LOW);
        digitalWrite(LED_BUILTIN, LOW);
        delay(1000); // Adjust pause between signals as needed
        break;
      case ' ':
        // Space between characters
        delay(1000); // Adjust pause between characters as needed
        break;
      case '0':
        // Space between words
        delay(4000); // Adjust pause between words as needed
        break;
      default:
        
        break;
    }
  }
}
