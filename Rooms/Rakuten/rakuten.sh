#!/bin/sh

basepath=$(dirname "$0")
cd "${basepath}"

source ../spider_util.sh

spiderName=Rakuten
cityFile=$1

init "${cityFile}"

for city in $(cat ${cityFile});
do
    cityName=$(echo ${city} | cut -d "," -f1)
    cityCode=$(echo ${city} | cut -d "," -f2)

    for plusDate in $(echo "45");
    do
        log=${city}-${plusDate}
        isDone=$(isSkip ${log})

        if [ ${isDone} -eq 0 ]; then
            ${SCRAPY} ${SCRAPY_OPTS} ${spiderName} -a city="${cityName}" -a plusDate=${plusDate} -a num=${cityCode}
            ret=$?
            if [ ${ret} -eq 0 ]; then
                success ${plusDate} ${cityName} ${log}
                sleep 2
            else
                fail ${ret} '${SCRAPY} ${SCRAPY} ${spiderName} -a city="${cityName}" -a plusDate=${plusDate} -a num=${cityCode}'
            fi
            echo "${log}" >> ${logPath}
        else
            echo "Skip ${log}"
        fi
    done
done
