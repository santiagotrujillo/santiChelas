import sqlite3

def insertar_user(id, name, email):
    conn = sqlite3.connect('santiChelasdb.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO users (id, name, email)
    VALUES  (?, ?, ?)
    ''', (id, name, email)
    )
    conn.commit()
    conn.close()

def insertar_beer(name, price):
    conn = sqlite3.connect('santiChelasdb.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO beers (name, price)
    VALUES  (?, ?)
    ''', (name, price)
    )
    conn.commit()
    conn.close()

def insertar_buys(user_id, beer_id, units, payment_method):

    # Verificar los tipos de los parámetros
    print(f"user_id: {user_id} (tipo: {type(user_id)})")
    print(f"beer_id: {beer_id} (tipo: {type(beer_id)})")
    print(f"units: {units} (tipo: {type(units)})")
    print(f"payment_method: {payment_method} (tipo: {type(payment_method)})")
    
    # Asegurarse de que los valores sean del tipo correcto
    if not isinstance(user_id, int) or not isinstance(beer_id, int) or not isinstance(units, int) or not isinstance(payment_method, str):
        print("Error: uno o más parámetros tienen tipos no compatibles.")
        return
    conn = sqlite3.connect('santiChelasdb.db')
    cursor = conn.cursor()


    # Obtener el precio de la cerveza seleccionada
    try:
        cursor.execute('''SELECT price FROM beers WHERE id = ?''', (beer_id,))
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        conn.close()
        return

    beer_price = cursor.fetchone()

    if beer_price is None:
        print("Error: No se encontro la cerveza con el ID proporcionado.")
        conn.close()
        return

    price_unit = beer_price[0]
    price_total = price_unit * units

    #Insertar una nueva venta
    cursor.execute('''
    INSERT INTO buys (user_id, beer_id, units, price_unit, price_total, payment_method)
    VALUES  (?, ?, ?, ?, ?, ?)
    ''', (user_id, beer_id, units, price_unit, price_total, payment_method)
    )
    conn.commit()
    conn.close()
    print("Compra insertada exitosamente. ")


def mostrar_users():
    conn = sqlite3.connect("santiChelasdb.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()

    if users:
        print("\n--- Lista de Usuarios ---")
        print("{:<5} {:<20} {:<30} {:<15}".format("ID", "Nombre", "Email", "Teléfono"))
        print("-" * 75)

        for user in users:
            user_id, name, email, phone = user

            # Reemplaza valores None por una cadena vacía o un valor predeterminado
            phone = phone if phone is not None else "Sin teléfono"
            print("{:<5} {:<20} {:<30} {:<15}".format(user_id, name, email, phone))
    else:
        print("No se encontraron usuarios en la base de datos.")

def mostrar_beers():
    conn = sqlite3.connect("santiChelasdb.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM beers')
    beers = cursor.fetchall()
    conn.close()

    if beers:
        print("\n--- Lista de Cervezas Disponibles ---")
        print("{:<5} {:<20} {:<10} {:<30}".format("ID", "Nombre", "Precio", "Descripción"))
        print("-" * 65)
        
        for beer in beers:            
            beer_id, name, price, description = beer
            description = description if description is not None else "Sin descripción"
            print("{:<5} {:<20} {:<10} {:<30}".format(beer_id, name, price, description))
    else:
        print("No se encontraron cervezas en la base de datos.")

def mostrar_buys():
    conn = sqlite3.connect("santiChelasdb.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM buys')
    buys = cursor.fetchall()
    conn.close()

    if buys:
        print("\n--- Lista de Cervezas Disponibles ---")
        print("{:<5} {:<12} {:<13} {:<17} {:<14} {:<15} {:<20}".format("ID", "ID Usuario", "ID cerveza", "Precio Unitario", "Precio Total", "Metodo de Pago", "Unidades"))
        print("-" * 100)

        for buy in buys:            
            id, user_id, beer_id, price_unit, price_total, payment_method, units = buy
            print("{:<5} {:<12} {:<13} {:<17} {:<14} {:<15} {:<20}".format(id, user_id, beer_id, price_unit, price_total, payment_method, units))
        
    else:
        print("No se encontraron compras en la base de datos.")

def actualizar_price_beers():
    conn = sqlite3.connect("santiChelasdb.db")
    cursor = conn.cursor()
    beer_id = input("Introduce el ID de la cerveza a actualizar: ")
    new_price = input("Cual es el nuevo precio de la cerveza?: ")

    try:
        # Verificar si los valores son válidos
        if not beer_id or not new_price:
            print("Error: Debes ingresar tanto el ID como el nuevo precio.")
            return

        # Convertir el precio a float
        new_price = int(new_price)

        # Actualizar el precio de la cerveza en la base de datos
        cursor.execute("""
            UPDATE beers
            SET price = ?
            WHERE id = ?
        """, (new_price, beer_id))  # <- Los valores se pasan correctamente como una tupla

        # Guardar los cambios
        conn.commit()
        if cursor.rowcount > 0:
            print(f"El precio de la cerveza con ID {beer_id} ha sido actualizado correctamente.")
        else:
            print(f"No se encontro la cerveza con ID {beer_id}.")
    except Exception as e:
        print(f"Error al actualizar el precio: {e}")

    conn.close()



def mostrar_menu():
    print("\n --- Menu Principal---")
    print("1. Insertar compra")
    print("2. Mostrar cervezas")
    print("3. Mostrar compras")
    print("4. Actualizar precio de la cerveza")
    print("5. Salir")

def solicitar_datos_compra():
    user_id = int(input("Introduce el ID del usuario: "))
    beer_id = int(input("Introduce el ID de la cerveza: "))
    units = int(input("Introduce la cantidad de Cerveza: "))
    payment_method = input("Introduce el metodo de pago: ")
    return user_id, beer_id, units, payment_method

def ejecutar_menu():
    while True:
        mostrar_menu()
        opc = input("Selecciona una opcion: ")

        if opc == "1":
            user_id, beer_id, units, payment_method = solicitar_datos_compra()
            insertar_buys(user_id, beer_id, units, payment_method)

        elif opc == "2":
            mostrar_beers()

        elif opc == "3":
            mostrar_buys()

        elif opc == "4":
            actualizar_price_beers()

        elif opc == "5":
            print("Saliendo del programa...")
            break

        else:
            print("Opcion no valida, por favor elige una opcion del menu")

#mostrar_users()
if __name__ == "__main__":
    ejecutar_menu()
