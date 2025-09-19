import json
import os
from pprint import pprint

from converters import CSVConverter, XMLConverter


def create_test_files():
	# Create CSV file
	with open("test.csv", "w", encoding="utf-8") as f:
		f.write("name,age,class\nMark,15,11\nAlex,10,4\n")
	
	# Create JSON file
	json_data = [
		{"name": "Book1", "price": "150", "pages": "80"},
		{"name": "Book2", "price": "500", "pages": "200"}
	]
	with open("test.json", "w", encoding="utf-8") as f:
		json.dump(json_data, f, ensure_ascii=False, indent=2)
	
	# Create XML file
	with open("test.xml", "w", encoding="utf-8") as f:
		f.write("""<?xml version="1.0" encoding="UTF-8"?>
		<products>
		    <product>
		        <name>Device_1</name>
		        <price>400</price>
		        <quantity>3</quantity>
		    </product>
		    <product>
		        <name>Device_2</name>
		        <price>200</price>
		        <quantity>60</quantity>
		    </product>
		</products>
		""")


def cleanup():
	"""Clean test files"""
	for file in ["test.csv", "test.json", "test.xml", "out.csv", "out.xml"]:
		if os.path.exists(file):
			os.remove(file)


create_test_files()

print("\nConverter CSV → JSON")
csv_json = CSVConverter.csv_to_json("test.csv")
pprint(csv_json)

print("\nConverter JSON → CSV")
CSVConverter.json_to_csv(csv_json, "out.csv")
print("CSV saved to 'out.csv' file")

print("\nConverter XML → JSON")
xml_json = XMLConverter.xml_to_json("test.xml")
pprint(xml_json)

print("\nConverter JSON → XML")
XMLConverter.json_to_xml("test.json", "out.xml")
print("XML saved в out.xml")

# cleanup()
