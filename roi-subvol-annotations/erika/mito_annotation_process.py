'''
neacee 2020-09-10
process mito annotations
'''

import json
import requests
import getpass
import pandas as pd
from datetime import date
from neuclease.dvid import *


def get_user(gmail):
	users = {
		"erika.neace@gmail.com" : "neacee",
		"brandoncanino808@gmail.com" : "caninob",
		"sammie42finley@gmail.com" : "finleys",
		"thomsonrymer@gmail.com" : "rymert",
		"aliansuleiman95@gmail.com" : "suleimana",
		"alanna.lohff@gmail.com" : "lohffa",
		"kelli.fairbanks@gmail.com" : "fairbanksk",
		"alfrancis1996@gmail.com" : "francisa",
		"alf5bc@virginia.edu" : "francisa",
		"natalielynnsmith@gmail.com" : "smithn",
		"mr.walsh.jr@gmail.com" : "walshj",
		"elliott.phillips9@gmail.com" : "phillipse2",
		"cookmichaeledward@gmail.com" : "cookm",
		"iris.talebi@gmail.com" : "talebii",
		"alvaradocx4@gmail.com" : "alvaradoc",
		"csmith792@gmail.com" : "smithc",
		"gary.patrick.hopkins@gmail.com" : "hopkinsg",
		"paterson1391@gmail.com" : "patersont",
		"sam.ballinger96@gmail.com" : "ballingers",
		"dennis.aa.bailey@gmail.com" : "baileyd2",
		"ribeirocaitlin@gmail.com" : "ribeiroc",
		"emanley8794@gmail.com" : "manleye",
		"sm.ryan1412@gmail.com" : "ryans",
		"nneoma.okeoma@gmail.com" : "okeoman",
		"emily.m.joyce1@gmail.com" : "joycee",
		"tansygarvey@gmail.com" : "yangt",
		"scott.ashleylauren@gmail.com" : "scotta",
		"als9ag@virginia.edu" : "scotta",
		"anniekayscott@gmail.com" : "scotta10",
		"phillips.m.emily@gmail.com" : "phillipse",
		"charli.tiscareno@gmail.com" : "tiscarenoc",
		"octave2014@gmail.com" : "ducloso",
		"tingzhao@gmail.com" : "zhoat",
		"tieka14@gmail.com" : "mooneyc",
		"na1218k@gmail.com" : "kirkn",
		"cjk7067@gmail.com" : "knechtc",
		"slauchie@gmail.com" : "lauchies",
		"omotaraogundeyi@gmail.com" : "ogundeyio",
		"quatretribunal@gmail.com" : "shinomiyaa",
		"satn2030@gmail.com" : "takemurasa",
		"cordish25@gmail.com" : "ordishc"
		}

	if gmail in users.keys():
		user = users[gmail]
		user_list.append(user)
	else:
		user = ""
	return(user)

def get_status(uuid, label):
	#-- get annotations and status for bodies in assignment --
	status_dict = {}
	status_url = "https://hemibrain-dvid2.janelia.org/api/node/"+str(uuid)+"/segmentation_annotations/key/"+str(label)
	print(status_url)
	#-- only bodies that have been annotated have keys in data instance --
	try:
		check_status_url = session.get(status_url)
		status_data = check_status_url.json()
		status = status_data["status"]
		# if "status" in status_data.keys():
		# 	status = status_data["status"]
		# else:
		# 	status = ""
		if "comment" in status_data.keys():
			comment = status_data["comment"]
		else:
			comment = ""
		if "class" in status_data.keys():
			body_name = status_data["class"]
		else:
			body_name = ""
		status_dict["status"] = status
		status_dict["comment"] = comment
		status_dict["class"] = body_name
	#-- sets fields to empty if no keyvalue in DVID --
	except:
		status_dict["status"] = ""
		status_dict["comment"] = ""
		status_dict["class"] = ""
	print(status_dict)
	return(status_dict)

