@echo off
chcp 65001
break>aos_info.txt
break>tmp1.txt
break>tmp2.txt
break>tmp3.txt
REM Push aapt files to android device
adb push ./GeometrA/static/aapt-arm-pie /data/local/tmp
adb shell chmod 0755 /data/local/tmp/aapt-arm-pie

REM adb shell pm list packages -3 -f >> aos_info.txt

REM get list of packages and put into tmp.txt
@For /F "usebackq tokens=1-2 delims=:" %%i in (`adb shell pm list packages -3 -f`) do echo %%j >> tmp1.txt

@For /F "usebackq tokens=1-2 delims==" %%i in (tmp1.txt) do (
    echo %%i >> tmp2.txt
)
Del tmp1.txt

@For /F %%i in (tmp2.txt) do (
    adb shell /data/local/tmp/aapt-arm-pie d badging %%i >> tmp3.txt
)
Del tmp2.txt

set name=
set version=
@For /F "usebackq tokens=1-2 delims=:" %%i in (tmp3.txt) do (
    If "%%i"=="package" (
        For /F "tokens=1-4" %%a in ("%%j") do (
            echo *********************
            echo %%a
            echo|set /p=%%a >> aos_info.txt
            echo %%c
            echo|set /p=%%c >> aos_info.txt
        )
    )
    If "%%i"=="application-label" (
        echo %%j >> aos_info.txt
    )
)
Del tmp3.txt
adb shell rm -f /data/local/tmp/aapt-arm-pie
