#!/usr/bin/python3
from readcsv import Reader

test=Reader()
test.read_csv("../draws/draws1.csv")
test.split()