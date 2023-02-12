# DMS- Table mapping generator

This is a simple tool to generate table mapping for DMS.

## Pre-requisites

* Python >= 3.6
* A file that contains the tables

e.g. `tables.txt`

```
table1
table2
table3
```

## Installation

```
pip install dmstablexhm
```


## Usage example

You can use the tool as a python module, once ran it will generate a JSON file with the table mapping in the current directory.


```
from dmstablexm import Mapping

p1 = Mapping("tables.txt","public","include","view","myprefix_")

p1.createJSON()
```

Output example:
```
{
  "rules": [
    {
      "rule-type": "transformation",
      "rule-id": "51",
      "rule-name": "c39ffde6c44141da8cf4eb46cc2dff94",
      "rule-target": "table",
      "object-locator": {
        "schema-name": "public",
        "table-name": "table1"
      },
      "rule-action": "add-prefix",
      "value": "myprefix_"
    },
    {
      "rule-type": "selection",
      "rule-id": "51",
      "rule-name": "c39ffde6c44141da8cf4eb46cc2dff94",
      "object-locator": {
        "schema-name": "public",
        "table-name": "table1"
      },
      "rule-action": "include",
      "filters": []
    },
    {
      "rule-type": "transformation",
      "rule-id": "921",
      "rule-name": "c39ffde6c44141da8cf4eb46cc2dff94",
      "rule-target": "table",
      "object-locator": {
        "schema-name": "public",
        "table-name": "table2"
      },
      "rule-action": "add-prefix",
      "value": "myprefix_"
    },
    {
      "rule-type": "selection",
      "rule-id": "921",
      "rule-name": "c39ffde6c44141da8cf4eb46cc2dff94",
      "object-locator": {
        "schema-name": "public",
        "table-name": "table2"
      },
      "rule-action": "include",
      "filters": []
    },
    {
      "rule-type": "transformation",
      "rule-id": "405",
      "rule-name": "c39ffde6c44141da8cf4eb46cc2dff94",
      "rule-target": "table",
      "object-locator": {
        "schema-name": "public",
        "table-name": "table3"
      },
      "rule-action": "add-prefix",
      "value": "myprefix_"
    },
    {
      "rule-type": "selection",
      "rule-id": "405",
      "rule-name": "c39ffde6c44141da8cf4eb46cc2dff94",
      "object-locator": {
        "schema-name": "public",
        "table-name": "table3"
      },
      "rule-action": "include",
      "filters": []
    }
  ]
}
```
