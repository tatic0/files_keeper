#!/bin/bash
# random_file_spread.sh

for i in file*; do
  cp -v $i `tempfile -d ./`
done
