#!/bin/sh

ws_path=$(dirname $0)

run(){
    local scrapy=$1
    local which_hotel=$2

    for city in $(ls ${which_hotel}/city*.cfg);
    do
        city=$(basename ${city})
        ${scrapy} ${city}
    done
}

run ${ws_path}/Agoda/agoda.sh ${ws_path}/Agoda &
run ${ws_path}/Rakuten/rakuten.sh ${ws_path}/Rakuten &

wait
