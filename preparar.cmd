@echo off
cd /d "%~dp0"
py ia.py preparar
if errorlevel 1 pause
