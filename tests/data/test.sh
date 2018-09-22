#! /bin/bash

i=0
while [[ $i -lt 5 ]]; do
    echo $i;
    >&2 echo $i;
    sleep 0.1;
    i=$[$i+1]
done
