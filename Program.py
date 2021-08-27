from pathlib import Path
import prod_col
import seller_col
import sale_col


def load_file(fileName):
    file = open(Path.cwd() / fileName)
    items = file.readlines()[1:]
    file.close()

    matriz_items = []

    for item in items:
        item = item.strip()
        matriz_items.append(item.split(","))
    return matriz_items


def obten_atributo(objeto, columna):
    return objeto[columna]


def obten_todo(objetos, columna):
    result = []
    for objeto in objetos:
        if columna == prod_col.NOMBRE or columna == seller_col.NOMBRE:
            result.append(objeto[columna].upper())
        else:
            result.append(objeto[columna])
    return result


def obten_objetos(objetos, columna, valor):
    result = []
    if columna == prod_col.NOMBRE or columna == seller_col.NOMBRE:
        valor = valor.upper()
    valores = obten_todo(objetos, columna)
    if valor in valores:
        for indx, val in enumerate(valores):
            if val == valor:
                result.append(objetos[indx])
        return result
    else:
        return False


def print_matriz(matriz):
    bigger_size = []
    biggest = 0
    for columna in range(len(matriz[0])):
        for fila in range(len(matriz)):
            if len(matriz[fila][columna]) > biggest:
                biggest = len(matriz[fila][columna])
        bigger_size.append(biggest)
        biggest = 0
        
    for fila in matriz:
        for columna, value in enumerate(fila):
            print(value.ljust(bigger_size[columna] + 3), end = "")
        print()


def registrar_venta(inventario, vendedores, ventas): 
    #Recolección y verificación de los datos de los datos de entrada requeridos
    item = input('Introduzca el nombre del artículo:\n')
    if obten_objetos(inventario, prod_col.NOMBRE, item) == False:
        print('El artículo no se encuentra en los archivos')
    else:
        vendedor = input('Introduzca el nombre del vendedor:\n')
        if obten_objetos(vendedores, seller_col.NOMBRE, vendedor) == False:
            print('El vendedor no se encuentra en los archivos')
        else:
            confirm = True
            cant = input('Introduzca la cantidad de items a vender:\n')
            try:
                cant = int(cant)
            except ValueError:
                print('La cantidad no es número entero')
                confirm = False
            if confirm == False or cant < 1:
                print('La cantidad introducida no es válida')
            elif cant < 1:
                print('La cantidad introducida no es válida')
                #Consulta disponibilidad en el inventario y descuenta la venta
            else:
                articulo = obten_objetos(inventario, prod_col.NOMBRE, item)[0]
                if int(articulo[prod_col.EXISTENCIA]) < cant:
                    print(f'No se puede realizar la venta')
                    print('Quedan solo ' + str(articulo[prod_col.EXISTENCIA])+
                        ' ' + str(articulo[prod_col.NOMBRE]) + 
                        ' en el inventario') 
                else:
                    prod_id = int(obten_atributo(articulo, prod_col.ID))
                    inventario[prod_id][prod_col.EXISTENCIA] = str(
                        int(inventario[prod_id][prod_col.EXISTENCIA]) - cant)
                    #Agrega las ventas del vendedor y totales
                    vend = obten_objetos(
                        vendedores, seller_col.NOMBRE, vendedor)[0]
                    vend_id = int(obten_atributo(vend, seller_col.ID))
                    ventas[prod_id][vend_id + 2] = str(
                        int(ventas[prod_id][vend_id + 2]) + cant)
                    ventas[prod_id][sale_col.TOTAL] = str(
                        int(ventas[prod_id][sale_col.TOTAL]) + cant)
                    print('Venta registrada exitosamente\n')


def llegada_articulos(inventario, vendedores, ventas):
    #Recolección y verificación de datos de entrada requeridos
    item = input('Introduzca el nombre del artículo:\n')
    if obten_objetos(inventario, prod_col.NOMBRE, item) == False:
        print('El artículo no se encuentra en los archivos')
    else:
        confirm = True
        cantidad = input('Introduzca la cantidad de ítems que llegaron:\n')
        try:
            cantidad = int(cantidad)
        except ValueError:
            print('La cantidad no es número entero')
            confirm = False
        if confirm == False or cantidad < 1:
                print(f'La cantidad introducida no es válida')
            #Agrega la cantidad a la existencia del producto
        else:
            articulo = obten_objetos(inventario, prod_col.NOMBRE, item)[0]
            prod_id = int(obten_atributo(articulo, prod_col.ID))
            inventario[prod_id][prod_col.EXISTENCIA] = str(
                int(inventario[prod_id][prod_col.EXISTENCIA]) + cantidad)
            print('Producto registrado exitosamente')


