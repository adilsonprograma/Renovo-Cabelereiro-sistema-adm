Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = CreateObject("Scripting.FileSystemObject").GetAbsolutePathName(".")
WshShell.Run "cmd /c python app.py", 0, False
Wscript.Sleep 1500
WshShell.Run "cmd /c start microsoft-edge:http://127.0.0.1:5000", 0, False
