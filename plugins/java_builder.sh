#!/bin/sh
if [ "$1" = "-src" ]; then
    SRC_DIR=$2;
fi;

if [ "$3" = "-out" ]; then
    OUTPUT_CLASSES_DIR=$4;
fi;

BASEDIR=$(dirname "$0")
ANT_PATH="$BASEDIR/apache-ant-1.10.7";

echo "Building project from source code [$SRC_DIR]";
$ANT_PATH/bin/ant -buildfile $ANT_PATH/javac_build.xml -Dsrc $SRC_DIR -Dout $OUTPUT_CLASSES_DIR