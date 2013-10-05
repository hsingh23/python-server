#!/usr/bin/python
import requests as r
from timeit import timeit
files = ["1b", "100b", "1000b", "10000b", "100000b", "1000000b"]
for f in files:
    stmt = "r.get('http://localhost:9000/%s')" % f
    setup = "import requests as r"
    times = []
    for x in range(10):
        times.append(timeit(stmt=stmt, setup=setup, number=1))
    print "Non concurrent", f, sum(times) / len(times)
    times = []
    for x in range(10):
        times.append(timeit(stmt=stmt, setup=setup, number=4))
    print "4 connections at once", f, sum(times) / len(times)
