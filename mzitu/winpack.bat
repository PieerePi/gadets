mkdir temp
cd temp
pyinstaller -F --icon="..\mzitu.ico" ..\getmzitu.py
copy dist\getmzitu.exe ..\
cd ..
rmdir /S /Q temp __pycache__
pause