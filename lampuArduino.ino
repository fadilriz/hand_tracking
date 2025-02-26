int led1 = 9;  // LED 1 (Merah)
int led2 = 10; // LED 2 (Kuning)
int led3 = 11; // LED 3 (Hijau)

void setup() {
    pinMode(led1, OUTPUT);
    pinMode(led2, OUTPUT);
    pinMode(led3, OUTPUT);
    Serial.begin(9600);
}

void loop() {
    if (Serial.available() > 0) {
        char command = Serial.read(); // Baca data dari laptop
        int jari = command - '0'; // Konversi dari karakter ke integer

        // Atur LED berdasarkan jumlah jari yang diangkat
        digitalWrite(led1, jari >= 1 ? HIGH : LOW);
        digitalWrite(led2, jari >= 2 ? HIGH : LOW);
        digitalWrite(led3, jari >= 3 ? HIGH : LOW);
    }
}
