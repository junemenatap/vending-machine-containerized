#!/bin/bash

pps=${1:-100}
mins=${2:-2}
total=$((mins * 60))
end=$((SECONDS + total))

while [ $SECONDS -lt $end ]; do
    for i in {1..$pps}; do
        curl -s -X POST "http://localhost:8000/products/buy/test" > /dev/null &
    done
    wait
done

wait