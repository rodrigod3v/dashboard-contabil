@echo off
title Gerador de ID - Dashboard Contabil
cls
echo ========================================================
echo      GERADOR DE IDENTIFICACAO UNICA (HWID)
echo ========================================================
echo.
echo Obtendo o serial da sua maquina...
echo.

for /f "skip=1 delims=" %%i in ('wmic csproduct get uuid') do (
    for /f "delims=" %%j in ("%%i") do (
        set "HWID=%%j"
        goto :Found
    )
)

:Found
if "%HWID%"=="" (
    echo Erro ao obter ID. Tente executar como Administrador.
    pause
    exit
)

echo.
echo --------------------------------------------------------
echo SEU ID: %HWID%
echo --------------------------------------------------------
echo.
echo Identificacao copiada para a area de transferencia!
echo Cole este codigo no site para fazer login.
echo.
echo %HWID%| clip

pause
