"""
Script de pruebas para el sistema bancario
"""

import sys
import os

# Agregar el directorio actual al path para importar el módulo
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sistema_bancario import *

def test_creacion_cuentas():
    """Prueba la creación de diferentes tipos de cuentas"""
    print("=== TEST: Creación de Cuentas ===")
    
    # Crear cuentas de prueba
    cuenta_ahorro = CuentaAhorro("Ana Test", 1500000)
    cuenta_corriente = CuentaCorriente("Pedro Test", 800000, 150000)
    cuenta_inversion = CuentaInversion("Laura Test", 3000000)
    
    print("✓ Cuentas creadas exitosamente")
    print(f"  {cuenta_ahorro}")
    print(f"  {cuenta_corriente}")
    print(f"  {cuenta_inversion}")

def test_operaciones_basicas():
    """Prueba operaciones básicas de depósito y retiro"""
    print("\n=== TEST: Operaciones Básicas ===")
    
    cuenta = CuentaAhorro("Test Operaciones", 1000000)
    print(f"Saldo inicial: ${cuenta.get_saldo():,.2f}")
    
    # Depósito
    cuenta.depositar(500000)
    print(f"Después de depósito: ${cuenta.get_saldo():,.2f}")
    
    # Retiro
    cuenta.retirar(200000)
    print(f"Después de retiro: ${cuenta.get_saldo():,.2f}")
    
    print("✓ Operaciones básicas completadas")

def test_sobregiro():
    """Prueba del sobregiro en cuenta corriente"""
    print("\n=== TEST: Sobregiro Cuenta Corriente ===")
    
    cuenta = CuentaCorriente("Test Sobregiro", 50000, 100000)
    print(f"Saldo inicial: ${cuenta.get_saldo():,.2f}")
    
    # Retiro dentro del límite
    if cuenta.retirar(120000):
        print(f"Retiro exitoso. Saldo: ${cuenta.get_saldo():,.2f}")
    else:
        print("Retiro fallido")
    
    # Retiro excediendo límite
    if cuenta.retirar(50000):
        print(f"Retiro exitoso. Saldo: ${cuenta.get_saldo():,.2f}")
    else:
        print("Retiro fallido (límite excedido)")

def test_transferencias():
    """Prueba transferencias entre cuentas"""
    print("\n=== TEST: Transferencias ===")
    
    cuenta1 = CuentaAhorro("Origen Test", 2000000)
    cuenta2 = CuentaCorriente("Destino Test", 500000)
    
    print(f"Saldo origen antes: ${cuenta1.get_saldo():,.2f}")
    print(f"Saldo destino antes: ${cuenta2.get_saldo():,.2f}")
    
    # Simular transferencia
    print("Simulando transferencia de 300,000...")
    if cuenta1.retirar(300000) and cuenta2.depositar(300000):
        print("Transferencia manual exitosa")
    
    print(f"Saldo origen después: ${cuenta1.get_saldo():,.2f}")
    print(f"Saldo destino después: ${cuenta2.get_saldo():,.2f}")

def test_polimorfismo():
    """Prueba el polimorfismo con diferentes tipos de cuentas"""
    print("\n=== TEST: Polimorfismo ===")
    
    cuentas = [
        CuentaAhorro("Polimorfismo 1", 1000000),
        CuentaCorriente("Polimorfismo 2", 500000),
        CuentaInversion("Polimorfismo 3", 2000000)
    ]
    
    print("Aplicando operaciones mensuales:")
    procesar_cuentas(cuentas)
    
    print("\nEstado final:")
    for cuenta in cuentas:
        print(f"  {cuenta}")

def test_comparacion():
    """Prueba la comparación de saldos"""
    print("\n=== TEST: Comparación de Saldos ===")
    
    cuenta1 = CuentaAhorro("Comparación 1", 1500000)
    cuenta2 = CuentaAhorro("Comparación 2", 800000)
    
    print(f"Cuenta 1: ${cuenta1.get_saldo():,.2f}")
    print(f"Cuenta 2: ${cuenta2.get_saldo():,.2f}")
    
    if cuenta1 > cuenta2:
        print("✓ Cuenta 1 tiene mayor saldo")
    else:
        print("✓ Cuenta 2 tiene mayor saldo")

def test_inversiones():
    """Prueba funcionalidades específicas de cuenta de inversión"""
    print("\n=== TEST: Cuenta de Inversión ===")
    
    cuenta = CuentaInversion("Inversor Test", 5000000)
    print(f"Saldo inicial: ${cuenta.get_saldo():,.2f}")
    
    # Invertir en portafolio
    if cuenta.invertir_en_portafolio(1000000, 500000, 500000):
        print("✓ Inversión en portafolio exitosa")
        print(f"Saldo después de inversión: ${cuenta.get_saldo():,.2f}")
    
    # Calcular rendimiento
    rendimiento = cuenta.calcular_interes()
    print(f"Rendimiento aplicado: ${rendimiento:,.2f}")
    print(f"Saldo final: ${cuenta.get_saldo():,.2f}")

def ejecutar_todas_las_pruebas():
    """Ejecuta todas las pruebas del sistema"""
    print("INICIANDO PRUEBAS DEL SISTEMA BANCARIO")
    print("=" * 50)
    
    try:
        test_creacion_cuentas()
        test_operaciones_basicas()
        test_sobregiro()
        test_transferencias()
        test_polimorfismo()
        test_comparacion()
        test_inversiones()
        
        print("\n" + "=" * 50)
        print("✓ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
        print("\nRevisa el archivo 'transacciones.log' para ver el registro detallado")
        
    except Exception as e:
        print(f"\n✗ Error durante las pruebas: {e}")
        return False
    
    return True

if __name__ == "__main__":
    ejecutar_todas_las_pruebas()