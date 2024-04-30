Set oShell = CreateObject("WScript.Shell")
Dim strDir, strPath, strIconPath, strDesktopPath

' Activar manejo de errores básico
On Error Resume Next

' Ajustar el directorio para apuntar a la raíz del proyecto, subiendo un nivel desde /dist
strDir = oShell.CurrentDirectory
strDir = strDir & "\.."

' Ruta del script de Python o del .bat para ejecutar
strPath = strDir & "\dist\start_app.bat"

' Ruta del archivo de icono
strIconPath = strDir & "\assets\icon.ico"

' Obtener la ruta del escritorio del usuario actual
strDesktopPath = oShell.SpecialFolders("Desktop")

' Crear el acceso directo en la raíz del proyecto
Set oLink = oShell.CreateShortcut(strDir & "\FL Init.lnk")
oLink.TargetPath = strPath
oLink.WindowStyle = 1
oLink.IconLocation = strIconPath
oLink.Description = "Acceso directo a la aplicación"
oLink.WorkingDirectory = strDir
oLink.Save

' Verificar si se produjo un error y manejarlo
If Err.Number <> 0 Then
    WScript.Echo "Error creando acceso directo en la raíz del proyecto: " & Err.Description
    Err.Clear ' Limpiar el error
End If

' Crear el acceso directo en el escritorio
Set oLinkDesktop = oShell.CreateShortcut(strDesktopPath & "\FL Init.lnk")
oLinkDesktop.TargetPath = strPath
oLinkDesktop.WindowStyle = 1
oLinkDesktop.IconLocation = strIconPath
oLinkDesktop.Description = "Acceso directo a la aplicación"
oLinkDesktop.WorkingDirectory = strDir
oLinkDesktop.Save

' Verificar si se produjo un error y manejarlo
If Err.Number <> 0 Then
    WScript.Echo "Error creando acceso directo en el escritorio: " & Err.Description
    Err.Clear ' Limpiar el error
End If

' Desactivar manejo de errores básico
On Error Goto 0
