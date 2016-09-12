all:
	python3 fetcher.py


spark:
	./scripts/deploy.sh
	ssh ubuntu@192.168.130.181 "cd jmq && ./scripts/run-python-in-cluster.sh"
