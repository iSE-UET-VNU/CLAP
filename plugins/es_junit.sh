#!/bin/sh
if [ "${1}" = "-src" ]; then
    SRC_DIR=${2};
fi;

if [ "${3}" = "-test" ]; then
    TEST_DIR=${4};
fi;

if [ "${5}" = "-build.classes" ]; then
    SRC_CLASSES_DIR=${6};
fi;

if [ "${7}" = "-build.testclasses" ]; then
    TEST_CLASSES_DIR=${8};
fi;

if [ "${9}" = "-report.coveragedir" ]; then
    COVERAGE_DIR=${10};
fi;

if [ "${11}" = "-junit.haltonfailure" ]; then
    JUNIT_HALT_ON_FALURE=${12};
fi;

BASEDIR=$(dirname "$0")
ANT_PATH="$BASEDIR/apache-ant-1.10.7";

$ANT_PATH/bin/ant clover.all -buildfile $ANT_PATH/junit_build.xml -Dsrc $SRC_DIR -Dtest $TEST_DIR -Dbuild.classes $SRC_CLASSES_DIR -Dbuild.testclasses $TEST_CLASSES_DIR -Dreport.coveragedir $COVERAGE_DIR -Djunit.haltonfailure=$JUNIT_HALT_ON_FALURE