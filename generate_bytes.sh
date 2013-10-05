#!/bin/bash
dd if=/dev/urandom of=1b bs=1 count=1
dd if=/dev/urandom of=100b bs=100 count=1
dd if=/dev/urandom of=1000b bs=1000 count=1
dd if=/dev/urandom of=10000b bs=10000 count=1
dd if=/dev/urandom of=100000b bs=100000 count=1
dd if=/dev/urandom of=1000000b bs=1000000 count=1