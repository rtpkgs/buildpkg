@echo off 
pyinstaller -F .\buildpkg.py 
copy .\dist\buildpkg.exe buildpkg.exe
rd /s /Q .\__pycache__
rd /s /Q .\build
rd /s /Q .\dist
del .\buildpkg.spec
pause