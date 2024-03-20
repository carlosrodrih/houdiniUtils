#!/bin/bash

MAIN_FOLDER="C:/Users/carlo/Desktop/python4production/WEEK6/assets"

for SUBFOLDER in "$MAIN_FOLDER"/*; do
	if [ -d "$SUBFOLDER" ]; then
		echo "Processing $SUBFOLDER"
		hython run_on_template_2.py "C:/Users/carlo/Desktop/python4production/WEEK6/asset_migration_tool/asset_to_usd_0001.hip" "$SUBFOLDER"

	fi
done