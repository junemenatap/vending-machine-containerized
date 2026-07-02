#!/bin/bash

item=${1:-test}
pps=${2:-100}

for ((i=1; i<=pps; i++)); do
    curl -s -X POST "http://localhost:8000/products/buy/${item}" > /dev/null &
done
wait