#!/bin/bash
x=10
while true; do
	echo "$x"
	if (( x >= 100 )); then
		break
	fi
	sleep 1s
	x=$(echo "$x + 10" | bc)
done
