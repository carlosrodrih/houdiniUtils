import hou
from importlib import reload
import sys

sys.path.append("C:/Users/carlo/Desktop/python4production/WEEK6/houdiniUtils")

import usd_migration_tools
reload(usd_migration_tools)

template1 = usd_migration_tools.USDmigrationUtils()
template1.createMainTemplate("C:/Users/carlo/Desktop/python4production/WEEK6/assets/cgaxis_110_54_thatch_palm_fbx")