#!/bin/sh

action=$1

for room in $(echo Agoda Rakuten);
do
    python service.py -p ${room} -a ${action}

    if [ ${action} == "stop" ]; then
        for pid in $(ps aux | grep ${room} | grep scrapy | awk '{print $2}');
        do
            kill ${pid}
        done
    fi
done