def consulta_inventario(inventario, vendedores, ventas):
    #Recolección de dato de entrada requerido
    item = input('Introduzca el nombre del producto:\n')
    #Verificación de dato de entrada
    if obten_objetos(inventario, prod_col.NOMBRE, item) == False:
        print('El artículo no se encuentra en los archivos')
    #Preparación de matriz a imprimir
    else:
        consulta = []
        articulo = obten_objetos(inventario, prod_col.NOMBRE, item)[0]
        consulta.append(prod_col.LIST_NAMES)
        consulta.append(articulo)
        print_matriz(consulta)
    

def consultar_datos_ventas(invetario, vendedores, ventas):
    #Recolección de datos de entrada requeridos y verificación
    vendedor = input('Introduzca el nombre del vendedor:\n')
    if obten_objetos(vendedores, seller_col.NOMBRE, vendedor) == False:
        print('El vendedor no se encuentra registrado en la base de datos.')
        
    else:
        art = input('Introduzca el nombre del producto:\n')
        if obten_objetos(inventario, prod_col.NOMBRE, art) == False:
            print('El artículo no se encuentra en las bases de datos.')
        #Procesamiento de la información y generación de los datos a imprimir
        else:
            vend = obten_objetos(vendedores, seller_col.NOMBRE, vendedor)[0]
            ID_vendedor = obten_atributo(vend, seller_col.ID)
            articulo = obten_objetos(inventario, prod_col.NOMBRE, art)[0]
            ID_articulo = obten_atributo(articulo, prod_col.ID)
            cantidad = obten_atributo(ventas, int(ID_articulo))[
                int(ID_vendedor) + 2]
            print(str(vend[1]) + ' ha vendido ' + str(cantidad) +
                ' unidades del producto: ' + str(articulo[1]) + '.')


def reporte_ventas_vendedor(inventario, vendedores, ventas):
    #Recolección de datos de entrada requeridos
    vendedor = input('Introduzca el nombre del vendedor:\n')
    #Verificación de datos de entrada
    if obten_objetos(vendedores, seller_col.NOMBRE, vendedor) == False:
        print('El vendedor no se encuentra registrado en la base de datos.')
    #Generación del reporte a regresar
    else:
        vend = obten_objetos(vendedores, prod_col.NOMBRE, vendedor)[0]
        vend_id = int(obten_atributo(vend, prod_col.ID))
        ventas_producto = obten_todo(ventas, (vend_id)+2)
        nombre_producto = obten_todo(ventas, sale_col.PROD_NOMBRE)
        precios = obten_todo(inventario, prod_col.PRECIO)
        impresion = [[sale_col.LIST_NAMES[1], 
            sale_col.LIST_NAMES[vend_id + 2], sale_col.LIST_NAMES[-1]]]
        for i in range(len(ventas_producto)):
            lista = []
            if int(ventas_producto[i]) == 0:
                continue
            else:    
                lista.append(nombre_producto[i])
                lista.append(ventas_producto[i])
                lista.append(
                    f'${int(precios[i]) * int(ventas_producto[i])}.00')
                impresion.append(lista)
        print_matriz(impresion)
                    

def reporte_ventas_articulo(inventario, vendedores, ventas):
    #Recolección de datos de entrada requeridos
    art = input('Introduzca el nombre del artículo:\n')
    #Verificación de datos de entrada
    if obten_objetos(inventario, prod_col.NOMBRE, art) == False:
        print('El artículo no se encuentra en los archivos')
    #Generación de los datos a imprimir
    else:
        empleados = obten_todo(vendedores, seller_col.NOMBRE)
        articulo = obten_objetos(inventario, prod_col.NOMBRE, art)[0]
        art_ventas = obten_objetos(ventas, sale_col.PROD_NOMBRE, art)[0]
        precio = int(obten_atributo(articulo, prod_col.PRECIO))
        #Generación de la impresión
        impresion = [[seller_col.LIST_NAMES[1], "Cantidad"]]
        venta_total = 0
        for i in range(len(empleados)):
            lista = []
            lista.append(empleados[i])
            lista.append(art_ventas[i + 2])
            impresion.append(lista)
            venta_total += int(art_ventas[i + 2])
        impresion.append(["TOTAL", f'${venta_total * precio}.00'])
        print_matriz(impresion)

