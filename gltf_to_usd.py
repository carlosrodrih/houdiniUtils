import hou
import os
class gltfToUSD:
	def __init__(self):
		self.root_path = "/obj"
		self.asset_name = ""

	def test(self):
		print("Hello from Gltf to USD tools")

	def createGltfHierarchy(self,dir_path):
		print("Extracting textures...")
		hierarchy = hou.node(self.root_path).createNode("gltf_hierarchy", self.asset_name)
		hierarchy.parm("filename").set(dir_path + "/" + self.asset_name + ".glb")
		hierarchy.parm("assetfolder").set(dir_path + "/" + self.asset_name + "_maps")
		hierarchy.parm("flattenhierarchy").set(1)
		hierarchy.parm("importcustomattributes").set(0)
		hierarchy.parm("buildscene").pressButton()

	def createMaterials(self,materiallib_lop):
		print("Linking materials...")
		materiallib_lop.parm("matnet").set(f"{self.root_path}/{self.asset_name}/materials")
		materiallib_lop.parm("materials").set(0)
		materiallib_lop.parm("fillmaterials").pressButton()

		for i in range(materiallib_lop.parm("materials").eval()):
			geo = materiallib_lop.parm(f"matpath{i+1}").eval()
			materiallib_lop.parm(f"geopath{i+1}").set(f"/{self.asset_name}/{self.asset_name}/{geo}")

	def createTemplate(self,dir_path):
		print("Executing template structure...")
		obj_file = [file for file in os.listdir(dir_path) if file.endswith(".glb")][0]
		self.asset_name = obj_file[:-4]
		print(self.asset_name)

		self.createGltfHierarchy(dir_path)

		#lop network
		lop_network = hou.node(self.root_path).createNode("lopnet")
		lop_path = lop_network.path()
		print(lop_path)

		#sopcreate lop
		sopcreate_lop = hou.node(lop_path).createNode("sopcreate",self.asset_name)
		sopcreate_lop.parm("enable_partitionattribs").set(0)

		#glt file
		file_sop = hou.node(sopcreate_lop.path() + "/sopnet/create").createNode("gltf")
		file_sop.parm("filename").set(dir_path + "/" + obj_file)
		file_sop.parm("usecustomattribs").set(0)
		file_sop.parm("materialassigns").set(1)

		#wrangler
		attr_wrangle = file_sop.createOutputNode("attribwrangle")
		attr_wrangle.parm("class").set(1)
		attr_wrangle.parm("snippet").set('string component = split(s@shop_materialpath, "/")[-1];\ns@path = "/" + component;')

		#attrib delete (in case we want to delete something)
		att_delete = attr_wrangle.createOutputNode("attribdelete")
		#att_delete.parm("ptdel").set("")
		att_delete.parm("primdel").set("name shop_materialpath")

		#output
		output_sop = att_delete.createOutputNode("output")

		#create primitive
		primitive_lop = hou.node(lop_path).createNode("primitive")
		primitive_lop.parm("primpath").set(self.asset_name)
		primitive_lop.parm("primkind").set("component")

		#graft stages
		graftstages_lop = primitive_lop.createOutputNode("graftstages")
		graftstages_lop.setNextInput(sopcreate_lop)
		graftstages_lop.parm("primkind").set("subcomponent")

		#material lop
		materiallib_lop = graftstages_lop.createOutputNode("materiallibrary")
		self.createMaterials(materiallib_lop)

		#Export USD
		print("Exporting usd...")
		usd_rop_export = materiallib_lop.createOutputNode("usd_rop")
		usd_rop_export.parm("lopoutput").set(dir_path + "/usd_export/" + self.asset_name + ".usd")
		usd_rop_export.parm("execute").pressButton()