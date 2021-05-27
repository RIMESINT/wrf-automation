#!/usr/bin/env bash

# disable NUMA Balancing 
echo 0 > /proc/sys/kernel/numa_balancing

# disable ASLR
echo 0 > /proc/sys/kernel/randomize_va_space
