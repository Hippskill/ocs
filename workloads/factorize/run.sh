rm -rf working_directory
mkdir working_directory

python3 src/generate.py working_directory/to_factorize.in

./factorize working_directory/to_factorize.in working_directory/to_factorize.out
