#!/bin/bash

mins=${1:-2}
total=$((mins * 60))
end=$((SECONDS + total))

while [ $SECONDS -lt $end ]; do
  for i in {1..1000}; do curl -s http://localhost:8000/products > /dev/null & done
  sleep 30
done

wait