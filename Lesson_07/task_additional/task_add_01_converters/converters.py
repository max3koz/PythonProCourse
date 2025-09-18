import csv
import json
import xml.etree.ElementTree as ET
from typing import List, Dict


class CSVConverter:
	"""
	Class for converting between CSV file and JSON.
	"""
	
	@staticmethod
	def csv_to_json(csv_path: str) -> List[Dict[str, str]]:
		"""Converting a CSV file to JSON."""
		with open(csv_path, mode='r', encoding='utf-8') as file:
			reader = csv.DictReader(file)
			return [row for row in reader]
	
	@staticmethod
	def json_to_csv(json_data: List[Dict[str, str]], csv_path: str) -> None:
		"""Converting a JSON to CSV file."""
		if not json_data:
			return
		with open(csv_path, mode='w', encoding='utf-8', newline='') as file:
			writer = csv.DictWriter(file, fieldnames=json_data[0].keys())
			writer.writeheader()
			writer.writerows(json_data)


class XMLConverter:
	"""
	Class for converting between XML file and JSON file.
	Expects the structure:
	<products><product><name>...</name>...</product></products>
	"""
	
	@staticmethod
	def xml_to_json(xml_path: str) -> List[Dict[str, str]]:
		"""Converting a XML file to JSON."""
		tree = ET.parse(xml_path)
		root = tree.getroot()
		result: List[Dict[str, str]] = []
		
		for element in root:
			item: Dict[str, str] = {}
			for child in element:
				item[child.tag] = child.text if child.text is not None else ""
			result.append(item)
		
		return result
	
	@staticmethod
	def json_to_xml(json_path: str, xml_path: str) -> None:
		"""Converting a JSON to XML file."""
		with open(json_path, 'r', encoding='utf-8') as f:
			data = json.load(f)
		
		root = ET.Element("root")
		
		for item in data:
			product = ET.SubElement(root, "item")
			for key, value in item.items():
				child = ET.SubElement(product, key)
				child.text = str(value)
		
		tree = ET.ElementTree(root)
		tree.write(xml_path, encoding='utf-8', xml_declaration=True)
