import datetime
from abc import ABC, abstractmethod
from typing import List, Dict
import logging

# Configuración del sistema de logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('transacciones.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# --------------------------------------------------------------
# Clase CuentaBancaria
# --------------------------------------------------------------
class CuentaBancaria(ABC):
    _contador_cuentas = 1000
    
    def __init__(self, titular: str, saldo_inicial: float = 0):
        self._numero_cuenta = f"{self.__class__.__name__}-{CuentaBancaria._contador_cuentas}"
        CuentaBancaria._contador_cuentas += 1
        self._titular = titular
        self._saldo = saldo_inicial
        self._fecha_apertura = datetime.datetime.now()
        self._transacciones = []
        self._registrar_transaccion("Apertura de cuenta", saldo_inicial)
    
    def _registrar_transaccion(self, tipo: str, monto: float):
        transaccion = {
            'fecha': datetime.datetime.now(),
            'tipo': tipo,
            'monto': monto,
            'saldo_anterior': self._saldo
        }
        self._transacciones.append(transaccion)
        logging.info(f"{self._numero_cuenta} - {tipo}: ${monto:,.2f}")
    
    @abstractmethod
    def calcular_interes(self) -> float:
        pass
    
    @abstractmethod
    def aplicar_comision(self) -> float:
        pass
    
    def depositar(self, monto: float) -> bool:
        if monto > 0:
            self._saldo += monto
            self._registrar_transaccion("Depósito", monto)
            return True
        return False
    
    def retirar(self, monto: float) -> bool:
        if monto > 0 and self._saldo >= monto:
            self._saldo -= monto
            self._registrar_transaccion("Retiro", -monto)
            return True
        return False
    
    def get_saldo(self) -> float:
        return self._saldo
    
    def get_numero_cuenta(self) -> str:
        return self._numero_cuenta
    
    def get_titular(self) -> str:
        return self._titular
    
    # Sobrecarga del operador + para transferencias
    def __add__(self, otra_cuenta) -> bool:
        if isinstance(otra_cuenta, CuentaBancaria):
            monto = float(input(f"Ingrese monto a transferir de {self._numero_cuenta} a {otra_cuenta.get_numero_cuenta()}: "))
            if self.retirar(monto):
                if otra_cuenta.depositar(monto):
                    self._registrar_transaccion(f"Transferencia enviada a {otra_cuenta.get_numero_cuenta()}", -monto)
                    otra_cuenta._registrar_transaccion(f"Transferencia recibida de {self._numero_cuenta}", monto)
                    return True
                else:
                    # Revertir si el depósito falla
                    self.depositar(monto)
        return False
    
    # Sobrecarga del operador > para comparar saldos
    def __gt__(self, otra_cuenta) -> bool:
        if isinstance(otra_cuenta, CuentaBancaria):
            return self._saldo > otra_cuenta.get_saldo()
        return False
    
    def __str__(self) -> str:
        return f"{self._numero_cuenta}: Titular: {self._titular}, Saldo: ${self._saldo:,.2f}"

# --------------------------------------------------------------
# Clases CuentaAhorro
# --------------------------------------------------------------
class CuentaAhorro(CuentaBancaria):
    TASA_INTERES = 0.02  # 2% anual
    
    def __init__(self, titular: str, saldo_inicial: float = 0):
        super().__init__(titular, saldo_inicial)
    
    def calcular_interes(self) -> float:
        interes = self._saldo * self.TASA_INTERES
        self._saldo += interes
        self._registrar_transaccion("Interés aplicado", interes)
        return interes
    
    def aplicar_comision(self) -> float:
        # Cuentas de ahorro no tienen comisión
        return 0
    
    def __str__(self) -> str:
        return f"{super().__str__()} (Interés: {self.TASA_INTERES*100}%)"
    

