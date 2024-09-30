#include <Arduino.h>

const int rele1 = 2;
const int rele2 = 4;

unsigned long lastActivationTime = 0;
bool isActive = false;
bool specialActivate = false;
bool specialDeactivate = false;

void setup() {
    Serial.begin(9600);
    pinMode(rele1, OUTPUT);
    pinMode(rele2, OUTPUT);
    
    // Desativa os relés ao iniciar
    digitalWrite(rele1, HIGH);
    digitalWrite(rele2, HIGH);
}

void loop() {
    if (Serial.available()) {
        String command = Serial.readStringUntil('\n');
        
        if (command.equals("ativar") && !isActive && !specialDeactivate) {
            // Verifica se já passaram 10 segundos desde a última ativação
            if (millis() - lastActivationTime >= 10000) {
                ativarRele();
            }
        } else if (command.equals("desativar") && isActive && (millis() - lastActivationTime >= 10000 || specialActivate)) {
            desativarRele();
        } else if (command.equals("ativar_especial")) {
            specialActivate = true;
            ativarRele();
        } else if (command.equals("desativar_especial")) {
            specialDeactivate = true;
            desativarRele();
        }
    }

    // Reseta o estado especial após a desativação
    if (isActive && (millis() - lastActivationTime >= 10000)) {
        specialActivate = false;
        specialDeactivate = false;
    }
}

void ativarRele() {
    digitalWrite(rele1, LOW);
    digitalWrite(rele2, LOW);
    isActive = true;
    lastActivationTime = millis();
    Serial.println("Relés ativados!");
}

void desativarRele() {
    digitalWrite(rele1, HIGH);
    digitalWrite(rele2, HIGH);
    isActive = false;
    Serial.println("Relés desativados!");
}
