@echo off
echo ===================================================
echo Melo's Music - Flutter Mobile App Setup
echo ===================================================
echo.
echo Checking if Flutter is installed...
where flutter >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Flutter SDK is not installed or not in your PATH!
    echo Please download and install Flutter from: https://docs.flutter.dev/get-started/install/windows
    echo Once installed and added to your PATH, run this script again.
    pause
    exit /b 1
)

echo Flutter is installed! 
echo Generating native Android, iOS, and Web platform files...
cd mobile_app
call flutter create .

echo.
echo Fetching dependencies...
call flutter pub get

echo.
echo Setup Complete! 
echo You can now open the "mobile_app" folder in Android Studio or VS Code.
echo To run the app on a connected device or emulator, type:
echo cd mobile_app
echo flutter run
pause
