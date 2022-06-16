current_dir := $(realpath .)

run-test:
	cat $(current_dir)/data/testing/sample.csv | ./main.py --mapper=user | sort | ./main.py --reducer=user > ${current_dir}/data/results/test-output.tsv

run:
	cat $(current_dir)/data/production/table.csv | ./main.py --mapper=user | sort | ./main.py --reducer=user > ${current_dir}/data/results/output.tsv