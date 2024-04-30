<p align="center">
  <img src="/icon.ico" alt="Logo FLInit" width="200"/>
</p>

# FL INIT

FL INIT es un script en Python diseñado para facilitar la creación de proyectos en FL Studio a partir de canciones disponibles en YouTube. Este script automatiza el proceso de descarga de audio de YouTube y la configuración inicial de proyectos en FL Studio.

## Características

- **Descarga de audio de YouTube**: Permite descargar canciones directamente de YouTube y guardarlas en formato MP3.
- **Creación automática de proyectos FL Studio**: Genera un archivo .flp utilizando una plantilla proporcionada por el usuario.
- **Separación de stems**: Ofrece la opción de separar los stems de la canción utilizando Demucs.
- **Gestión de configuraciones**: Usa un archivo `settings.ini`, que se crea automáticamente si no existe, para establecer rutas predeterminadas de proyectos y la ruta de las plantillas .flp.

## Requisitos

- Windows 10 o 11
- Python (recomendable 3.7 o superior)
- Las dependencias que se indican en `requirements.txt`: 
  - `pytube==15.0.0`
  - `moviepy==1.0.3`
  - `pyflp==2.2.1`
  - `demucs==4.0.1`
  - `torch==2.3.0`
  - `torchaudio==2.3.0`

## Instalación

1. **Clonar el repositorio**: Descarga el repositorio y colócalo en un directorio fijo para evitar problemas de ruta entre el `fl_init.py` y el archivo `settings.ini`.
2. **Instalar dependencias**: Asegúrate de instalar las dependencias necesarias listadas en `requirements.txt` ejecutando:
```
pip install -r requirements.txt
```
3. **Creación de Acceso Directo**: Es aconsejable crear un acceso directo del archivo `fl_init.py` en una ubicación conveniente para el usuario. Esto facilitará el uso del script y garantizará que el archivo `settings.ini` permanezca en el mismo directorio que el script de Python, evitando problemas de configuración.
4. **Cambiar el Icono del Acceso Directo**: Puedes asignar el `icon.ico` incluido en el repositorio al acceso directo que crees para la aplicación. Esto dará una apariencia coherente y reconocible a tu acceso directo.

## Uso

- **Ejecutar el archivo `fl_init.py`**: La opción más sencilla para ejecutar el programa es abriéndolo con el intérprete de python. Al ejecutar el programa, se abrirá una terminal donde se mostrarán las barras de progreso de la descarga y la separación de stems.
- **Rellenar los campos**: Tendrás que introducir la URL de YouTube, la ubicación del proyecto, el nombre del proyecto y opcionalmente la plantilla .flp que deseas usar (si no se indica nada no creará el archivo .flp). Al rellenar todos los campos, podrás iniciar la descarga. También hay un checkbox opcional para que separe los stems. Ten en cuenta que este proceso utiliza IA (Demucs) y que la velocidad va a variar dependiendo de la GPU. En mi caso, un portátil con una gráfica integrada, me tarda 5 mins.
- **Configuración de la ruta de las plantillas**: Si no te aparece ningún valor en el menú desplegable ten en cuenta que las plantillas las coge de la ruta que tengas en Configuración>Cambiar ubicación de las plantillas FLP.
- **Descarga**: Cuando le das al botón “Descargar”, te creará el directorio que se indica en el label, donde estarán el archivo de FL Studio junto con el audio en formato mp3 (bajo el directorio `/assets`). Si has seleccionado la extracción de los stems, se guardarán en `assets/mdx_extra/`.

## Contribuir

Si deseas contribuir al proyecto, puedes enviar pull requests o abrir issues en este repositorio para sugerir mejoras o reportar errores.
