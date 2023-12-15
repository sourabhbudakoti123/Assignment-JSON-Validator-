import json
from typing import Dict, Union
from enum import Enum

class Days(Enum):
    SU = 1
    MO = 2
    TU = 3
    WE = 4
    TH = 5
    FR = 6
    SA = 7

d = [('extraday',str(member.name)) for member in Days]
check = [str(member.name) for member in Days]

class JsonValidator:
    def __init__(self, schema_file: str):
        self.schema_file = schema_file
        self.errors = []

    def validate_schema(self, json_file: str) -> bool:
        """
        Validate a JSON against a given schema.
        :param json_file: Path to the JSON file is validated.
        :type json_file: str
        :return: True if validation is coorect, False otherwise.
        :rtype: bool
        """
        schema_data = self._load_json(self.schema_file)

        json_data = self._load_json(json_file)
        json_data=json_data['Employees']
        ct=5

        if not self._validate_required_fields(json_data, schema_data):
            ct-=1

        if not self._validate_at_least_one_of(json_data, schema_data):
            ct-=1

        if not self._validate_either_one_or_another(json_data, schema_data):
            ct-=1

        if not self._validate_mutually_exclusive_fields(json_data, schema_data):
            ct-=1

        if not self._validate_field_values(json_data, schema_data):
            ct-=1

        if ct==5 :
            return True
        else :
            return False

    def _load_json(self, file_path: str) -> Union[Dict, None]:
        """
        Load JSON data from a file.
        :param file_path: Path to the JSON file.
        :type file_path: str
        :return: Loaded JSON data or None if loading fails.
        :rtype: dict or None(dict is dictionary)
        """
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            self.errors.append(f"Error in opening {file_path}: {str(e)}")
            return None

    def _validate_required_fields(self, json_data: Dict, schema_data: Dict) -> bool:
        """
        Validate if required fields are present in the JSON.
        :param json_data: The JSON data to be validated.
        :type json_data: dict
        :param schema_data: The JSON schema data.
        :type schema_data: dict
        :return: True if required fields are present, False otherwise.
        :rtype: bool
        """
        required_fields = schema_data.get("required", [])
        for field in required_fields:
            if field not in json_data[0]:
                # print(field)
                self.errors.append(f"Required field '{field}' is not present.")
                return False
        return True

    def _validate_at_least_one_of(self, json_data: Dict, schema_data: Dict) -> bool:
        """
        Validate if at least one of many fields is present in the JSON.
        :param json_data: The JSON data to be validated.
        :type json_data: dict
        :param schema_data: The JSON schema data.
        :type schema_data: dict
        :return: True if at least one of the fields is present, False otherwise.
        :rtype: bool
        """
        at_least_one_of = schema_data.get("atLeastOneOf", [])
        x = [field for field in at_least_one_of if field in json_data[0]]
        if not x:
            self.errors.append("At least one of the MobilePhone, WorkPhone, HomePhone should be present.")
            return False
        return True

    def _validate_either_one_or_another(self, json_data: Dict, schema_data: Dict) -> bool:
        """
        Validate if either one field or another field is present, but not both.
        :param json_data: The JSON data to be validated.
        :type json_data: dict
        :param schema_data: The JSON schema data.
        :type schema_data: dict
        :return: True if the validation condition is met, False otherwise.
        :rtype: bool
        """
        either = schema_data.get("either", {})
        field1 = either[0]
        field2 = either[1]
        # print(field1)
        # print(field2)

        
        if field1 in json_data[0] and field2 in json_data[0]:
            self.errors.append(f"Both '{field1}' and '{field2}' cannot be present simultaneously.")
            return False
        return True

    def _validate_mutually_exclusive_fields(self, json_data: Dict, schema_data: Dict) -> bool:
        """
        Validate if mutually exclusive fields are not present together in the JSON.
        :param json_data: The JSON data to be validated.
        :type json_data: dict
        :param schema_data: The JSON schema data.
        :type schema_data: dict
        :return: True if mutually exclusive fields are valid, False otherwise.
        :rtype: bool
        """
        mutually_exclusive_fields = schema_data.get("mutuallyExclusive", [])
        x = [field for field in mutually_exclusive_fields if field in json_data[0]]
        
        if len(x) > 1:
            self.errors.append(f"'{', '.join(x)}' cannot be present together.")
            return False
        return True

    def _validate_field_values(self, json_data: Dict, schema_data: Dict) -> bool:
        """
        Validate if field values are one of a set of predefined values.
        :param json_data: The JSON data to be validated.
        :type json_data: dict
        :param schema_data: The JSON schema data.
        :type schema_data: dict
        :return: True if field values are valid, False otherwise.
        :rtype: bool
        """
        field_values = d
        for field, valid_values in field_values:
            # print(field," ",valid_values)
            # print(json_data[0][field])
            if field in json_data[0] and json_data[0][field] not in check:
                self.errors.append(f"Invalid value '{json_data[0][field]}' for field '{field}'.")
                return False
        return True

validator = JsonValidator('schema.json')
json_file = 'sample.json'
validation_result = validator.validate_schema(json_file)
print("Final Validation:", validation_result)
if validator.errors:
    print("List of Errors:")
    for error in validator.errors:
        print(error)
