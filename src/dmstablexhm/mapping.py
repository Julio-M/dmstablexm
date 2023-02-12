#!/usr/bin/env python3

# Import modulesm for json, os and readline
import json

# Import modules for uuid and random to use for unique id's
import uuid
import random

class Color:
    # Expect text to be string
    def __init__(self, text):
        self.text = text
        self.BOLD = '\033[1m'
        self.END = '\033[0m'
        self.YELLOW = '\033[93m'

    # Return the text in bold
    def bold(self):
        return f"{self.BOLD}{self.text}{self.END}"

    def yellow(self):
        return f"{self.YELLOW}{self.text}{self.END}"

# Make uuid json serializable
class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)

unique_id = uuid.uuid4() 
random_ids = []
# Initialize empty dictionary `data` and set `rules` key to an empty list
data = {}
data['rules'] = []

# Define class for mapping
class Mapping:

    # class statick variable
    mapping_type = "DMS Mapping"

    # Constructor
    def __init__(self,table_list_input,schema_list_input,rule_action,table_types, prefix_value=None):
        
        # rule_action should only be allowed to be one of the following values ["include","exclude","explicit"]
        # table_types should only be allowed to be one of the following values ["table","view","al"]

        # Validate the values of the parameters

        if rule_action not in ["include","exclude","explicit"]:
            raise ValueError("The rule action must be one of the following values: include, exclude or explicit")
        
        if table_types not in ["table","view","all"]:
            raise ValueError("The table type must be one of the following values: table, view or all")

        self.table_list_input = table_list_input
        self.schema_list_input = schema_list_input
        self.prefix_value = prefix_value
        self.rule_action = rule_action
        self.table_types = table_types


    # Function that will print all the values in a table format
    def printTable(self):
        print(Color("Values used: \n").bold())

        if self.prefix_value == None:
            self.prefix_value = "None"
        
        header = ["Table List Input","Schema List Input","Prefix Value","Rule Action","Table Types"]
        header = ' '.join(word.ljust(20) for word in header)

        # Seperate the header from the rest of the data
        print(header)
        print('-' * len(header))

        # Print the data
        print(self.table_list_input.ljust(20),self.schema_list_input.ljust(20),self.prefix_value.ljust(20),self.rule_action.ljust(20),self.table_types.ljust(20))
        print(' ' * len(header))


    # Function that reads table list file
    def readTableList(self):
        file = open(self.table_list_input, "r")
        file_lines = file.read()
        list_of_lines = file_lines.split("\n")
        list_of_lines_after_quotes = [w.strip('\"') for w in list_of_lines]
        return list_of_lines_after_quotes if '"' in list_of_lines[0] else list_of_lines

    # General rules template
    def general_rules(self,i,random_id):
        return {
                "rule-type":"selection",
                "rule-id":f"{random_id}",
                "rule-name":unique_id,
                "object-locator":{
                    "schema-name":self.schema_list_input,
                    "table-name":self.readTableList()[i] if "add-prefix" not in self.readTableList()[i] else  self.readTableList()[i].replace(' add-prefix',"")
                },
                "rule-action":self.rule_action,
                "filters":[]
            }

    # Prefix rules template
    def prefix_rules(self,i,random_id):
            return {
                "rule-type":"transformation",
                "rule-id":f"{random_id}",
                "rule-name":unique_id,
                "rule-target":"table",
                "object-locator":{
                    "schema-name":self.schema_list_input,
                    "table-name":self.readTableList()[i] if "add-prefix" not in self.readTableList()[i] else  self.readTableList()[i].replace(' add-prefix',"")
                },
                "rule-action":"add-prefix",
                "value":self.prefix_value
            }
    
    # Loop through the list of table names, create dictionary, and add it to the list
    def createJSON(self):
        printTable = self.printTable()
        # Ask user if they want to continue
        for i in range(0,len(self.readTableList())):
            random_id = random.randint(0,1000)
            if random_id in random_ids: random_id = random.randint(0,1000)
            if self.prefix_value != None and self.prefix_value != "None":
                data['rules'].append(self.prefix_rules(i,random_id))
                data['rules'].append(self.general_rules(i,random_id))
                print(Color("Prefix rule added-> ").bold() + Color(self.prefix_value).yellow() + " in front of -> " + Color(self.readTableList()[i]).bold())
            else:
                data['rules'].append(self.general_rules(i,random_id))
            random_ids.append(random_id)

        with open('table_mapping.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=True, indent=2, cls=UUIDEncoder)
        print('\n')
        print("Check your table_mapping.json file.")