# --------------------------------------------------------------
# Clases CuentaCorriente
# --------------------------------------------------------------
class CuentaCorriente(CuentaBancaria):
    def __init__(self, titular: str, saldo_inicial: float = 0, limite_sobregiro: float = 100000):
        super().__init__(titular, saldo_inicial)
        self._limite_sobregiro = limite_sobregiro
        self._comision_mantenimiento = 5000  # $5,000 mensuales
    
    def retirar(self, monto: float) -> bool:
        if monto > 0 and (self._saldo - monto) >= -self._limite_sobregiro:
            self._saldo -= monto
            self._registrar_transaccion("Retiro", -monto)
            return True
        return False
    
    def calcular_interes(self) -> float:
        # Cuentas corrientes no generan interés
        return 0
    
    def aplicar_comision(self) -> float:
        if self._saldo >= self._comision_mantenimiento:
            self._saldo -= self._comision_mantenimiento
            self._registrar_transaccion("Comisión mantenimiento", -self._comision_mantenimiento)
            return self._comision_mantenimiento
        return 0
    
    def __str__(self) -> str:
        sobregiro_info = " (Sobregiro usado)" if self._saldo < 0 else ""
        return f"{super().__str__()}{sobregiro_info}"


# --------------------------------------------------------------
# Clases CuentaInversion
# --------------------------------------------------------------
class CuentaInversion(CuentaBancaria):
    def __init__(self, titular: str, saldo_inicial: float = 0):
        super().__init__(titular, saldo_inicial)
        self._portafolio = {
            'acciones': 0.0,
            'bonos': 0.0,
            'fondos': 0.0
        }
        self._rendimiento_anual = 0.0
    
    def calcular_interes(self) -> float:
        # Simular rendimiento variable entre -5% y +15%
        import random
        self._rendimiento_anual = random.uniform(-0.05, 0.15)
        rendimiento = self._saldo * self._rendimiento_anual
        self._saldo += rendimiento
        self._registrar_transaccion("Rendimiento inversión", rendimiento)
        return rendimiento
    
    def aplicar_comision(self) -> float:
        comision = self._saldo * 0.01  # 1% de comisión por gestión
        if self._saldo >= comision:
            self._saldo -= comision
            self._registrar_transaccion("Comisión gestión", -comision)
            return comision
        return 0
    
    def invertir_en_portafolio(self, accion: float, bono: float, fondo: float):
        total = accion + bono + fondo
        if total <= self._saldo:
            self._portafolio['acciones'] += accion
            self._portafolio['bonos'] += bono
            self._portafolio['fondos'] += fondo
            self._saldo -= total
            self._registrar_transaccion("Inversión en portafolio", -total)
            return True
        return False
    
    def __str__(self) -> str:
        rendimiento_str = f" (Rendimiento: {self._rendimiento_anual*100:+.1f}%)" if hasattr(self, '_rendimiento_anual') else ""
        return f"{super().__str__()}{rendimiento_str}"

# Función polimórfica
def procesar_cuentas(cuentas: List[CuentaBancaria]):
    print("\n--- PROCESANDO OPERACIONES MENSUALES ---")
    for cuenta in cuentas:
        print(f"\nProcesando {cuenta.get_numero_cuenta()}:")
        interes = cuenta.calcular_interes()
        if interes != 0:
            print(f"  Interés/Rendimiento aplicado: ${interes:,.2f}")
        
        comision = cuenta.aplicar_comision()
        if comision != 0:
            print(f"  Comisión aplicada: ${comision:,.2f}")
        
        print(f"  Saldo final: ${cuenta.get_saldo():,.2f}")

# Menú interactivo
def mostrar_menu():
    print("\n" + "="*50)
    print("        SISTEMA BANCARIO")
    print("="*50)
    print("1. Crear nueva cuenta")
    print("2. Depositar")
    print("3. Retirar")
    print("4. Transferir entre cuentas")
    print("5. Comparar saldos")
    print("6. Mostrar estado de cuentas")
    print("7. Procesar operaciones mensuales")
    print("8. Salir")
    print("="*50)

