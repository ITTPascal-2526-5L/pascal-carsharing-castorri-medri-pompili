@echo off
call clasp pull
call npm run build
call clasp push