#!/bin/bash
# random_file_generator.sh

BS=$(shuf -i 1-200 -n 1)
COUNT=$(shuf -i 1-10 -n 1)
TEMPFILE=$(tempfile -d ./)

dd if=/dev/urandom of=$TEMPFILE bs=$BS count=$COUNT  > /dev/null 2>&1
