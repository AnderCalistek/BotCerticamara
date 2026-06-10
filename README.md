#  Automatización Sistema SIGA
### Descarga de Contratos Presenciales (CP) y No Presenciales (CNP)

## el proceso de instalacion esta en la parte final de este archivo.




---

###  Descripción
Este programa automatiza el ciclo de vida completo de descarga y organización de contratos desde la plataforma **SIGA**. El sistema permite procesar dos canales distintos (**Presenciales - CP** y **No Presenciales - CNP**) de forma rápida y efectiva, gestionando la navegación web, la descompresión de archivos y la organización de PDFs finales en carpetas categorizadas.

---

###  Vista Previa de la Interfaz
Aquí puedes ver cómo luce el sistema de automatización en acción:

![Interfaz Principal](codigo/imagenes/Interfaz.png)


---

###  Características Principales
*   **Doble-Canal (CP/CNP)**: Selector dinámico que ajusta mapeos de columnas, carpetas de destino y lógica de búsqueda según el canal.
*   **Interfaz Moderna**: Diseño en modo oscuro construido con `CustomTkinter` para una experiencia profesional.
*   **Dashboard Interactivo**: Consola en tiempo real, barra de progreso y botón de parada de emergencia.
*   **Persistencia de Credenciales**: Sistema de Auto-login seguro que recupera accesos desde Windows Credential Manager.
*   **Guardado Incremental**: El progreso se guarda en el Excel cada 10 filas para evitar pérdida de datos por fallas externas.
*   **Organización Autónoma**: Descompresión y organización automático de PDFs al finalizar el proceso.

---

###  Arquitectura del Sistema
El proceso se divide en **3 fases críticas** coordinadas por un script principal:

1.  **Fase de Descarga (`automatizar_siga.py`)**: El script  que interactúa con SIGA, llena formularios y descarga los ZIPs de contratos.
2.  **Fase de Descompresión (`descomprimir_nuevos.py`)**: Monitorea las descargas y extrae el contenido de los archivos ZIP.
3.  **Fase de Organización (`extraer_pdfs.py`)**: Filtra y mueve exclusivamente los archivos `.pdf` a la carpeta de destino final.

---

###  Estructura del Proyecto
*   `GUI_AUTOMATIZACION.py`: Punto de entrada principal (Panel de control).
*   `PROCESO_COMPLETO.py`: Director principal que coordina todas las fases.
*   `config.py`: Archivo de configuraciones (rutas, columnas y variables globales).
*   `automatizar_siga.py`: Lógica pura de automatización web con Selenium.
*   `dist/SIGA_AUTOMATIZACION_PRO.exe`: Versión compilada "todo-en-uno" para usuarios finales.

---

###  Instalación y Uso

#### A. Para Desarrolladores (Python):
1.  **Instalar dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

#### ¿Qué estamos instalando? (Guía de herramientas):
*   **Selenium**: Es el **"Robot"** principal que abre el navegador y hace los clics por ti.
*   **Webdriver-manager**: Es la libreria que asegura que el robot tenga las piezas correctas para tu Chrome.
*   **Openpyxl**: Es la libreria que se encrga del excel, que lee y escribe los datos de las filas y columnas y llena el excel con los datos de los contratos.
*   **Customtkinter**: Es la libreria que crea la ventana moderna y el modo oscuro.
*   **Keyring**: Es la libreria, que es como una caja fuerte que guarda tus contraseñas de forma segura en Windows. 

2.  **Configurar credenciales**: Ejecuta `setup_siga_credentials.py`. Solo lo harás una vez.
3.  **Lanzar el programa**:
    ```bash
    python GUI_AUTOMATIZACION.py
    ```

#### B. Para Usuarios Finales (.exe):
1.  Ve a la carpeta `dist/`.
2.  Abre **`SIGA_AUTOMATIZACION_PRO.exe`**.
3.  **Configurar accesos (Solo la primera vez):** Pulsa el botón de arriba a la derecha que dice **"⚙ CONFIGURAR ACCESO"** para guardar tu correo y clave de SIGA de forma segura.

![Configuración de Accesos](codigo/imagenes/contraseña.png)

4.  Selecciona el Canal, el archivo Excel y el rango de filas. ¡Dale a **"INICIAR"** y listo.


---

###  Compilación (Actualizar .exe)
Si haces cambios en el código y quieres actualizar el ejecutable, presiona doble clic en el archivo, se abrirá una ventana de comandos, espera a que termine y listo, ya tienes el .exe actualizado con los cambios que hiciste:
```
CONSTRUIR_EJECUTABLE.bat
```

---

> [!IMPORTANT]
> **Requisito del Excel:** Mantén el archivo Excel cerrado mientras el bot trabaja para evitar errores de escritura.

---


