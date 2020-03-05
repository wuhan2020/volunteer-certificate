#!/bin/bash
# restart shell script
cd `dirname $0`
./stop.sh
./start.sh
