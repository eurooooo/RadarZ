@echo off
echo Starting RadarZ Development Environment...
echo.

REM 启动后端（在新窗口）
start "RadarZ Backend" cmd /k "cd /d %~dp0backend && uv run fastapi dev main.py"

REM 等待一秒让后端启动
timeout /t 1 /nobreak >nul

REM 启动前端（在新窗口）
start "RadarZ Frontend" cmd /k "cd /d %~dp0frontend && pnpm dev"

echo.
echo Both servers are starting in separate windows...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to close this window (servers will continue running)...
pause >nul

