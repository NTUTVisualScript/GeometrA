function remWS {
    if [ -z "${1}" ]; then
        cat | tr -d '[:space:]'
    else
        echo "${1}" | tr -d '[:space:]'
    fi
}

RESULT=$(adb shell "[ -f "/data/local/tmp/aapt-arm-pie" ] || echo 1")
if [ -z "$RESULT" ]; then
  echo "File exists";
else
  $(adb push ./GeometrA/static/aapt-arm-pie /data/local/tmp)
  $(adb shell chmod 0755 /data/local/tmp/aapt-arm-pie)
fi


" " > aos_info.txt
for pkg in `adb shell pm list packages -3 -f | awk -F= '{sub("package:","");print $1}'`
do
  adb shell /data/local/tmp/aapt-arm-pie d badging $pkg | awk -F: '
  $1 == "package" { split($2,space," ")
name=space[1];version=space[3]}
$1 == "application-label" {print name, version, $2 }' >> ./aos_info.txt
done

adb shell rm -f /data/local/tmp/aapt-arm-pie
