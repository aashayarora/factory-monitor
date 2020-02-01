#!/bin/bash

for x in /etc/image-config.d/*.sh; do source "$x"; done
