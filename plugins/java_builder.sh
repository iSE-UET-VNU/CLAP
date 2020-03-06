#!/bin/sh
if [ "$1" = "-project" ]; then
    PROJECT_PATH=$2;
fi;
BASEDIR=$(dirname "$0")
ANT_PATH="$BASEDIR/apache-ant-1.10.7";

echo "Building project from source code [$PROJECT_PATH]";
$ANT_PATH/bin/ant -buildfile $ANT_PATH/javac_build.xml -Dbase_path $PROJECT_PATH