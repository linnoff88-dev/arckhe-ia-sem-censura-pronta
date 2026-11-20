@echo off
cd /d "%~dp0"
py ia.py conversar
if errorlevel 1 pause
