import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pytube import YouTube
from configparser import ConfigParser
from moviepy.editor import AudioFileClip
import pyflp
import threading
import shlex
import demucs.separate  # Asegúrate de tener esta biblioteca instalada y configurada correctamente

# Obtener la ruta del directorio donde se encuentra el script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Ruta completa del archivo de configuración
config_file = os.path.join(script_dir, 'settings.ini')

# Cargar o crear configuración
config = ConfigParser()
default_download_path = os.path.expanduser('~')

if not os.path.exists(config_file):
    config['PATHS'] = {'download_path': default_download_path}
    with open(config_file, 'w') as f:
        config.write(f)
else:
    config.read(config_file)

# Función para guardar la configuración
def save_config():
    with open(config_file, 'w') as f:
        config.write(f)

# Función para abrir el directorio en el explorador de archivos
def open_folder(path):
    os.startfile(path)
    
# Función para actualizar el label con la ruta del proyecto
def update_output_path_label(*args):
    project_location = location_entry.get()
    project_name = name_entry.get()
    output_path = os.path.join(project_location, project_name)
    output_path_label.config(text=f"Ruta de salida: {output_path}")


# Añadir esta función que proporcionaste para separar los stems
def separate_audio(file_path, output_dir, project_name):
    final_output_dir = os.path.join(output_dir, project_name, 'assets')
    os.makedirs(final_output_dir, exist_ok=True)
    # Aquí simplemente se define el modelo y la salida se establece directamente
    command = f'--mp3 -n mdx_extra --out "{final_output_dir}" "{file_path}"'
    args = shlex.split(command)
    # Inicia el proceso de separación en un hilo para evitar bloquear la GUI
    def run_separation():
        print("Proceso en curso", "Extracción de stems en progreso...")
        demucs.separate.main(args)
        messagebox.showinfo(f"La separación ha terminado. Los stems se han guardado en: {final_output_dir}")
        print(f"La separación ha terminado. Los stems se han guardado en: {final_output_dir}")
    threading.Thread(target=run_separation).start()

# Función para descargar solo audio y convertirlo a MP3
# Modificar la función de descarga para incluir la separación de stems
def download_video():
    url = url_entry.get()
    project_location = location_entry.get()
    project_name = name_entry.get()
    separate_stems = separate_stems_var.get()
    
    if not url or not project_location or not project_name:
        messagebox.showerror("Error", "Todos los campos son necesarios")
        return
    
    try:
        yt = YouTube(url)
        title = yt.title
        safe_title = ''.join(char for char in title if char.isalnum() or char in " -_")
        
        project_path = os.path.join(project_location, project_name)
        assets_path = os.path.join(project_path, 'assets')
        os.makedirs(assets_path, exist_ok=True)

        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_file_path = audio_stream.download(output_path=assets_path, filename=f"{safe_title}.mp4")

        mp3_path = os.path.join(assets_path, f'{safe_title}.mp3')
        audio_clip = AudioFileClip(audio_file_path)

        audio_clip.write_audiofile(mp3_path)
        audio_clip.close()
        os.remove(audio_file_path)
        
        if separate_stems:
            separate_audio(mp3_path, project_location, project_name)
        
        create_flp(project_path, project_name)
        open_folder(project_path)

        messagebox.showinfo("Proyecto creado", "Se ha creado el proyecto. Se acaba de iniciar el proceso de extraer los stems. Para ver el progreso mira la terminal. Si quieres puedes crear otro proyecto miestras tanto (te va a ralentizar el otro).")
        print("Se ha creado el proyecto. Se acaba de iniciar el proceso de extraer los stems. Para ver el progreso mira la terminal. Si quieres puedes crear otro proyecto miestras tanto (te va a ralentizar el otro).")

    except Exception as e:
        messagebox.showerror("Error", f"Error al descargar el audio: {str(e)}")
        print(f"Excepción al escribir el archivo de audio: {e}")  # Esto imprimirá en la consola si es posible.


# Crear el proyecto de FL Studio
def create_flp(project_path, project_name):
    try:
        fl_template_path = os.path.join(config['PATHS']['fl_template_path'], template_combobox.get())
        project = pyflp.parse(fl_template_path)
        pyflp.save(project, os.path.join(project_path, f'{project_name}.flp'))
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo crear el archivo FLP: {str(e)}")


def update_template_list():
    template_path = config['PATHS']['fl_template_path']
    try:
        # Listar todos los archivos .flp en el directorio de plantillas
        flp_files = [file for file in os.listdir(template_path) if file.endswith('.flp')]
        template_combobox['values'] = flp_files
        if flp_files:
            template_combobox.current(0)  # Establece el primer archivo como seleccionado por defecto
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar la lista de plantillas: {str(e)}")


# Función para seleccionar carpeta
def select_folder():
    path = filedialog.askdirectory(initialdir=config['PATHS']['download_path'])
    if path:
        location_entry.delete(0, tk.END)
        location_entry.insert(0, path)
        config['PATHS']['download_path'] = path
        save_config()