def contrata_vendedor(inventario, vendedores, ventas):
    #Recolección y verificación de datos
    nombre = input('Introduzca el nombre del nuevo trabajador:\n')
    nombre = nombre.title()
    fecha = ''
    confirm = True 
    dia = input('Introduzca el día en número (DD):\n')
    try:
        dia = int(dia)
    except ValueError:
        print('Introduzca un número entero')
        confirm = False
    if  confirm == False or (len(str(dia)) != 2 and len(
        str(dia)) != 1) or dia <= 0 or dia > 31:
        print('Día no válido')
    else:
        mes = input('Introduzca el mes en número (MM):\n')
        try:
            mes = int(mes)
        except ValueError:
            print('Introduzca un número entero')
            confirm = False
        if confirm == False or (len(str(mes)) != 2 and len(
            str(mes)) != 1) or mes <= 0 or mes > 12:
            print('Mes no válido')
        else:
            año = input('Introduzca el año en número (AAAA): \n')
            try:
                año = int(año)
            except ValueError:
                print('Introduzca un número entero')
                confirm = False
            if confirm == False or len(str(
                año)) != 4 or año < 2018 or año > 2020:
                print('Año no válido')
            else:
                #Agrega el vendedor a la matriz de vendedores
                fecha = f'{dia}/{mes}/{año}'
                vendedores.append([len(vendedores), nombre, fecha])
                sale_col.LIST_NAMES.insert(-1, f'V{len(vendedores)-1}')
                sale_col.NAMES = str(sale_col.NAMES[:-5] + ',' +
                    sale_col.LIST_NAMES[-2] + ',Total')
                #Agrega una columna a matriz de ventas
                for i in ventas:
                    i.insert(-1, 0)
                print('Vendedor registrado')


def guardar(inventario, vendedores, ventas):
    files = ['stock.csv', 'employees.csv', 'sales.csv']
    for i in range(len(files)):
        if i == 0:
            arch_s = prod_col.NAMES + '\n'
            matriz = inventario
        elif i == 1:
            arch_s = seller_col.NAMES + '\n'
            matriz = vendedores
        else:
            arch_s = sale_col.NAMES + '\n'
            matriz = ventas
        
        for fila in matriz:
            for columna in fila:
                arch_s = arch_s + str(columna) + ','
            arch_s = arch_s[:-1] + '\n'
        
        arch_s = arch_s[:-1]

        archivo = open(Path.cwd() / files[i], 'w') 
        archivo.write(arch_s)
        archivo.close()


def main():
    option = '-'
    while option != '8':
        print('\n\nBienvenido al software de administrador de Silicon MX')
        print(' Seleccione una opción')
        print('  1- Registrar venta')
        print('  2- Registrar llegada de artículos')
        print('  3- Consultar datos del inventario')
        print('  4- Consultar datos de ventas')
        print('  5- Mostrar reporte de ventas por vendedor')
        print('  6- Mostrar reporte de ventas por artículo')
        print('  7- Contratar nuevo vendedor')
        print('  8- Guardar y cerrar')
        option = input()
        
        if option == '1':
            registrar_venta(inventario, vendedores, ventas)
       
        elif option == '2':
            llegada_articulos(inventario, vendedores, ventas)
            
        elif option == '3':
            consulta_inventario(inventario, vendedores, ventas)
            
        elif option == '4':
            consultar_datos_ventas(inventario, vendedores, ventas)
            
        elif option == '5':
            reporte_ventas_vendedor(inventario, vendedores, ventas)
            
        elif option == '6':
            reporte_ventas_articulo(inventario, vendedores, ventas)

        elif option == '7':
            contrata_vendedor(inventario, vendedores, ventas)
        
        elif option != '8':
            print('Selección inválida')
        
    guardar(inventario, vendedores, ventas)
    print('Datos guardados\n¡Que tenga un buen día!')        

#Cargar archivos a matrices
inventario = load_file('stock.csv')
vendedores = load_file('employees.csv')
ventas = load_file('sales.csv')
    
main()