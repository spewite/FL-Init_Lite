import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from pytube import YouTube
from configparser import ConfigParser
from moviepy.editor import AudioFileClip
import pyflp

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

# Función para descargar solo audio y convertirlo a MP3
def download_video():
    url = url_entry.get()
    project_location = location_entry.get()
    project_name = name_entry.get()
    
    if not url or not project_location or not project_name:
        messagebox.showerror("Error", "Todos los campos son necesarios")
        return
    
    try:
        yt = YouTube(url)
        title = yt.title
        # Limpieza del título para evitar problemas en el nombre del archivo
        safe_title = ''.join(char for char in title if char.isalnum() or char in " -_")
        
        project_path = os.path.join(project_location, project_name)
        assets_path = os.path.join(project_path, 'assets')
        os.makedirs(assets_path, exist_ok=True)
        
        audio_stream = yt.streams.filter(only_audio=True).first()  # Selecciona el mejor stream de audio
        audio_file_path = audio_stream.download(output_path=assets_path, filename=f"{safe_title}.mp4")  # Guarda como .mp4
        
        # Convertir el archivo de audio a MP3
        mp3_path = os.path.join(assets_path, f'{safe_title}.mp3')
        audio_clip = AudioFileClip(audio_file_path)
        audio_clip.write_audiofile(mp3_path)
        audio_clip.close()
        
        # Opcional: eliminar el archivo original descargado
        os.remove(audio_file_path)
        
        create_flp(project_path, project_name)

        open_folder(project_path)  # Abrir el directorio después de descargar y convertir
    except Exception as e:
        messagebox.showerror("Error", f"Error al descargar el audio: {str(e)}")


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



# GUI setup
root = tk.Tk()
root.title("FL INIT")

# Calcular posición para centrar la ventana
window_width = 700
window_height = 250
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width/2)
center_y = int(screen_height/2 - window_height/2)

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

# Actualizar el label con la ruta de salida cada vez que cambien los campos de entrada
location_entry.bind('<KeyRelease>', update_output_path_label)
name_entry.bind('<KeyRelease>', update_output_path_label)

# Menú
menubar = tk.Menu(root)
root.config(menu=menubar)

# Menú Archivo
file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Archivo", menu=file_menu)
file_menu.add_command(label="Cambiar ubicación de descarga", command=select_folder)
file_menu.add_command(label="Cambiar ubicación de la plantilla FLP", command=select_template)

root.mainloop()