#!/bin/bash

for filename in C:/Users/carlo/Desktop/python4production/WEEK4/test_objs/*.fbx; do
	hython script.py "C:/Users/carlo/Desktop/python4production/WEEK4/main_basic_template.hip" "$filename"
done