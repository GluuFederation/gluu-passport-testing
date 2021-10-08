import os
import datetime
from collections import OrderedDict
import json

# Currently we implement only three data types: string, boolean, integer, datetime
syntaxType = {
                '1.3.6.1.4.1.1466.115.121.1.7': 'boolean',
                '1.3.6.1.4.1.1466.115.121.1.27': 'integer',
                '1.3.6.1.4.1.1466.115.121.1.24': 'datetime',
              }
# other syntaxes are treated as string

# This function was used to gather data types from opendj schema files
# collected types were dumped to opendj_types.json


class AttribDataTypes:

    listAttributes = ['member']
    attribTypes = {}

    def __init__(self):
        self.test_dir = os.environ.get('TEST_DIR')
        self.ldifs_dir = '{}/data/ldifs'.format(self.test_dir)
        opendjTypesFn = '{}/opendj_types.json'.format(self.ldifs_dir)
        self.attribTypes = self.readJsonFile(opendjTypesFn)

        for v in syntaxType.values():
            if not v in self.attribTypes:
                self.attribTypes[v] = []

        if 'json' not in self.attribTypes:
            self.attribTypes['json'] = []

        self.processGluuSchema()

    def readJsonFile(self, jsonFile, ordered=False):
        print('reading json file', jsonFile)
        object_pairs_hook = OrderedDict if ordered else None
        if os.path.exists(jsonFile):
            with open(jsonFile) as f:
                return json.load(f, object_pairs_hook=object_pairs_hook)

    def processGluuSchema(self):
        gluuSchemaFn = '{}/gluu_schema.json'.format(self.ldifs_dir)
        gluuSchema = self.readJsonFile(gluuSchemaFn)
        gluuAtrribs = gluuSchema['attributeTypes']

        for attrib in gluuAtrribs:
            if attrib.get('json'):
                atype = 'json'
            elif  attrib['syntax'] in syntaxType:
                atype = syntaxType[attrib['syntax']]
            else:
                atype = 'string'
                
            for name in attrib['names']:
                self.attribTypes[atype].append(name)

        for obj_type in ['objectClasses', 'attributeTypes']:
            for obj in gluuSchema[obj_type]:
                if obj.get('multivalued'):
                    for name in obj['names']:
                        if not name in self.listAttributes:
                            self.listAttributes.append(name)

    def getAttribDataType(self, attrib):
        for atype in self.attribTypes:
            if attrib in self.attribTypes[atype]:
                return atype

        return 'string'

    def getTypedValue(self, dtype, val):
        retVal = val
        
        if dtype == 'json':
            try:
                retVal = json.loads(val)
            except Exception as e:
                pass

        if dtype == 'integer':
            try:
                retVal = int(retVal)
            except:
                pass
        elif dtype == 'datetime':
            if not isinstance(val, datetime.datetime):

                if '.' in val:
                    date_format = '%Y%m%d%H%M%S.%fZ'
                else:
                    date_format = '%Y%m%d%H%M%SZ'

                if not val.lower().endswith('z'):
                    val += 'Z'
                
                val = datetime.datetime.strptime(val, date_format)

            retVal = val.strftime('%Y-%m-%dT%H:%M:%S.%f')

        elif dtype == 'boolean':
            if not isinstance(retVal, bool):
                if retVal.lower() in ('true', 'yes', '1', 'on'):
                    retVal = True
                else:
                    retVal = False

        return retVal

attribDataTypes = AttribDataTypes()