def get_mito_info(mito_id):
	if mito_id != 0:
		mito_size_url ="http://emdata3.int.janelia.org:8900/api/node/d31b/masked-mito-cc/size/"+str(mito_id)
		get_size_data = session.get(mito_size_url)
		mito_size_json = get_size_data.json()
		mito_size = mito_size_json["voxels"]
		return(mito_size)
	else:
		return(0)


def get_bodyId(uuid, task):
	#--gets bodyID for this location in given uuid--
	print(uuid)
	print(task)
	# body_url = 'https://hemibrain-dvid2.janelia.org/api/node/'+str(uuid)+'/segmentation/label/'+task
	prod_body_url = "https://hemibrain-dvid2.janelia.org/api/node/"+str(uuid)+"/segmentation/label/"+task
	mito_body_url = 'http://emdata3.int.janelia.org:8900/api/node/d31b/masked-mito-cc/label/'+task
	print(prod_body_url)
	print(mito_body_url)
	check_prod_body_url = session.get(prod_body_url)
	prod_body_json = check_prod_body_url.json()
	prod_body_label = prod_body_json["Label"]
	prod_body_info = get_status(uuid, prod_body_label)
	prod_body_status = prod_body_info["status"]
	prod_body_type = prod_body_info["class"]
	check_mito_body_url = session.get(mito_body_url)
	mito_body_json = check_mito_body_url.json()
	mito_body_label = mito_body_json["Label"]
	

	mito_size = get_mito_info(mito_body_label)
	labels = [prod_body_label, mito_body_label, mito_size, prod_body_status, prod_body_type]
	return(labels)

def get_bookmarks(uuid):
	#-- get all bookmarks --
	bookmarks_url = "https://hemibrain-dvid2.janelia.org/api/node/"+uuid+"/neuroglancer_todo/all-elements"
	check_bookmarks = session.get(bookmarks_url)
	bookmarks = check_bookmarks.json()
	print(bookmarks)
	print(len(bookmarks))
	#-- write json for Tig loader --
	bookmarks_json = json.dumps(bookmarks, indent=2)
	with open(uuid+"_mito_annotation_data.json", "w") as outfile: 
	    outfile.write(bookmarks_json)

   #-- get bkm data --
	for bookmark in bookmarks:
		print(bookmark)
		task = bookmarks[bookmark]
		print(task)
		if len(task) >= 1:
			for e in task:
				print(e)
				bkm = e
				pos = bkm["Pos"]
				if pos[0] == 15642:
					print("------------------------------------------------------------------------------------")
				prop = bkm["Prop"]
				tags = bkm["Tags"]
				gmail = prop["user"]
				if "comment" in prop.keys():
					comment = prop["comment"]
				else:
					comment = ""
				if "type" in prop.keys():
					annot = prop["type"]
				else:
					annot = ""

				x = pos[0]
				y = pos[1]
				z = pos[2]
				loc = str(x)+"_"+str(y)+"_"+str(z)

				#-- get segmentation info for point --
				bodies = get_bodyId(uuid, loc)
				print(bodies)
				prod_body = bodies[0]
				mito_body = bodies[1]
				mito_size = bodies[2]
				prod_status = bodies[3]
				prod_type = bodies[4]
				
				user = get_user(gmail)

				bkm_out = {
					"user" : user,
					"gmail" : gmail,
					"type" : annot,
					"prod bodyID" : prod_body,
					"prod status" : prod_status,
					"prod cellType" : prod_type,
					"mito bodyID" : mito_body,
					"mito size" : mito_size,
					"location" : pos,
					"comment" : comment
				}

				data.append(bkm_out)




if __name__ == '__main__':
	today = date.today()

	session = requests.Session()
	session.params = { 
		'u': getpass.getuser(),
		'app': 'cloud mito bookmarks'
		}
	uuid = sys.argv[1]
	data = []
	user_list = []
	#-- grab data --
	get_bookmarks(uuid)

	cols = ["user", "gmail", "type", "prod bodyID", "prod status", "prod cellType", "mito bodyID", "mito size", "location", "comment"]
	df = pd.DataFrame(data)
	df = df[cols]
	df.to_csv(uuid+"_cloud_mito_info_bookmarks_"+str(today.strftime("%y-%m-%d"))+".csv")

