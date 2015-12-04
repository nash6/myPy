#test.py

from PyLuaTblParser import PyLuaTblParser 





if __name__ == '__main__':
	print 'Test begin'

	file_path = r'C:\Users\S6\Desktop\output.txt'

	testCase = []



	#inside {}


	testCase.append('{1,2,3}')
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

	testCase.append("{[1]=nil}")

	testCase.append("{[00.00]=1, [1] = 2}")

	

	testCase.append("{[11]='abc', [-0x2]=-0xa, [-11] = 5, [--awd\n-0x2--daw\n] = 6}")

	testCase.append('{[==[\nalo\n123"]==]}')

	testCase.append("{'alo\010123\"'}")

	testCase.append("{1,2,3,--[===\n 123}")

	testCase.append(r'''{'\\\97lo\10\04923"', [==[\97lo\10\04923"]==], 'ug\97\000123'}''')

	testCase.append('{[11] = 11, nil, 3,[-11.] = "abc", [-11] = "v", [-0xb] = nil}')

	testCase.append('{[-99] = -2 ,[-99] = 0xa,3}')

	testCase.append('{1,2,3,nil,5,[99] = 1,[99] = nil}')

	testCase.append('{-.1e-2, .1e-2, -0x2,--[[1]]1.e-1, 1.e+1}')

	testCase.append(r'''{["'\\"] = 1}''')

	testCase.append('{[--awd\n-2.e-1--daw\n] = 6,[--[=[d\n2123]=]-.2e-1--[[daw\n]]]=7}')

	testCase.append('{[1]=1,[2]=2,[3]=3}')

	testCase.append('{"\\\n\\\t"}')
	#testCase.append('--sdwa\n{_sdaw" = 1}--[=[\n]=]')

	#testCase.append('{[[1\n1]],"1\n1"}')

	'''
	
	fp = open(r'C:\Users\S6\Desktop\new1.txt')
	tmp = ''
	for line in fp:
		tmp += line
	fp.close()


	fv = open(r'C:\Users\S6\Desktop\reader.txt','w')
	
	for index,char in enumerate(tmp):
		fv.write( '%d: %s\n'%(index,char) )

	fcom = open(r'C:\Users\S6\Desktop\com.txt','w')
	
	t = PyLuaTblParser()
	t2 = PyLuaTblParser()
	t3 = PyLuaTblParser()
	t.load(tmp)
	d1 = t.dumpDict()
	t2.loadDict(d1)		
	t2.dumpLuaTable(file_path)
	t3.loadLuaTable(file_path)
	d3 = t3.dump()
	print >> fcom ,d3

	if d3 == d1:
		print 'yes'
	'''

	for index, each in enumerate(testCase):
		print index, ': len' ,len(each)
		print each
		
		a1 = PyLuaTblParser()
		a2 = PyLuaTblParser()
		a3 = PyLuaTblParser()
		
		a1.load(each)
		d1 = a1.dumpDict()

		a2.loadDict(d1)		
		a2.dumpLuaTable(file_path)
		a3.loadLuaTable(file_path)
		d3 = a3.dump()
		print `d3`
	
	

