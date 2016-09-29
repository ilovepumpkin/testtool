#!/bin/sh

ssh likezhao@9.71.44.38 ls -t /$1/$2|awk '/^[0-9]+[a-z]*$/{print $1}'|head -n1

