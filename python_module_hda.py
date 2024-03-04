import hou
import sys
import os
from importlib import reload 

#PATH of the cloned git !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#path = "C:/Users/carlo/Desktop/gdrive"

sys.path.append("C:/Users/carlo/Desktop/python4production/WEEK3/repos/houdiniUtils")
import gdrive
reload(gdrive)

#STEP 1
#I made this step just to create a custom folder to dont mesh with paths, but you can type any route you want
#This method is the same we did in class. Also the user can specify a custom name without the file extensions
#If there is no input a default name with the version is added
def setPath():
    default_path = hou.pwd().parm("filename").evalAsString()
    dest_path = "/".join(default_path.split("/")[:-1])
    hip_path = hou.text.expandString("$HIP")
    hipname_path = hou.text.expandString("$HIPNAME")
    backup_folder = hip_path + "/gdrive"
    try:
        file_version = len([file for file in os.listdir(backup_folder) if file.endswith("abc")])
    except:
        os.mkdir(backup_folder)
        file_version = len([file for file in os.listdir(backup_folder) if file.endswith("abc")])
        
    backup_path = f"{hip_path}/gdrive/$HIPNAME.alembic_v{file_version}.abc"
    custom = hou.pwd().parm("custom_name").evalAsString()
    if custom !="":
        backup_path = f"{hip_path}/gdrive/{custom}.abc"
    else:
        backup_path = f"{hip_path}/gdrive/{hipname_path}.alembic_v{file_version}.abc"
    hou.pwd().parm("filename").set(backup_path)

#STEP 3
#This method calls the gdrive class which is encharged of calling the google drive Api to upload the file from the same
#path we did the alembic save in step 2.
def uploadDrive():
    file_path = hou.pwd().parm("filename").evalAsString()
    gd = gdrive.gdrive()
    gd.execute(file_path)