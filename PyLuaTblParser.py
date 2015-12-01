#PyLuaTblParser.py
#Written by lyc 2015.11.24
#For Netease codefly



class PyLuaTblParser(object):
	def __init__(self):
		self.pyDict = {}
		self.pyList = []

		

	def load(self, s):
		'''load Lua table'''

		self.pyDict = {}
		self.pyList = []
		if not isinstance(s, str):
			raise TypeError('Input is NOT string!')

		s = s.strip()
		if not (s[0] == '{' and s[-1] == '}'):
			raise TypeError('Input is NOT tableconstructor!')

		s = s[1:-1].strip()



		self.luaTblContent = s
		self.curr = 0
		self.stat = 0
		self.negative = False
		self.longCom = False
		self.decimal = False
		self.tmpKey = None
		self.tmpVal = None
		'''
		-2 wait for val when left is =
		-1 wait for key when left is [
		0 normal
		1 has a key
		2 has key and val
		3 has 'str' list next should be ,;
		4 exp name next should be =
		'''
		self._lex()

		

	def dump(self):
		result = ''
		if len(self.pyDict) == 0:
			result += '{'
			for each in self.pyList:
				if each == None:
					result += 'nil, '
				else:
					result += str(each)
					result += ', '
			result += '}'
		else:
			d = self.dumpDict()
			result = self._dict2lua(d)
		return result

	def loadLuaTable(self, f):
		fp = open(f, 'r')
		tmpstr = ''
		for item in fp:
			tmpstr += item
		fp.close()
		self.load(tmpstr)


	def dumpLuaTable(self, f):
		fp = open(f, 'w')
		fp.write(self.dump())
		fp.close()

	def loadDict(self, d):
		myd = self.deepCopyDict(d)
		for key in myd:
			if isinstance(key, str) or isinstance(key, int) or isinstance(key, float):
				self.pyDict[key] = myd[key]


	def dumpDict(self):
		if len(self.pyDict) == 0:
			return self.pyList[:]
		else:
			for index, each in enumerate(self.pyList):
				self.pyDict[index + 1] = each	
			return self.deepCopyDict(self.pyDict)

	#private fun
	def _lex(self):
		spaces = ('\t', ' ', '\n', '\r', '\f', '\v')
		nums = ('0', '1', '2', '3', '4', '5', '6','7','8','9')
		while True:
			if self.curr >= len(self.luaTblContent):
				self._store()
				break

			if self.luaTblContent[self.curr] in spaces:
				self._next()

			elif self.luaTblContent[self.curr] in ('\'','\"'):
				if self.stat == 0:
					self.tmpKey = self._getStr(self.luaTblContent[self.curr])
					self.stat = 3
				elif self.stat == -1:
					self.tmpKey = self._getStr(self.luaTblContent[self.curr])

					if self.curr >= len(self.luaTblContent):
						raise TypeError('stat -1 no ] %s', self.curr)
		
					while(self.luaTblContent[self.curr] != ']'):
						if self.luaTblContent[self.curr] not in spaces:
							raise TypeError('extra char  %s', self.curr)
						self._next()
						if self.curr >= len(self.luaTblContent):
							raise TypeError('stat -1 no ] %s', self.curr)
					self.stat = 1
					self._next()	
				elif self.stat == -2:
					self.tmpVal = self._getStr(self.luaTblContent[self.curr])
					self.stat = 2
				else:
					raise TypeError('Extra \' or " %s', self.curr)
					
			elif self.luaTblContent[self.curr] == '=':
				if self.stat == 1:
					self.stat = -2
					self._next()
				elif self.stat == 4:
					self.stat = -2
					self._next()
				else:
					raise TypeError('Extra = %s', self.curr)

			elif self.luaTblContent[self.curr] in (',', ';'):
				self._store()
				self._next()

			elif self.luaTblContent[self.curr] == '[':#[=[ or [key]
				if self._checkNext('=['):
					self._next()
					eqC = 0
					while self.luaTblContent[self.curr] == '=':
						eqC += 1
						if not self._next():
							raise TypeError('Extra [= or [[ %s', self.curr)

					if self.luaTblContent[self.curr] != '[':
						raise TypeError('Extra [=[ or [[ %s', self.curr)

					pat = ']' + '=' * eqC + ']'
					
					ret = self.luaTblContent.find(pat, self.curr + 1)
					if ret == -1:
						raise TypeError('No match %s %s'%(pat,self.curr))

					tmpstr = self.luaTblContent[self.curr + 1: ret]
				
					if tmpstr[0] == '\n':
						tmpstr = tmpstr[1:]
					self.curr = ret + len(pat) 
					
					if not self.longCom:
						if self.stat == 0:
							self.tmpKey = tmpstr
							self.stat = 3
						else:
							raise TypeError('Extra [[str]]'%(self.curr))
				else: 
					if self.stat == 0:
						self.stat = -1
						self._next()
					else:
						raise TypeError('Extra [ %s', self.curr)

			elif self.luaTblContent[self.curr] == '{':
				if self.stat not in (-2, 0):
					raise TypeError('Error { %s', self.curr)

				stack = []
				begin = self.curr

				if not self._next():
					raise TypeError('No match for { %s', self.curr)
				
				while True:
					if self.luaTblContent[self.curr] == '}' and len(stack) == 0:
						break

					if self.luaTblContent[self.curr] in ('\'', '\"') and self.luaTblContent[self.curr -1 ] != '\\':
						if len(stack) == 0:
							stack.append(self.luaTblContent[self.curr])
						elif stack[-1] == self.luaTblContent[self.curr]:
							stack.pop()
						elif stack[-1] in ('\'','\"'):
							pass
						else:
							stack.append(self.luaTblContent[self.curr])
					elif self.luaTblContent[self.curr] == '{':
						if len(stack) == 0:
							stack.append(self.luaTblContent[self.curr])
						elif stack[-1] in ('\'','\"'):
							pass
						else:
							stack.append(self.luaTblContent[self.curr])
					elif self.luaTblContent[self.curr] == '}':
						if len(stack) == 0:
							raise TypeError('U see god')
						elif stack[-1] in ('\'','\"'):
							pass
						elif stack[-1] == '{':
							stack.pop()
						else:
							raise TypeError('U see god')
					elif self.luaTblContent[self.curr] == '[':
						if len(stack) != 0 and stack[-1] in ('\'','\"'):
							pass
						else:
							if self._checkNext('=['):
								self._next()
								eqC = 0
								while self.luaTblContent[self.curr] == '=':
									eqC += 1
									if not self._next():
										raise TypeError('Extra [= or [[ %s', self.curr)

								if self.luaTblContent[self.curr] != '[':
									raise TypeError('Extra [=[ or [[ %s', self.curr)

								pat = ']' + '=' * eqC + ']'
								
								ret = self.luaTblContent.find(pat, self.curr + 1)
								if ret == -1:
									raise TypeError('No match %s %s'%(pat,self.curr))

								self.curr = ret + pat -1 

					if not self._next():
						raise TypeError('No match for { %s', self.curr)

				recur = PyLuaTblParser()
				recur.load(self.luaTblContent[begin:self.curr+1])

				if self.stat == 0:
					self.tmpKey = recur.dumpDict()
					self.stat = 3
				elif self.stat == -2:
					self.tmpVal = recur.dumpDict()
					self.stat = 2
				self._next()

			elif self.luaTblContent[self.curr] == '.': #num
				if self._checkNext(str(nums)):
					self.decimal = True
					self._next()
				else:
					raise TypeError('Extra . %s' % self.curr)
			elif self.luaTblContent[self.curr] == '-':
				if self._checkNext('-'):
					self._next()
					if self.curr + 1 == len(self.luaTblContent):
						continue
					if self._checkNext('['):
						self._next()
						if self._checkNext('=['):
							self.longCom = True
						else:
							self._comment()
					else:
						self._comment()
				else:
					if self._checkNext('.'+str(nums)):
						self.negative = True
						self._next()
					else:
						raise TypeError('Extra - %s' % self.curr)

			elif self.luaTblContent[self.curr] == '+':
				if self.stat not in (-2, -1):
					raise TypeError('Extra + %s' % self.curr)
				self._next()

			elif self.luaTblContent[self.curr] in nums:
				begin = self.curr
				if self.stat == -1:
					if self.tmpKey != None:
						raise TypeError('Already has key in [  when read nums %s' % self.curr)

					ret = self.alter(spaces +(']',))
					if ret == -1:
						raise TypeError('Extra Num %s' % self.curr)
					
					strNum = self.luaTblContent[begin:self.curr]
					
					realNum = self.str2Num(strNum, begin)

					self.tmpKey = realNum					
					self._findRhs()

				elif self.stat == -2 or self.stat == 0:
					if self.tmpVal != None:
						raise TypeError('Already has val in nums %s' % self.curr)

					ret = self.alter(spaces + (',',':'))
					if ret == -1:
						strNum = self.luaTblContent[begin:]
					else:
						strNum = self.luaTblContent[begin:self.curr]

					realNum = self.str2Num(strNum, begin)
					
					if self.stat == -2:
						self.tmpVal = realNum
						self.stat = 2
					else:
						self.tmpKey = realNum
						self.stat = 3
				else:
					raise TypeError('Extra Num %s' % self.curr)

			elif self.luaTblContent[self.curr].isalpha() or self.luaTblContent[self.curr] == '_':
				begin = self.curr
				ret = self.alter(spaces + (',',';'))

				name = ''
				if ret == -1:
					name = self.luaTblContent[begin:]
				else:
					name = self.luaTblContent[begin:self.curr]

				if name == 'nil':
					if self.stat == 0:
						self.tmpKey = None
						self.stat = 3
					elif self.stat == -2:
						self.tmpVal = None
						self.stat = 2
					else:
						raise TypeError('Extra nil %s' % self.curr)
				elif name in ('false', 'true'):
					tmp = True
					if name == 'false':
						tmp = False
					if self.stat == 0:
						self.tmpKey = tmp
						self.stat = 3
					elif self.stat == -2:
						self.tmpVal = tmp
						self.stat = 2
					else:
						raise TypeError('Extra T/F %s' % self.curr)
				else:
					if self.stat == 0:
						self.tmpKey = name
						self.stat = 4
					else:
						raise TypeError('Extra exp name %s' % self.curr)


			else:
				raise TypeError("Oop")

	def _store(self):
		if self.stat == -1:
			raise TypeError("Wait for Key %s", self.curr)
		elif self.stat == -2:
			raise TypeError("Wait for Val %s", self.curr)
		elif self.stat == 1 or self.stat == 3:
			if self.tmpKey == None and self.stat == 1:
				raise TypeError("stat 1 but None tmpKey %s", self.curr)
			self.pyList.append(self.tmpKey)
			self.tmpKey = None
			self.stat = 0
		elif self.stat == 2:
			if self.tmpKey == None:
				raise TypeError('No tmpKey when stat 2 %s', self.curr)
			if self.tmpVal == None:
				#raise TypeError('No tmpVal when stat 2 %s', self.curr)
				pass
			else:
				self.pyDict[self.tmpKey] = self.tmpVal
			self.tmpKey = None
			self.tmpVal = None
			self.stat = 0
		elif self.stat == 0:
			pass
		else:
			raise TypeError("store stat eror %s "% self.curr)

	def _getStr(self, pat):
		if not self._next():
			raise TypeError('Error in %s: EOF', pat)
		ret = self.luaTblContent.find(pat, self.curr + 1)
		if not ret:
			raise TypeError('Error in %s: no found', pat)
		else:
			while self.luaTblContent[ret - 1] ==  "\\":
				ret = self.luaTblContent.find(pat, ret + 1)
				if ret == -1:
					raise TypeError('Error in %s: no found', pat)
			ocurr = self.curr
			self.curr = ret + 1	
			return self.luaTblContent[ocurr:ret]

	def _next(self):
		self.curr += 1
		if self.curr >= len(self.luaTblContent):
			return False
		else:
			return True

	def _checkNext(self, pat):
		if self.curr + 1 >= len(self.luaTblContent):
			return False
		if self.luaTblContent[self.curr + 1] in pat:
			return True
		else:
			return False

	def _comment(self):
		if self._next():
			while self.luaTblContent[self.curr] not in ('\n', '\r'):
				if not self._next():
					break
			else:
				self._next()

	def _findRhs(self):
		spaces = ('\t', ' ', '\n', '\r', '\f', '\v')
		if self.curr >= len(self.luaTblContent):
			raise TypeError('stat -1 no ] %s', self.curr)
		
		while(self.luaTblContent[self.curr] != ']'):
			if self.luaTblContent[self.curr] not in spaces:
				raise TypeError('extra char  %s', self.curr)
			self._next()
			if self.curr >= len(self.luaTblContent):
				raise TypeError('stat -1 no ] %s', self.curr)
		self.stat = 1
		self._next()	
	
	def str2Num(self, strNum, begin):
		if strNum == '':
			raise TypeError('No strNum %s' % begin)
		if strNum.find('.') != -1 and self.decimal:
			raise TypeError('Too many . in num %s' %begin)
		if strNum[0] == '-' and self.negative:
			raise TypeError('Too many - in num %s' %begin)


		if strNum[0] == '0' and len(strNum) > 1 and strNum[1] in 'Xx':
			if self.decimal:
				raise TypeError('Error .0x %s' % self.curr)
			if self.negative:
				strNum = '-' + strNum
			if '.' not in strNum:
				return int(strNum, 16)
			else:
				 raise TypeError('0x.................')
			
		else:
			if self.decimal:
				strNum = '0.' + strNum
			if self.negative:
				strNum = '-' + strNum

			if 'e' in strNum or '.' in strNum:
				return float(strNum)
			else:
				return int(strNum)

	def alter(self, tup):
		if self.curr > len(self.luaTblContent):
			return -1
		while self.luaTblContent[self.curr] not in tup:
			if not self._next():
				return -1
		return 0

	def deepCopyDict(self, d):
		result = {}
		for key in d:
			if isinstance(d[key], dict):
				result[key] = self.deepCopyDict(d[key])
			else:
				result[key] = d[key]
		return result

	def _dict2lua(self, d):
		mystr = '{'
		for key in d:
			mystr += '['
			if isinstance(key, str):
				mystr += '"'
			mystr += str(key)
			if isinstance(key, str):
				mystr += '"'
			mystr += ']'
			mystr += ' = ' 
			if isinstance(d[key] , dict):
				mystr += self._dict2lua(d[key])
			elif isinstance(d[key], list):
				mystr += '{'
				for each in d[key]:
					if each == None:
						mystr += 'nil, '
					else:
						mystr += str(each)
						mystr += ', '
				mystr += '}'
			elif d[key] == False:
				mystr += 'false, '
			elif d[key] == True:
				mystr += 'True, '
			elif isinstance(d[key], str):
				mystr += '"'
				mystr += d[key]
				mystr += '"'
			else:
				mystr += str(d[key])
			mystr += ', '
		mystr += '}'
		return mystr

		
if __name__ == '__main__':
	a1 = PyLuaTblParser()
	a2 = PyLuaTblParser()
	a3 = PyLuaTblParser()

	file_path = r'C:\Users\S6\Desktop\output.txt'

	test_str = '{array = {65,23,5,},dict = {mixed = {43,54.33,false,9,string = "value",},array = {3,6,4,},string = "value",},}'
	a1.load(test_str)
	print a1
	'''
	d1 = a1.dumpDict()
	print d1

	a2.loadDict(d1)
	
	
	a2.dumpLuaTable(file_path)
	
	a3.loadLuaTable(file_path)

	d3 = a3.dumpDict()
 	print d3
 	'''

