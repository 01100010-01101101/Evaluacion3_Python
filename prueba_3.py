import csv
import datetime

class Habitacion:
    def __init__(self, piso, numero, costo_diario):
        self.piso = piso
        self.numero = numero
        self.estado = "Disponible"
        self.costo_diario = costo_diario
        self.reserva = None  # None si no está reservada, o datos de la reserva

    def reservar(self, nombre, apellido, rut, fecha_ingreso, fecha_salida):
        self.estado = "Reservada"
        self.reserva = {
            'nombre': nombre,
            'apellido': apellido,
            'rut': rut,
            'fecha_ingreso': fecha_ingreso,
            'fecha_salida': fecha_salida
        }

    def anular_reserva(self):
        self.estado = "Disponible"
        self.reserva = None

    def __str__(self):
        return f"Habitación {self.piso}{self.numero} - Estado: {self.estado}, Costo diario: ${self.costo_diario}"

class Hotel:
    def __init__(self):
        self.habitaciones = {}
        self.total_ventas_diarias = 0

        # habitaciones del hotel
        for piso in range(1, 6):
            for numero in range(1, 9):
                if piso == 5:
                    costo_diario = 100000
                elif piso == 4:
                    costo_diario = 60000
                else:
                    costo_diario = 30000
                codigo = f"{piso}{numero}"
                self.habitaciones[codigo] = Habitacion(piso, numero, costo_diario)

    def reservar_habitacion(self, codigo, nombre, apellido, rut, fecha_ingreso, fecha_salida):
        habitacion = self.habitaciones.get(codigo)
        if habitacion:
            if habitacion.estado == "Disponible":
                try:
                    fecha_ingreso = datetime.datetime.strptime(fecha_ingreso, "%Y-%m-%d %H:%M")
                    fecha_salida = datetime.datetime.strptime(fecha_salida, "%Y-%m-%d %H:%M")
                except ValueError:
                    print("Error: Formato de fecha incorrecto.")
                    return

                costo_total = (fecha_salida - fecha_ingreso).days * habitacion.costo_diario
                print(f"El costo total de la reserva es: ${costo_total}")

                confirmacion = input("¿Desea confirmar la reserva? (s/n): ")
                if confirmacion.lower() == 's':
                    habitacion.reservar(nombre, apellido, rut, fecha_ingreso, fecha_salida)
                    print("¡Reserva realizada con éxito!")
                    return True
                else:
                    print("Reserva cancelada.")
            else:
                print("La habitación no está disponible para reserva.")
        else:
            print("Habitación no encontrada.")

    def buscar_habitacion(self, codigo):
        habitacion = self.habitaciones.get(codigo)
        if habitacion:
            print(f"Información de la habitación {codigo}:")
            print(habitacion)
            if habitacion.reserva:
                print("Reserva actual:")
                print(habitacion.reserva)
        else:
            print("Habitación no encontrada.")

    def ver_estado(self):
        print("Estado actual de todas las habitaciones del hotel:")
        for codigo, habitacion in self.habitaciones.items():
            print(f"{codigo}: {habitacion}")

    def ventas_diarias(self):
        total_ventas = 0
        hoy = datetime.date.today()
        for habitacion in self.habitaciones.values():
            if habitacion.reserva:
                fecha_salida = datetime.datetime.strptime(habitacion.reserva['fecha_salida'], "%Y-%m-%d %H:%M").date()
                if fecha_salida == hoy:
                    total_ventas += (fecha_salida - datetime.datetime.strptime(habitacion.reserva['fecha_ingreso'], "%Y-%m-%d %H:%M").date()).days * habitacion.costo_diario
        print(f"Total de ventas del día: ${total_ventas}")
        self.total_ventas_diarias = total_ventas

    def guardar_informacion(self):
        with open('estado_habitaciones.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Piso', 'Número', 'Estado', 'Costo diario', 'Nombre', 'Apellido', 'Rut', 'Fecha ingreso', 'Fecha salida'])
            for habitacion in self.habitaciones.values():
                if habitacion.reserva:
                    reserva = habitacion.reserva
                    writer.writerow([habitacion.piso, habitacion.numero, habitacion.estado, habitacion.costo_diario,
                                     reserva['nombre'], reserva['apellido'], reserva['rut'], reserva['fecha_ingreso'], reserva['fecha_salida']])
                else:
                    writer.writerow([habitacion.piso, habitacion.numero, habitacion.estado, habitacion.costo_diario, "", "", "", "", ""])

def menu():
    print("\nBienvenido al sistema de gestión de habitaciones del hotel.")
    print("Seleccione una opción:")
    print("1. Reservar habitación")
    print("2. Buscar habitación")
    print("3. Ver estado de las habitaciones")
    print("4. Ver ventas diarias")
    print("5. Guardar información de las habitaciones")
    print("6. Salir")

hotel = Hotel()

while True:
    menu()
    opcion = input("Ingrese el número de la opción deseada: ")

    if opcion == '1':
        codigo = input("Ingrese el código de la habitación a reservar (ej. 13, 34, 58): ")
        nombre = input("Ingrese nombre del responsable: ")
        apellido = input("Ingrese apellido del responsable: ")
        rut = input("Ingrese rut del responsable: ")
        fecha_ingreso = input("Ingrese fecha de ingreso (YYYY-MM-DD HH:MM): ")
        fecha_salida = input("Ingrese fecha de salida (YYYY-MM-DD HH:MM): ")
        hotel.reservar_habitacion(codigo, nombre, apellido, rut, fecha_ingreso, fecha_salida)

    elif opcion == '2':
        codigo = input("Ingrese el código de la habitación a buscar (ej. 13, 34, 58): ")
        hotel.buscar_habitacion(codigo)

    elif opcion == '3':
        hotel.ver_estado()

    elif opcion == '4':
        hotel.ventas_diarias()

    elif opcion == '5':
        hotel.guardar_informacion()
        print("Información guardada correctamente en estado_habitaciones.csv")

    elif opcion == '6':
        print("¡Gracias por utilizar nuestro sistema de gestión de habitaciones!")
        break

    else:
        print("Opción no válida. Por favor, ingrese un número del 1 al 6 según el menú.")