#!/bin/bash
# shutdown shell script
name=$(lsof -i:5000|tail -1|awk '"$1"!=""{print $2}')
if [ -z $name ]
then
    echo "No process can be used to killed!"
    exit 0
fi
 
id=$(cat /tmp/gunicorn-vc.pid)
kill $id > /dev/null 2>&1

echo "Process name=gunicorn($id) kill!"
exit 0
