#!/bin/bash

MAIN_FOLDER="C:/Users/carlo/Desktop/python4production/WEEK6/avatar"

for SUBFOLDER in "$MAIN_FOLDER"/*; do
	if [ -d "$SUBFOLDER" ]; then
		echo "Processing $SUBFOLDER"
		hython run_on_template_2.py "C:/Users/carlo/Desktop/python4production/WEEK6/gltf_to_usd/template.hip" "$SUBFOLDER"

	fi
done