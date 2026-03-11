import json
import os
import jsonschema
from jsonschema import validate

RULEBOOK_PATH = './rules/compiled/compiled_rulebook.json'
SCHEMA_PATH = './rules/schema/rulebook.schema.json'

def validate_rules():
    with open(SCHEMA_PATH, 'r') as schema_file:
        schema = json.load(schema_file)

    with open(RULEBOOK_PATH, 'r') as rulebook_file:
        rulebook = json.load(rulebook_file)

    try:
        validate(instance=rulebook, schema=schema)
        print("Rulebook is valid!")
    except jsonschema.exceptions.ValidationError as err:
        print(f"Rulebook is invalid: {err.message}")

if __name__ == '__main__':
    validate_rules()