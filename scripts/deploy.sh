#!/bin/sh
HOST=192.168.130.181
ADDR=$HOST:/home/ubuntu/jmq
USER=ubuntu
OPTIONS='-azP --delete'

rsync $OPTIONS\
 --exclude 'data/'\
 --exclude '\.*'\
 . $USER@$ADDR
