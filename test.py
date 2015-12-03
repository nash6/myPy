#test.py

from PyLuaTblParser import PyLuaTblParser 





if __name__ == '__main__':
	print 'Test begin'

	file_path = r'C:\Users\S6\Desktop\output.txt'

	testCase = []



	#inside {}
	testCase.append('{{--[=\n1}}')
	testCase.append('{{[=[abc]=]}}')
	testCase.append('{1, {--[=[}]=]2}}')


	testCase.append('{array = {65,23,5,},dict = {mixed = {43,54.33,false,9,string = "value",},array = {3,6,4,},string = "value",},}')
	testCase.append('{["_sawda\\\""] = 123}')
	testCase.append('{1,2,3,nil,{--}\n}}')

	testCase.append('{1,2,3,nil,--[=[\n]=]{--}\n}}')

	testCase.append("{1,2,''}")
	testCase.append(r"{'abc\\',2}")


	testCase.append(r"{1,2,{'abc\\'}}")

	testCase.append("{['abc\"'] = 4}")

	testCase.append("{_ba3= 3}")

	testCase.append("{123;456}")

	testCase.append("{[1]=abc}")

	testCase.append("{[00.00]=1, [1] = 2}")

	testCase.append("{[0x1e1]=1}")

	testCase.append("{[11]='abc', [-0x2]=-0xa, [-11] = 5}")

	testCase.append('{[==[\nalo\n123"]==]}')

	testCase.append("{'alo\010123\"'}")

	testCase.append("{1,2,3,--[===\n 123}")

	testCase.append(r'''{'\\\97lo\10\04923"', [==[\97lo\10\04923"]==], 'ug\97\000123'}''')

	testCase.append('{[11] = 11, nil, 3,[-11.] = "abc", [-11] = "v", [-0xb] = nil}')

	for index, each in enumerate(testCase):
		print index, ': len' ,len(each)
		print each
		
		a1 = PyLuaTblParser()
		a2 = PyLuaTblParser()
		a3 = PyLuaTblParser()
		
		a1.load(each)
		print a1.pyDict
		print a1.pyList
		d1 = a1.dumpDict()
		print d1
		
		a2.loadDict(d1)		
		a2.dumpLuaTable(file_path)
		a3.loadLuaTable(file_path)
		d3 = a3.dump()
		print d3

		


