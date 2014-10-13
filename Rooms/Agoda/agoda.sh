#!/bin/sh

basepath=$(dirname "$0")
cd "${basepath}"

source ../spider_util.sh

spiderName=Agoda
cityFile=$1
nightCount=1

init "${cityFile}"

for city in $(cat ${cityFile});
do
    log=${city}-${date}
    isDone=$(isSkip ${log})

    if [ ${isDone} -eq 0 ]; then
        for plusDate in $(echo "45");
        do
            ${SCRAPY} ${SCRAPY_OPTS} ${spiderName} -a city="${city}" -a plusDate=${plusDate} -a nightCount=${nightCount}
            ret=$?
            if [ ${ret} -eq 0 ]; then
                success ${plusDate} ${city} ${log}
                sleep 5
            else
                fail ${ret} '${SCRAPY} ${SCRAPY} ${spiderName} -a city="${city}" -a plusDate=${plusDate}'
            fi
        done

        echo "${log}" >> ${logPath}
    else
        echo "Skip ${city}"
    fi
done
