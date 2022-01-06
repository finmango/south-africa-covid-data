#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# required libraries
import requests
import csv
import json
import os
import pandas as pd

#added libraries
import datetime
import glob

def createFolders():
	if not os.path.isdir('municiple_data'):
		os.mkdir('municiple_data')
	if not os.path.isdir('province_data'):
		os.mkdir('province_data')

def municipleData():
	#count iterates through each subset of modified data
	count = 0

	#url_index iterates through the list of json webpages
	url_index = 1

	url1 = 'https://nmclist.nicd.ac.za/App_JSON/DashProvincialCumulativeTests_'
	url2 = '.json?v=2025'

	for url_index in range(1,10):
		#iterates through json webpages
		count = 0
		url = url1 + str(url_index) + url2

		#processes json response
		response = requests.get(url)
		data_json = json.loads(response.text)
		date_of_collection = data_json['start']
		modified_data = data_json['series']
		url_index+=1
			
		max_pages = len(modified_data)
		for count in range(0,max_pages):
			#parsed info starting from count
			sub_modified_data = modified_data[count]['data']

			#parses name info from count
			municiple_name = modified_data[count]['name']

			#finds the code for the province by using the province as a key in a dictionary
			with open('province_municiple_list.txt') as f:
				name_list = f.read()
				modified_list = json.loads(name_list)
			municiple_code = modified_list.get(municiple_name)
			municiple_csv = pd.DataFrame(sub_modified_data, columns = ['ID', 'Cases'])

			#inverts data so that it begins from most recent cumulative data instead of starting from case 1
			municiple_csv = municiple_csv.sort_values(by=['Cases'], ascending=False)

			#adds row to top with municiple code and name
			new_row = pd.DataFrame({'ID': [municiple_code], 'Cases': [municiple_name]})
			municiple_csv = pd.concat([new_row, municiple_csv]).reset_index(drop=True)

			municiple_csv.to_csv(f'data/municiple_data/{municiple_code}.csv', index=False)

			#print(municiple_name)

def provinceData():
	count = 0
	url = "https://nmclist.nicd.ac.za/App_JSON/DashProvinceCumulativeCases.json?v=2025"

	#retrieves info from json request
	response = requests.get(url)
	data_json = json.loads(response.text)
	date_of_collection = data_json['start']
	modified_data = data_json['series']

	#converts timestamp to iso format
	date_obj = datetime.datetime.strptime(date_of_collection, "%Y-%m-%d %H:%M:%S")
	iso_date = date_obj.isoformat()
	
	max_pages = len(modified_data)
	for count in range(0,max_pages):
		#parsed info starting from count
		sub_modified_data = modified_data[count]['data']

		#parses name info from count
		province_name = modified_data[count]['name']

		#finds the code for the province by using the province as a key in a dictionary
		with open('province_municiple_list.txt') as f:
			name_list = f.read()
			modified_list = json.loads(name_list)
		province_code = modified_list.get(province_name)
		province_csv = pd.DataFrame(sub_modified_data, columns = ['ID', 'Cases'])

		#inverts data so that it begins from most recent cumulative data instead of starting from case 1
		province_csv = province_csv.sort_values(by=['Cases'], ascending=False)

		#adds row to top with province code and name
		new_row = pd.DataFrame({'ID': [province_code], 'Cases': [province_name]})
		province_csv = pd.concat([new_row, province_csv]).reset_index(drop=True)

		province_csv.to_csv(f'data/province_data/{province_code}.csv', index=False)

		#print(province_name)

def joinFiles():
	joined_municiple_files = os.path.join('data/municiple_data', '*.csv')
	joined_municiple_list = glob.glob(joined_municiple_files)
	total_municiple_info = pd.concat(map(pd.read_csv, joined_municiple_list), ignore_index=True, axis=1) 
	total_municiple_info.to_csv('data/total_info/total_municiple_info.csv', index=False)

	joined_province_files = os.path.join('data/province_data', '*.csv')
	joined_province_list = glob.glob(joined_province_files)
	total_province_info = pd.concat(map(pd.read_csv, joined_province_list), ignore_index=True, axis=1)
	total_province_info.to_csv('data/total_info/total_province_info.csv', index=False)

def main():
	#createFolders() only nessecary if running code on own computer
	municipleData()
	provinceData()
	joinFiles()

if __name__ == '__main__':
    main()
