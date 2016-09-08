#!/bin/bash


# TODO: fix me!

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
# <spark-master> = spark://172.27.11.11:7077
# <your-main-class> = cz.datamole.experiment1.Main
# <your-assembled.jar> = experiment1-assembly-1.0.0-SNAPSHOT.jar


# VARIOUS
#
# when submitting to cluster, memory is determined separately for driver
# (--driver-memory) and for *each* executor process (--executor-memory)
#
# additional configuration examples, that we have used:
#        --conf="spark.local.dir=/var/tmp/" \
#        --conf="spark.network.timeout=1800" \
#        --driver-java-options="-Dcz.datamole.projectmilka.partitionCount=400" \


mkdir -p logs

tmux new -s spark_first_run_$(date +"%F_%H-%M-%S") '\

    (time /opt/spark-1.6.1-bin-hadoop2.6/bin/spark-submit \
        --driver-memory 1g \
        --executor-memory 2g \
        --master spark://172.27.11.11:7077 \
        source/spark/spark.py ) \
    2>&1 | tee logs/$(date +"%F_%H-%M-%S").out'
