@echo off
call clasp pull
call npm run build
call clasp push

@REM non funziona perché non c'è clasp