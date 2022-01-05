#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# required libraries
import requests
import csv
import json
import os
import pandas as pd

def createFolders():
	if not os.path.isdir('municiple_data'):
		os.mkdir('municiple_data')
	if not os.path.isdir('province_data'):
		os.mkdir('province_data')

def municipleData():
	#count iterates through each subset of modified data
	count = 0

	#url_index iteraates through the list of json webpages
	url_index = 1

	url1 = "https://nmclist.nicd.ac.za/App_JSON/DashProvincialCumulativeTests_"
	url2 = ".json?v=2025"

	for url_index in range(1,10):
		try:
			#iterates through json webpages
			count = 0
			url = url1 + str(url_index) + url2
			response = requests.get(url)
			data_json = json.loads(response.text)
			date_of_collection = data_json["start"]
			modifed_data = data_json["series"]
			url_index+=1
		except:
			print("ERROR")
			
		max_pages = len(modified_data) + 1
		for count in range(0,max_pages):
			try:
				#parsed info starting from count
				sub_modified_data = modifed_data[count]["data"]

				#parses name info from count
				municiple_name = modifed_data[count]["name"]

				municiple_csv = pd.DataFrame(sub_modified_data, columns = ['ID', 'Cases'])
				municiple_csv.to_csv(f'data/municiple_data/{municiple_name}.csv')

				count+=1

			except:
				print("ERROR with municiple")

def provinceData():
	count = 0
	url = "https://nmclist.nicd.ac.za/App_JSON/DashProvinceCumulativeCases.json?v=2025"

	#retrieves info from json request
	response = requests.get(url)
	data_json = json.loads(response.text)
	date_of_collection = data_json["start"]
	modifed_data = data_json["series"]
	
	max_pages = len(modified_data) + 1
	for count in range(0,max_pages):
			try:
				#parsed info starting from count
				sub_modified_data = modifed_data[count]["data"]

				#parses name info from count
				province_name = modifed_data[count]["name"]

				province_csv = pd.DataFrame(sub_modified_data, columns = ['ID', 'Cases'])
				province_csv.to_csv(f'data/province_data/{province_name}.csv')

				count+=1

			except:
				print(count)
				print("ERROR with province")
				break
	print("Success")


def main():
	#createFolders() only nessecary if running code on own computer
	municipleData()
	provinceData()

if __name__ == "__main__":
    main()

