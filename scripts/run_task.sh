#!/bin/bash

# TODO: fix me

# always launch your experiment via this script.
# it ensures that experiment can be easily re-launched.
# it also launches experiment process in tmux session, which ensures long-running process to survive
# ssh-termination and let's you list (via tmux ls) all running experiments on your system.

# USAGE
#
# substitute all expressions in '<' '>'.
#
# e.g.:
# <spark-home> = /opt/spark-1.6.1-bin-hadoop2.6/
# <your-main-class> = cz.datamole.experiment1.Main
# <your-assembled.jar> = experiment1-assembly-0.1.jar


# VARIOUS
#
# in local mode (--master 'local[*]', memory is determined only by --driver-memory
# (both for driver and workers, since all run in single java process)

# additional configuration examples, that we have used:
#         --conf="spark.local.dir=/var/tmp/" \
#         --driver-java-options="-Dcz.datamole.associationrules.partitionCount=200" \



mkdir -p logs

tmux new -s github_api_fetch_$(date +"%F_%H-%M-%S") '\

    (time /opt/spark-1.6.1-bin-hadoop2.6/bin/spark-submit \
        --driver-memory 1G \
        --master 'local[*]' \
        --py-files /home/ubuntu/jmq /home/ubuntu/jmq/github_api_fetcher.py \
    2>&1 | tee logs/$(date +"%F_%H-%M-%S").out
'
