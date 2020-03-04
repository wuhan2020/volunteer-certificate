#!/bin/bash
# shutdown shell script
name=$(lsof -i:5000|tail -1|awk '"$1"!=""{print $2}')
if [ -z $name ]
then
    echo "No process can be used to killed!"
    exit 0
fi
id=$(lsof -i:80|tail -1|awk '"$1"!=""{print $2}')
kill $id > /dev/null 2>&1

echo "Process name=$name($id) kill!"
exit 0