def main():
    cuentas = []
    
    # Crear algunas cuentas de ejemplo
    cuentas.append(CuentaAhorro("Juan Pérez", 1000000))
    cuentas.append(CuentaCorriente("María García", 500000, 200000))
    cuentas.append(CuentaInversion("Carlos López", 5000000))
    
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            print("\n--- CREAR NUEVA CUENTA ---")
            print("1. Cuenta de Ahorro")
            print("2. Cuenta Corriente")
            print("3. Cuenta de Inversión")
            tipo = input("Seleccione tipo de cuenta: ")
            
            titular = input("Nombre del titular: ")
            try:
                saldo = float(input("Saldo inicial: "))
            except ValueError:
                print("Error: Saldo debe ser un número válido")
                continue
            
            if tipo == "1":
                cuenta = CuentaAhorro(titular, saldo)
            elif tipo == "2":
                try:
                    limite = float(input("Límite de sobregiro: "))
                except ValueError:
                    limite = 100000
                cuenta = CuentaCorriente(titular, saldo, limite)
            elif tipo == "3":
                cuenta = CuentaInversion(titular, saldo)
            else:
                print("Opción inválida")
                continue
            
            cuentas.append(cuenta)
            print(f"Cuenta creada exitosamente: {cuenta}")
        
        elif opcion == "2":
            print("\n--- DEPOSITAR ---")
            if not cuentas:
                print("No hay cuentas creadas")
                continue
            
            for i, cuenta in enumerate(cuentas):
                print(f"{i}. {cuenta.get_numero_cuenta()} - {cuenta.get_titular()}")
            
            try:
                idx = int(input("Seleccione cuenta: "))
                monto = float(input("Monto a depositar: "))
                if cuentas[idx].depositar(monto):
                    print("Depósito exitoso")
                else:
                    print("Error en el depósito")
            except (ValueError, IndexError):
                print("Selección inválida")
        
        elif opcion == "3":
            print("\n--- RETIRAR ---")
            if not cuentas:
                print("No hay cuentas creadas")
                continue
            
            for i, cuenta in enumerate(cuentas):
                print(f"{i}. {cuenta.get_numero_cuenta()} - {cuenta.get_titular()}")
            
            try:
                idx = int(input("Seleccione cuenta: "))
                monto = float(input("Monto a retirar: "))
                if cuentas[idx].retirar(monto):
                    print("Retiro exitoso")
                else:
                    print("Fondos insuficientes o monto inválido")
            except (ValueError, IndexError):
                print("Selección inválida")
        
        elif opcion == "4":
            print("\n--- TRANSFERIR ---")
            if len(cuentas) < 2:
                print("Se necesitan al menos 2 cuentas")
                continue
            
            for i, cuenta in enumerate(cuentas):
                print(f"{i}. {cuenta.get_numero_cuenta()} - {cuenta.get_titular()}")
            
            try:
                idx_origen = int(input("Seleccione cuenta origen: "))
                idx_destino = int(input("Seleccione cuenta destino: "))
                
                if cuentas[idx_origen] + cuentas[idx_destino]:
                    print("Transferencia exitosa")
                else:
                    print("Transferencia fallida")
            except (ValueError, IndexError):
                print("Selección inválida")
        
        elif opcion == "5":
            print("\n--- COMPARAR SALDOS ---")
            if len(cuentas) < 2:
                print("Se necesitan al menos 2 cuentas")
                continue
            
            for i, cuenta in enumerate(cuentas):
                print(f"{i}. {cuenta.get_numero_cuenta()} - {cuenta.get_titular()}")
            
            try:
                idx1 = int(input("Seleccione primera cuenta: "))
                idx2 = int(input("Seleccione segunda cuenta: "))
                
                if cuentas[idx1] > cuentas[idx2]:
                    print(f"{cuentas[idx1].get_numero_cuenta()} tiene mayor saldo")
                else:
                    print(f"{cuentas[idx2].get_numero_cuenta()} tiene mayor saldo")
            except (ValueError, IndexError):
                print("Selección inválida")
        
        elif opcion == "6":
            print("\n--- ESTADO DE CUENTAS ---")
            if not cuentas:
                print("No hay cuentas creadas")
                continue
            
            for cuenta in cuentas:
                print(cuenta)
        
        elif opcion == "7":
            procesar_cuentas(cuentas)
        
        elif opcion == "8":
            print("¡Gracias por usar el sistema bancario!")
            break
        
        else:
            print("Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    main()