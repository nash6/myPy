#test.py
#

from PyLuaTblParser import PyLuaTblParser 


if __name__ == '__main__':
	print 'Test begin'

	file_path = r'C:\Users\S6\Desktop\output.txt'

	testCase = []


	testCase.append('{array = {65,23,5,},dict = {mixed = {43,54.33,false,9,string = "value",},array = {3,6,4,},string = "value",},}')


	testCase.append(r'''{["'\\"] = 1}''')
	

	testCase.append('{1,2,3}')
	testCase.append('{--[=[}]=]1--[=[}]=],--[=[}]=]2--[=[}]=],--[=[}]=]3--[=[}]=]}')
	testCase.append('{{--[=\n1}}')
	#testCase.append('{{[=[abc]=]}}')
	#testCase.append('{1, {--[=[}]=]2}}')
	
	testCase.append('{["_sawda\\\""] = 123}')
	testCase.append('{1,2,3,nil,{--\n}\n}')

	#testCase.append('{1,2,3,nil,--[=[\n]=]{--}\n}}')

	testCase.append("{1,2,''}")
	testCase.append(r"{'abc\\',2}")


	testCase.append(r"{1,2,{'abc\\'}}")

	testCase.append("{['abc\"'] = 4}")

	testCase.append("{_ba3= 3}")

	testCase.append("{123;456}")

	testCase.append("{[1]=nil}")

	testCase.append("{[00.00]=1, [1] = 2}")

	

	testCase.append("{[11]='abc', [-0x2]=-0xa, [-11] = 5, [--awd\n-0x2--daw\n] = 6}")

	testCase.append('{[==[\nalo\n123"]==]}')

	testCase.append("{'alo\010123\"'}")

	testCase.append("{1,2,3,--[===\n 123}")

	#testCase.append(r"{'\\\97lo\10\04923"', [==[\97lo\10\04923"]==], 'ug\97\000123'}")

	testCase.append('{[11] = 11, nil, 3,[-11.] = "abc", [-11] = "v", [-0xb] = nil}')

	testCase.append('{[-99] = -2 ,[-99] = 0xa,3}')

	testCase.append('{1,2,3,nil,5,[99] = 1,[99] = nil}')

	testCase.append('{-.1e-2, .1e-2, -0x2,--[[1]]1.e-1, 1.e+1}')

	

	testCase.append('{[--awd\n-2.e-1--daw\n] = 6,[--[=[d\n2123]=]-.2e-1--[[daw\n]]]=7}')

	testCase.append('{[1]=1,[2]=2,[3]=3}')

	testCase.append('{"\\\n\\\t"}')

	
	#testCase.append('''{"\\\"\\a"}''')
	#testCase.append('''{"abc\\n",'abc\n','\\\"','\\0123','string"','\\\\','string\"',[[\n\r\'\""']],'\\x59'}''')
	#testCase.append('''{1,2,{"\'", {},[[}]], --[==[\n]==]} --\n}''')
	#testCase.append('''{1.2, .3, 0x1,1.e-1--\n, }''')
	#testCase.append('''{--{}\n{"abc\\n", '"a"', _abv = 1 }}''')
	#testCase.append('''{1,{},2}''')
	#testCase.append('''{1,"string",[4]="string",nil,[5]=nil,true,false}''')
	#testCase.append('''{'\\\''}''')
	#testCase.append('{\'\\\\"\\x08\\x0c\\n\\r\\t`1~!@#$%^&*()_+-=[]{}|;:\\\\\',./<>?\'}')
	#testCase.append('''{["\\\\\"\\x08\\x0c\\n\\r\\t`1~!@#$%^&*()_+-=[]{}|;:',./<>?"] = 1, }''')
	#testCase.append("{\"\\\"\",\"\\n\"}")


	testCase.append(r'''{'\\"\x08\x0c\n\r\t`1~!@#$%^&*()_+-=[]{}|;:\',./<>?'}''')

	for index, each in enumerate(testCase):
		print index, ': len' ,len(each)
		print each
		
		a1 = PyLuaTblParser()
		a2 = PyLuaTblParser()
		a3 = PyLuaTblParser()
		#a4 = PyLuaTblParser()


		a1.load(each)

		d1 = a1.dumpDict()
		#a = r'\\"\x08\x0c\n\r\t`1~!@#$%^&*()_+-=[]{}|;:\',./<>?'
		#d1 = [a]
		a2.loadDict(d1)		
		a2.dumpLuaTable(file_path)
		a3.loadLuaTable(file_path)
		d3 = a3.dump()
		print d3
