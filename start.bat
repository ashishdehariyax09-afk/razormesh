@echo off
title RazorMesh: Autonomous Agentic Commerce Gateway
color 0B

echo ======================================================================
echo    RAZORMESH: AUTONOMOUS AGENTIC COMMERCE GATEWAY v2.0
echo    Track 01: Autonomous Agentic Commerce - Razorpay AI Buildathon 2026
echo ======================================================================
echo.

echo [1/2] Running 15-Case Adversarial Test Suite...
python test_adversarial.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Test suite failed. Please check dependencies.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [2/2] Launching RazorMesh Gateway & Mission Control Cockpit...
python run.py

pause
