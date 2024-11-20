import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
from sqlalchemy import create_engine, text
import pymysql
import matplotlib.pyplot as plt
import pandas as pd

class EncuestaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Encuestas")
        self.root.geometry("1000x1000")  # Aumento de la ventana

        # Conectar a la base de datos
        self.engine = self.conectar_base_datos()
        if not self.engine:
            return

        # Configurar la interfaz
        self.configurar_interfaz()

    def conectar_base_datos(self):
        try:
            # Crear una conexión de SQLAlchemy usando PyMySQL
            engine = create_engine("mysql+pymysql://root:curso@localhost/ENCUESTAS")
            return engine
        except Exception as e:
            messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {e}")
            return None
    def configurar_interfaz(self):
        frame = ttk.Frame(self.root)
        frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Configurar Treeview
        self.tree = ttk.Treeview(frame, columns=("id", "edad", "sexo", "bebidas_semana", "cervezas_semana",
                                                 "bebidas_fin_semana", "destiladas_semana", "vinos_semana",
                                                 "perdidas_control", "diversion_dependencia", "problemas_digestivos",
                                                 "tension_alta", "dolor_cabeza"), show='headings')

        columnas = ["ID", "Edad", "Sexo", "Bebidas/Semana", "Cervezas/Semana", "Bebidas Fin de Semana",
                    "Destiladas/Semana", "Vinos/Semana", "Pérdidas Control", "Diversión Dependencia",
                    "Problemas Digestivos", "Tensión Alta", "Dolor de Cabeza"]

        for col, name in zip(self.tree["columns"], columnas):
            self.tree.heading(col, text=name)
            self.tree.column(col, width=120)

        # Hacer que la tabla ocupe casi todo el espacio disponible
        self.tree.grid(row=0, column=0, columnspan=3, pady=10, sticky="nsew")

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Botones de acción en la parte inferior
        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

        ttk.Button(button_frame, text="Agregar Registro", command=self.agregar_registro_gui, width=20).grid(row=0,
                                                                                                            column=0,
                                                                                                            padx=10,
                                                                                                            pady=10)
        ttk.Button(button_frame, text="Eliminar Registro", command=self.eliminar_registro_gui, width=20).grid(row=0,
                                                                                                              column=1,
                                                                                                              padx=10,
                                                                                                              pady=10)
        ttk.Button(button_frame, text="Actualizar Registro", command=self.actualizar_registro_gui, width=20).grid(row=1,
                                                                                                                  column=0,
                                                                                                                  padx=10,
                                                                                                                  pady=10)
        ttk.Button(button_frame, text="Filtrar Registros", command=self.filtrar_registros_gui, width=20).grid(row=1,
                                                                                                              column=1,
                                                                                                              padx=10,
                                                                                                              pady=10)
        ttk.Button(button_frame, text="Generar Gráfico ", command=self.ver_grafico, width=30).grid(row=2,
                                                                                                               column=0,
                                                                                                               columnspan=2,
                                                                                                               padx=10,
                                                                                                               pady=10)
        ttk.Button(button_frame, text="Exportar a Excel", command=self.exportar_a_excel, width=30).grid(row=3,
                                                                                                         column=0,
                                                                                                         columnspan=2,
                                                                                                         padx=10,
                                                                                                         pady=10)

        # Leer los registros inicialmente
        self.leer_registros()
    def leer_registros(self):
        # Limpiar los datos existentes en el Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        with self.engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM ENCUESTA ORDER BY idEncuesta")).fetchall()
            for row in result:
                self.tree.insert("", "end", values=row)

    def agregar_registro_gui(self):
        # Lista de campos que se van a agregar
        campos = [
            ('Edad', 'entero'),
            ('Sexo', 'texto'),
            ('BebidasSemana', 'entero'),
            ('CervezasSemana', 'entero'),
            ('BebidasFinSemana', 'entero'),
            ('BebidasDestiladasSemana', 'entero'),
            ('VinosSemana', 'entero'),
            ('PerdidasControl', 'texto'),
            ('DiversionDependenciaAlcohol', 'texto'),
            ('ProblemasDigestivos', 'texto'),
            ('TensionAlta', 'texto'),
            ('DolorCabeza', 'texto'),
        ]

        # Crear la ventana emergente para ingresar datos
        ventana_agregar = tk.Toplevel()
        ventana_agregar.title("Agregar Registro")

        # Diccionario para almacenar los valores de los campos
        valores = {}

        for i, (campo, tipo) in enumerate(campos):
            # Etiqueta para el campo
            label = tk.Label(ventana_agregar, text=f"{campo}:")
            label.grid(row=i, column=0, padx=10, pady=5)

            # Caja de entrada dependiendo del tipo
            if tipo == 'texto':
                entry = tk.Entry(ventana_agregar)
            elif tipo == 'entero':
                entry = tk.Entry(ventana_agregar)
            # Agregar más tipos si es necesario

            entry.grid(row=i, column=1, padx=10, pady=5)
            valores[campo] = (entry, tipo)  # Guardamos el widget y el tipo en el diccionario

        # Función para agregar el registro
        def agregar_registro():
            # Validar los datos y procesar la entrada
            registro = {}
            for campo, (entry, tipo) in valores.items():
                valor = entry.get()
                if valor == "":  # Si está vacío, mostrar un mensaje de error
                    messagebox.showerror("Error", f"El campo {campo} no puede estar vacío.")
                    return
                if tipo == 'entero' and not valor.isdigit():  # Validar si es un número entero
                    messagebox.showerror("Error", f"El campo {campo} debe ser un número entero.")
                    return
                registro[campo] = valor

            # Aquí debes agregar el registro a la base de datos o la estructura que estés utilizando.
            print("Registro agregado:", registro)

            # Cerrar la ventana emergente
            ventana_agregar.destroy()

        # Botón para agregar el registro
        boton_agregar = tk.Button(ventana_agregar, text="Agregar", command=agregar_registro)
        boton_agregar.grid(row=len(campos), column=0, columnspan=2, pady=10)

        ventana_agregar.mainloop()

    def eliminar_registro_gui(self):
        # Obtener el registro seleccionado
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Debe seleccionar un registro para eliminar.")
            return

        registro = self.tree.item(seleccion[0], "values")
        id_encuesta = registro[0]

        # Confirmación de eliminación
        if messagebox.askyesno("Confirmación", f"¿Está seguro de que desea eliminar el registro con ID {id_encuesta}?"):
            with self.engine.connect() as connection:
                query = "DELETE FROM ENCUESTA WHERE idEncuesta = :id"
                connection.execute(text(query), {"id": id_encuesta})

            messagebox.showinfo("Éxito", "Registro eliminado correctamente.")
            self.leer_registros()
    def actualizar_registro_gui(self):
        # Obtener el registro seleccionado
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Debe seleccionar un registro para actualizar.")
            return

        registro = self.tree.item(seleccion[0], "values")
        id_encuesta = registro[0]

        # Crear una nueva ventana para actualizar datos
        actualizar_window = Toplevel(self.root)
        actualizar_window.title("Actualizar Registro")
        actualizar_window.geometry("400x500")

        # Crear campos para editar los datos
        ttk.Label(actualizar_window, text="Edad:").grid(row=1, column=0, padx=10, pady=5)
        edad = tk.Entry(actualizar_window)
        edad.insert(0, registro[1])
        edad.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(actualizar_window, text="Sexo:").grid(row=2, column=0, padx=10, pady=5)
        sexo = tk.Entry(actualizar_window)
        sexo.insert(0, registro[2])
        sexo.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(actualizar_window, text="Bebidas Semana:").grid(row=3, column=0, padx=10, pady=5)
        bebidas_semana = tk.Entry(actualizar_window)
        bebidas_semana.insert(0, registro[3])
        bebidas_semana.grid(row=3, column=1, padx=10, pady=5)

        def actualizar():
            query = """
                UPDATE ENCUESTA
                SET edad = :edad, Sexo = :sexo, BebidasSemana = :bebidas_semana
                WHERE idEncuesta = :id
            """
            with self.engine.connect() as connection:
                connection.execute(text(query), {
                    "edad": edad.get(),
                    "sexo": sexo.get(),
                    "bebidas_semana": bebidas_semana.get(),
                    "id": id_encuesta
                })

            messagebox.showinfo("Éxito", "Registro actualizado correctamente.")
            actualizar_window.destroy()
            self.leer_registros()

        ttk.Button(actualizar_window, text="Actualizar", command=actualizar).grid(row=13, column=0, columnspan=2, pady=20)
    def filtrar_registros_gui(self):
        filtrar_window = Toplevel(self.root)
        filtrar_window.title("Filtrar Registros")
        filtrar_window.geometry("400x400")

        # Lista de columnas para filtrar
        columnas = [
            "Edad", "Sexo", "BebidasSemana", "CervezasSemana",
            "BebidasFinSemana", "BebidasDestiladasSemana", "VinosSemana",
            "PerdidasControl", "DiversionDependenciaAlcohol",
            "ProblemasDigestivos", "TensionAlta", "DolorCabeza"
        ]

        # Widgets para seleccionar columna y valor
        ttk.Label(filtrar_window, text="Seleccionar columna:").grid(row=0, column=0, padx=10, pady=5)
        columna_var = tk.StringVar(value=columnas[0])
        columna_menu = ttk.Combobox(filtrar_window, textvariable=columna_var, values=columnas)
        columna_menu.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(filtrar_window, text="Valor a buscar:").grid(row=1, column=0, padx=10, pady=5)
        valor_entry = tk.Entry(filtrar_window)
        valor_entry.grid(row=1, column=1, padx=10, pady=5)

        # Función para filtrar registros
        def filtrar():
            columna = columna_var.get()
            valor = valor_entry.get()

            query = f"SELECT * FROM ENCUESTA WHERE {columna} = :valor"
            try:
                with self.engine.connect() as connection:
                    df = pd.read_sql_query(query, connection, params={"valor": valor})
                self.mostrar_datos(df)
                filtrar_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo realizar el filtro: {e}")

        # Botón para filtrar
        ttk.Button(filtrar_window, text="Filtrar", command=filtrar).grid(row=2, column=0, columnspan=2, pady=20)

    def mostrar_datos(self, df):
        # Función para mostrar los resultados filtrados en el Treeview
        self.tree.delete(*self.tree.get_children())
        for _, row in df.iterrows():
            self.tree.insert("", tk.END, values=tuple(row))

    def ver_grafico(self):
        grafico_window = Toplevel(self.root)
        grafico_window.title("Seleccionar Gráfico")
        grafico_window.geometry("400x300")

        # Opciones de columnas para gráficos
        columnas = [
            "Edad", "BebidasSemana", "CervezasSemana", "BebidasFinSemana",
            "BebidasDestiladasSemana", "VinosSemana", "PerdidasControl",
            "DiversionDependenciaAlcohol", "ProblemasDigestivos",
            "TensionAlta", "DolorCabeza"
        ]

        # Widgets para selección de columna y tipo de gráfico
        ttk.Label(grafico_window, text="Seleccionar columna:").grid(row=0, column=0, padx=10, pady=5)
        columna_var = tk.StringVar(value=columnas[0])
        columna_menu = ttk.Combobox(grafico_window, textvariable=columna_var, values=columnas)
        columna_menu.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(grafico_window, text="Seleccionar tipo de gráfico:").grid(row=1, column=0, padx=10, pady=5)
        tipo_grafico_var = tk.StringVar(value="Barras")
        tipos_graficos = ["Barras", "Líneas", "Tarta"]
        tipo_menu = ttk.Combobox(grafico_window, textvariable=tipo_grafico_var, values=tipos_graficos)
        tipo_menu.grid(row=1, column=1, padx=10, pady=5)

        def generar_grafico():
            columna = columna_var.get()
            tipo = tipo_grafico_var.get()

            # Consulta a la base de datos
            query = f"SELECT {columna}, COUNT(*) AS frecuencia FROM ENCUESTA GROUP BY {columna}"
            with self.engine.connect() as connection:
                df = pd.read_sql_query(query, connection)

            # Crear gráfico basado en el tipo seleccionado
            if tipo == "Barras":
                plt.bar(df[columna], df["frecuencia"], color="blue")
                plt.title(f"Frecuencia de {columna}")
                plt.xlabel(columna)
                plt.ylabel("Frecuencia")
            elif tipo == "Líneas":
                plt.plot(df[columna], df["frecuencia"], marker="o", color="green")
                plt.title(f"Frecuencia de {columna}")
                plt.xlabel(columna)
                plt.ylabel("Frecuencia")
            elif tipo == "Tarta":
                plt.pie(df["frecuencia"], labels=df[columna], autopct="%1.1f%%", startangle=140)
                plt.title(f"Distribución de {columna}")

            plt.show()

        ttk.Button(grafico_window, text="Generar Gráfico", command=generar_grafico).grid(row=2, column=0, columnspan=2, pady=20)

    def exportar_a_excel(self):
        query = "SELECT * FROM ENCUESTA"
        with self.engine.connect() as connection:
            df = pd.read_sql_query(query, connection)

        archivo = "encuestas_exportadas.xlsx"
        df.to_excel(archivo, index=False)
        messagebox.showinfo("Éxito", f"Los datos se han exportado correctamente a {archivo}")
if __name__ == "__main__":
    root = tk.Tk()
    app = EncuestaApp(root)
    root.mainloop()