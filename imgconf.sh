#!/bin/bash

for x in /etc/image-config.d/*.sh
do
sh "$x" 
done
