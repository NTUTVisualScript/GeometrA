exec &> $HOME/.geometra/logfile.txt

remWS () {
    if [ -z "${1}" ]; then
        cat | tr -d '[:space:]'
    else
        echo "${1}" | tr -d '[:space:]'
    fi
}

RESULT=$($GEOMETRA_RESOURCE/adb_resources/mac/adb shell "[ -f "/data/local/tmp/aapt-arm-pie" ] || echo 1")
if [ -z "$RESULT" ]; then
  echo "File exists";
else
  $GEOMETRA_RESOURCE/adb_resources/mac/adb push $GEOMETRA_RESOURCE/aapt-arm-pie /data/local/tmp
  $GEOMETRA_RESOURCE/adb_resources/mac/adb shell chmod 0755 /data/local/tmp/aapt-arm-pie
fi


> $HOME/.geometra/aos_info.txt
for pkg in `$GEOMETRA_RESOURCE/adb_resources/mac/adb shell pm list packages -3 -f | awk -F= '{sub("package:","");print $1}'`
do
  $GEOMETRA_RESOURCE/adb_resources/mac/adb shell /data/local/tmp/aapt-arm-pie d badging $pkg | awk -F: '
  $1 == "package" { split($2,space," ")
name=space[1];version=space[3]}
$1 == "application-label" {print name, version, $2 }' >> $HOME/.geometra/aos_info.txt
done

$GEOMETRA_RESOURCE/adb_resources/mac/adb shell rm -f /data/local/tmp/aapt-arm-pie
