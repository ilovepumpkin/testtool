#!/bin/sh

ssh shenrui@9.71.44.38 ls -t /build/$1|awk '/^[0-9]+[a-z]*$/{print $1}'|head -n1

