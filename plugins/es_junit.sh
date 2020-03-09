#!/bin/sh
if [ "$1" = "-main" ]; then
    SRC_CLASSES_DIR=$2;
fi;

if [ "$3" = "-test" ]; then
    TEST_CLASSES_DIR=$4;
fi;

BASEDIR=$(dirname "$0")
ANT_PATH="$BASEDIR/apache-ant-1.10.7";

echo "Testing classes with supplied test cases [$SRC_CLASSES_DIR]";
$ANT_PATH/bin/ant junit -buildfile $ANT_PATH/junit_build.xml -Dmain $SRC_CLASSES_DIR -Dtest $TEST_CLASSES_DIR