# Función para cambiar la ruta del proyecto solo para esta vez.
def select_folder_temporal():
    path = filedialog.askdirectory(initialdir=config['PATHS']['download_path'])
    location_entry.delete(0, tk.END)
    location_entry.insert(0, path)

# Función para seleccionar carpeta
def select_template():
    path = filedialog.askdirectory(initialdir=config['PATHS']['fl_template_path'])
    if path:
        config['PATHS']['fl_template_path'] = path
        save_config()
        update_template_list()

# Antes de iniciar la interfaz gráfica, imprimir el mensaje de bienvenida
def print_welcome_message():
    print("""
    +------------------------------------+
    |              FL INIT               |
    +------------------------------------+
    | Bienvenido al inicializador de FL  |
    | Studio! Esta aplicación permite la |
    | descarga de audio de YouTube y la  |
    | separación de stems automatizada.  |
    |                                    |
    | La consola mostrará las barras de  |
    | carga y el progreso de los         |
    | procesos. Por favor, manténgala    |
    | abierta durante la operación.      |
    +------------------------------------+
    """)

# Llamar a la función antes del bucle principal de Tkinter
print_welcome_message()

# GUI setup
root = tk.Tk()
root.title("FL INIT")

def show_info(event):
    messagebox.showinfo("Información de Separación de Stems", "El tiempo requerido para la separación de stems puede variar significativamente en función de las especificaciones del hardware utilizado, especialmente la GPU. Un hardware más avanzado facilitará una mayor velocidad de procesamiento. Mi portatil con una gráfica integrada tarda 5 mins. Podrás ver el progreso de la separación en la terminal que se abre al ejectuar la aplicación. ")

# Calcular posición para centrar la ventana
window_width = 700
window_height = 280
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width/2)
center_y = int(screen_height/2 - window_height/2)
root.resizable(False, False)

# Tamaño y posición de la ventana
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# Marco para los inputs
input_frame = tk.Frame(root, pady=10)
input_frame.pack()

# URL Entry
tk.Label(input_frame, text="URL de YouTube:").grid(row=0, column=0, sticky='w', padx=10, pady=5)
url_entry = tk.Entry(input_frame, width=70)
url_entry.grid(row=0, column=1, padx=10, pady=5)

# Location Entry
tk.Label(input_frame, text="Ubicación del Proyecto:").grid(row=1, column=0, sticky='w', padx=10, pady=5)
location_entry = tk.Entry(input_frame, width=70)
location_entry.insert(0, config['PATHS']['download_path'])
location_entry.grid(row=1, column=1, padx=10, pady=5)

# Name Entry
tk.Label(input_frame, text="Nombre del Proyecto:").grid(row=2, column=0, sticky='w', padx=10, pady=5)
name_entry = tk.Entry(input_frame, width=70)
name_entry.grid(row=2, column=1, padx=10, pady=5)

# Botón para seleccionar la ubicación del proyecto
browse_button = tk.Button(input_frame, text="Examinar", command=select_folder_temporal)
browse_button.grid(row=1, column=2, padx=10, pady=5)

# Template Selection Combobox
tk.Label(input_frame, text="Plantilla FLP:").grid(row=3, column=0, sticky='w', padx=10, pady=5)
template_combobox = ttk.Combobox(input_frame, width=67)
template_combobox.grid(row=3, column=1, padx=10, pady=5)

update_template_list()  # Llamar a la función para cargar las plantillas iniciales
# Output Path Label
output_path_label = tk.Label(input_frame, text="Ruta de salida: ", anchor='w', relief='sunken', width=81)
output_path_label.grid(row=4, column=0, columnspan=2, pady=10)


# Download Button
download_button = tk.Button(input_frame, text="DESCARGAR", command=download_video)
download_button.grid(row=5, column=0, columnspan=2, pady=10)

# Añadir checkbox y etiqueta de información
separate_stems_var = tk.IntVar(value=0)  # Variable para el estado del checkbox
separate_stems_checkbox = tk.Checkbutton(input_frame, text="Separar stems", variable=separate_stems_var)
separate_stems_checkbox.grid(row=6, column=0, columnspan=2, pady=5, sticky='w')

info_label = tk.Label(input_frame, text="ℹ️", fg="blue", cursor="hand2")
info_label.grid(row=6, column=1, sticky='w')
info_label.bind("<Button-1>", show_info)

info_label.grid(row=6, column=1, sticky='w')

# Actualizar el label con la ruta de salida cada vez que cambien los campos de entrada
location_entry.bind('<KeyRelease>', update_output_path_label)
name_entry.bind('<KeyRelease>', update_output_path_label)


# Menú
menubar = tk.Menu(root)
root.config(menu=menubar)

# Menú Archivo
file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Archivo", menu=file_menu)
file_menu.add_command(label="Cambiar ubicación de salida por defecto", command=select_folder)
file_menu.add_command(label="Cambiar ubicación de la plantilla FLP", command=select_template)

root.mainloop()