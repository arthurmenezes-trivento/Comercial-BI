@echo off
REM Executa o script process_pbix.py a partir da pasta do repositório.
cd /d "%~dp0"
if exist "%~dp0\process_pbix.py" (
    py "%~dp0\process_pbix.py" %*
    if errorlevel 1 (
        python "%~dp0\process_pbix.py" %*
    )
) else (
    echo Nao foi encontrado o arquivo process_pbix.py no mesmo diretório deste .bat.
    pause
)
