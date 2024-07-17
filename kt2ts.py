import re
import os
import openpyxl
import sys

filename = '/Users/yk/Downloads/DeliverySignScanBillCode.kt'


def transformType(ot):
	newType = 'Object'
	for item in ['Int', 'Double', 'Long', 'Number', 'Boolean'] :
		if item in ot:
			newType = 'number'
	
	if 'String' in ot:
		newType = 'string'
	# if 'Bool' in ot:
	# 	newType = 'boolean'
	
	if '[' in ot or 'Array' in ot:
		newType = '%s[]' % (newType)

	if '[String:' in ot:
		newType = 'Map<string, Object>'
	return newType

def createMethod(dic):
	paramsStr = ''
	setStr = ''

	for key, value in dic.items():
		setLine = "		this.%s = %s" %(key, key)
		setStr = setStr + setLine + '\n'

		paramsLine = "%s?: %s" %(key.strip(), value.strip())
		paramsStr = paramsStr + paramsLine + ', '

	endIdx = len(paramsStr) - 2
	createStr = "	constructor(%s) {\n %s\n	}" %(paramsStr[:endIdx], setStr)
	print(createStr)

def initString(dic):
	initStr = ''
	for key, value in dic.items():
		initline = "bean.%s" %(key)
		initStr = initStr + initline + ', '
	print(initStr)

def transformModel():
	kv = {}

	with open(filename, 'r') as file:
	    # 逐行读取文件内容
	    for line in file:
	        row = line.strip()
	        
	        if row.startswith('struct') :
	        	name = re.findall(r'struct ([^"]*?): ', row)[0]
	        	showLine = "export class %s {" %(name)
	        	print(showLine)
	        	continue

	        if row.startswith('class'):
	        	name = re.findall(r'class ([^"]*?): ', row)[0]
	        	showLine = "export class %s {" %(name)
	        	print(showLine)
	        	continue

	        if row.startswith('data class'):
	        	name = re.findall(r'class ([^"]*?)\(', row)[0]
	        	showLine = "export class %s {" %(name)
	        	print(showLine)
	        	continue

	        if row.startswith('//'):
	        	print(row)
	        	continue

	        # name = ''
	        if row.startswith('var '): 
	        	# print(row)
	        	name = re.findall(r'var ([^"]*?): ', row)[0]
	        	# typeStr = re.findall(r': ([^"]*?) =', row)[0]
	        	showType = transformType(row)

	        	kv[name] = showType

	        	showLine = "	%s?: %s;" %(name, showType)

	        	index = row.find('//')
	        	if index != -1:
	        		showLine += row[index:]

	        	dbType = showType[:3]
	        	if 'Long' in row:
	        		dbType = 'real'

	        	decorative = "	@Columns({ columnName: '%s', types: ColumnType.%s })" %(name, dbType)
	        	print(decorative)
	        	print(showLine + '\n')

	        if row.startswith('}'):
	        	createMethod(kv)
	        	print(row)
	        	break

	        if row.startswith(')'):
	        	createMethod(kv)
	        	print(row.replace(')', '}', 1))
	        	break
	
	initString(kv)
	

transformModel()





