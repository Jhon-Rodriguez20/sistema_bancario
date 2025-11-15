# 🏦 Sistema Bancario en Python

## 📋 Descripción
Sistema bancario completo desarrollado en Python que implementa herencia, polimorfismo y sobrescritura de operadores para gestionar diferentes tipos de cuentas bancarias con operaciones especializadas.

## ✨ Características
✅ Tres tipos de cuentas: Ahorro, Corriente e Inversión

✅ Herencia y polimorfismo con clase abstracta

✅ Sobrecarga de operadores para transferencias y comparaciones

✅ Sistema de logs automático

✅ Menú interactivo fácil de usar

✅ Validaciones y manejo de errores

## 🛠️ Requisitos
Python 3.8 o superior

No se requieren librerías externas

## 🚀 Instalación y Ejecución
1. Clonar o descargar los archivos:
sistema_bancario.py
test_sistema.py

2. Ejecutar el sistema principal:
python sistema_bancario.py

3. Ejecutar pruebas (opcional):
python test_sistema.py

📊 Tipos de Cuentas
💰 Cuenta de Ahorro
Interés anual: 2%

Sin comisiones de mantenimiento

Ideal para ahorro a largo plazo

💳 Cuenta Corriente
Límite de sobregiro configurable

Comisión mensual: $5,000

Flexibilidad para operaciones diarias

📈 Cuenta de Inversión
Rendimiento variable: -5% a +15%

Portafolio de inversión (acciones, bonos, fondos)

Comisión de gestión: 1%

🎮 Guía de Uso
Menú Principal
Al ejecutar el sistema verás este menú:

==================================================
        SISTEMA BANCARIO
==================================================
1. Crear nueva cuenta
2. Depositar
3. Retirar
4. Transferir entre cuentas
5. Comparar saldos
6. Mostrar estado de cuentas
7. Procesar operaciones mensuales
8. Salir
==================================================

1. Crear Nueva Cuenta
Pasos:

Selecciona opción 1

Elige tipo de cuenta (1: Ahorro, 2: Corriente, 3: Inversión)

Ingresa nombre del titular

Ingresa saldo inicial

Para cuenta corriente: define límite de sobregiro

2. Depositar Fondos
Pasos:

Selecciona opción 2

Elige cuenta destino usando el NÚMERO:

0. CuentaAhorro-1000 - Juan Pérez
1. CuentaCorriente-1001 - María García
→ Escribe: 0 (para Juan Pérez)
Ingresa monto a depositar

3. Retirar Fondos
Pasos:

Selecciona opción 3

Elige cuenta origen usando el NÚMERO

Ingresa monto a retirar

Nota: Cuenta corriente permite sobregiro hasta el límite

4. Transferir entre Cuentas
Pasos:

Selecciona opción 4

Elige cuenta origen (número)

Elige cuenta destino (número)

Ingresa monto a transferir

Característica: Usa sobrecarga del operador +

5. Comparar Saldos
Pasos:

Selecciona opción 5

Elige primera cuenta (número)

Elige segunda cuenta (número)

Resultado: Muestra qué cuenta tiene mayor saldo

6. Mostrar Estado
Pasos:

Selecciona opción 6

Muestra: Todas las cuentas con saldos actualizados

7. Procesar Operaciones Mensuales
Pasos:

Selecciona opción 7

Aplica automáticamente:

Intereses en cuentas de ahorro

Rendimientos en cuentas de inversión

Comisiones en cuentas corrientes