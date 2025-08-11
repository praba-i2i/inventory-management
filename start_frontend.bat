@echo off
echo Starting React Frontend Server...
echo.

cd frontend

echo Installing Node.js dependencies...
npm install

echo.
echo Starting React development server on http://localhost:3000
echo.

npm start

pause
