#!/bin/bash
sudo ./mouse &
sleep 5s
while [ true ]
do
	python plotmouse.py &
	sleep 15s
	kill $!
	kill $!
done

