#!/bin/bash

pps=${1:-50}
mins=${2:-2}
total=$((mins * 60))
end=$((SECONDS + total))

while [ $SECONDS -lt $end ]; do
  for i in {1..$pps}; do curl -s http://localhost:8000/products > /dev/null & done
  sleep 1
done

wait