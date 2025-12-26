@echo off
setlocal

:: 提示用戶輸入IP地址
set /p ip="Enter Ping IP address: "

:loop
:: 獲取當前日期並格式化為 YYYY-MM-DD
for /f "tokens=1-3 delims=/ " %%a in ("%date%") do (
    set _today=%%a-%%b-%%c
)

:: 設定日誌文件名稱
set logfile=%_today%_ping_log.txt

:: 對指定的 IP 地址進行一次 ping
ping -n 1 %ip% > nul
if %errorlevel%==0 (
    echo %date% %time%: %ip% - Success >> "%logfile%"
    echo %date% %time%: %ip% - Success
) else (
    echo %date% %time%: %ip% - Fail >> "%logfile%"
    echo %date% %time%: %ip% - Fail
)

:: 暫停 1 秒，然後繼續下一次 ping
timeout /t 1 > nul
goto loop
