Set oShell = CreateObject("WScript.Shell")
Dim strDir, strPath, strIconPath

' Ajustar el directorio para apuntar a la raíz del proyecto, subiendo un nivel desde /dist
strDir = oShell.CurrentDirectory
strDir = strDir & "\.."

' Ruta del script de Python o del .bat para ejecutar
strPath = strDir & "\dist\start_app.bat"

' Ruta del archivo de icono
strIconPath = strDir & "\assets\icon.ico"

' Crear el acceso directo en la raíz del proyecto
Set oLink = oShell.CreateShortcut(strDir & "\FL Init.lnk")

oLink.TargetPath = strPath
oLink.WindowStyle = 1
oLink.IconLocation = strIconPath
oLink.Description = "Acceso directo a la aplicación"
oLink.WorkingDirectory = strDir
oLink.Save
