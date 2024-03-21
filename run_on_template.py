import hou
import os

DIRPATH = "C:/Users/carlo/Desktop/python4production/WEEK6/avatar"

def grab_sop_create(root):
	return [node for node in root.children() if node.type().name() == "sopcreate"][0]

def grab_gltf_hierarchy(root):
	return [node for node in root.children() if node.type().name() == "gltf_hierarchy"][0]

def updateMaterials(asset_name,materiallib_lop):
		materiallib_lop.parm("matnet").set(f"/obj/{asset_name}/materials")
		materiallib_lop.parm("materials").set(0)
		materiallib_lop.parm("fillmaterials").pressButton()

		for i in range(materiallib_lop.parm("materials").eval()):
			geo = materiallib_lop.parm(f"matpath{i+1}").eval()
			materiallib_lop.parm(f"geopath{i+1}").set(f"/{asset_name}/{asset_name}/{geo}")


def batch_process_usd(dir_path):
	files = [file for file in os.listdir(dir_path) if file.endswith(".glb")]
	for obj_file in files:
		asset_name = obj_file[:-4]

		#GLTF HIERARCHY
		gltf_hierarchy = grab_gltf_hierarchy(hou.node("/obj"))
		gltf_hierarchy.parm("filename").set(dir_path + "/" + asset_name +".glb")
		gltf_hierarchy.parm("assetfolder").set(dir_path + "/" + asset_name + "_maps")
		gltf_hierarchy.parm("buildscene").pressButton()


		#STAGE OPERATIONS
		primitive_lop = hou.node("/obj/lopnet1/primitive1")
		primitive_lop.parm("primpath").set(asset_name)

		sop_create_lop = grab_sop_create(hou.node("/obj/lopnet1"))
		sop_context_file = hou.node(sop_create_lop.path() + "/sopnet/create/gltf1")
		sop_context_file.parm("filename").set(dir_path + "/" + obj_file)
		sop_create_lop.setName(asset_name)

		#Repeat Material Operations
		materiallib_lop = hou.node("/obj/lopnet1/materiallibrary1")
		updateMaterials(asset_name,materiallib_lop)

		rop_output = hou.node("/obj/lopnet1/usd_rop1")
		rop_output.parm("lopoutput").set(dir_path + "/usd_export/" + asset_name + ".usd")
		rop_output.parm("execute").pressButton()

batch_process_usd(DIRPATH)
