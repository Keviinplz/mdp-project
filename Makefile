current_dir := $(realpath .)

run-test-full:
	cat $(current_dir)/data/testing/sample.csv | ./main.py --mapper=user | sort | ./main.py --reducer=user | sort | ./main.py --mapper=quantity | sort | ./main.py --reducer=quantity > ${current_dir}/data/results/test-output.tsv

run-test:
	cat $(current_dir)/data/testing/sample.csv | ./main.py --mapper=user | sort | ./main.py --reducer=user > ${current_dir}/data/results/test-output.tsv

run:
	cat $(current_dir)/data/production/table.csv | ./main.py --mapper=user | sort | ./main.py --reducer=user > ${current_dir}/data/results/output.tsv