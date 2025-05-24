@echo off
set base_dir=%~dp0
%base_dir:~0,2%
pushd %base_dir% 1>nul 2>&1

set wintemp=%SYSTEMROOT%\temp
set _LOG_FILE=%wintemp%\MvFGDriverLog.log

echo [%date% %time%] >> %_LOG_FILE%

:: ���뽫֤���ļ�
certutil.exe -f -addstore "TrustedPublisher" MvVirtualSerial_Microsoft.cer >> %_LOG_FILE%
certutil.exe -f -addstore "TrustedPublisher" MvVirtualSerial_SHA256.cer >> %_LOG_FILE%
certutil.exe -f -addstore "TrustedPublisher" MvVirtualSerial_SHA256_EV.cer >> %_LOG_FILE%
echo. >> %_LOG_FILE%

:: ����������־��¼
call StartTrace.cmd >> %_LOG_FILE%

:: ��װ�����ļ���ˢ���豸�б�
MvDriverInstall.exe /i MvVirtualSerial.inf MVFGVIRTUALCOMBUS\CAMPORT >> %_LOG_FILE%
MvDriverInstall.exe /i MvVirtualSerial.inf MVFGVIRTUALCOMBUS\PSPORT >> %_LOG_FILE%

echo. >> %_LOG_FILE%