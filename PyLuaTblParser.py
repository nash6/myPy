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
	
		d = self.dumpDict()
		result = self._dict2lua(d)
		return result

	def loadLuaTable(self, f):
		fp = open(f, 'r')
		tmpstr = ''
		for item in fp:
			tmpstr += str(item)
		fp.close()
		self.load(tmpstr)


	def dumpLuaTable(self, f):
		fp = open(f, 'w')
		fp.write(self.dump())
		fp.close()

	def loadDict(self, d):
		self.pyDict = {}
		self.pyList = []
		myd = self.deepCopyDict(d)
		for key in myd:
			if isinstance(key, str) or isinstance(key, int) or isinstance(key, float):
				self.pyDict[key] = myd[key]


	def dumpDict(self):
		'''
		
		'''
		self._list2Dict()
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
					self._findRhs()
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
				if self.stat in (-2, -1, 0):
					raise TypeError(" ", self.stat)
				self._store()
				self._next()

			elif self.luaTblContent[self.curr] == '[':#[=[ or [key]
				if self._checkNext('=['):
					self._next()

					tmpstr = self._longBrackets()

					if tmpstr == None:
						raise TypeError('[=[ long string has no [')
									
					if self.stat == 0:
						self.tmpKey = tmpstr
						self.stat = 3
					elif self.stat == -1:
						self.tmpKey = tmpstr
						self._findRhs()
						self.stat = 1
					elif self.stat == -2:
						self.tmpVal = tmpstr
						self.stat = 2
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
				lhc = 0
				begin = self.curr
				if not self._next():
					raise TypeError('No match for { %s', self.curr)
				
				while True:
					if self.curr >= len(self.luaTblContent):
						raise TypeError('No match for { %s', self.curr)

					if self.luaTblContent[self.curr] == '}' and lhc == 0:
						break

					if self.luaTblContent[self.curr] in ('\'', '\"') :
						self._getStr(self.luaTblContent[self.curr])
					
					elif self.luaTblContent[self.curr] == '{':
						lhc += 1
						if not self._next():
							raise TypeError('No match for { %s', self.curr)
					elif self.luaTblContent[self.curr] == '}' and lhc != 0:						
						lhc -= 1
						if not self._next():
							raise TypeError('No match for { %s', self.curr)
					elif self.luaTblContent[self.curr] == '[':
						if self._checkNext('=['):
							self._next()
							self._longBrackets()
						else:
							if not self._next():
								raise TypeError('No match for { %s', self.curr)
					elif self.luaTblContent[self.curr] == '-':
						if self._checkNext('-'):
							self._next()#--
							if self._checkNext('['):
								self._next()#--[
								if self._checkNext('=['):
									self._next()
									self._longBrackets()
								else:
									self._comment()
							else:
								self._comment()
						else:
							self._next()
					else:
						self._next()
				
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
							self._next()
							ret = self._longBrackets()			
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
				#if self.stat not in (-2, -1):
				raise TypeError('Extra + %s' % self.curr)
				#self._next()

			elif self.luaTblContent[self.curr] in nums:
				begin = self.curr
				if self.stat == -1:
					if self.tmpKey != None:
						raise TypeError('Already has key in [  when read nums %s' % self.curr)

					ret = self.alterNum()
					if ret == -1:
						raise TypeError('Extra Num %s' % self.curr)
					
					strNum = self.luaTblContent[begin:self.curr]
					
					realNum = self.str2Num(strNum, begin)

					self.tmpKey = realNum					
					self._findRhs()

				elif self.stat == -2 or self.stat == 0:
					if self.tmpVal != None:
						raise TypeError('Already has val in nums %s' % self.curr)

					ret = self.alterNum()
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
				elif self.stat == 1:
					raise TypeError('Extra Num %s' % self.curr)
				elif self.stat == 2:
					raise TypeError('Extra Num %s' % self.curr)
				elif self.stat == 3:
					raise TypeError('Extra Num %s' % self.curr)
				elif self.stat == 4:
					raise TypeError('Extra Num %s' % self.curr)

			elif self.luaTblContent[self.curr].isalpha() or self.luaTblContent[self.curr] == '_':
				begin = self.curr
				ret = self.alter(spaces + (',',';','='))

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
					if self.stat == -2:
						self.tmpVal = None
						self.stat = 2
						#raise TypeError('Extra exp name %s %s' % (name,self.curr))
					elif self.stat == -1:
						raise TypeError('Extra exp name %s' % self.luaTblContent)
					elif self.stat == 0:
						self.stat = 4
						self.tmpKey = name
					elif self.stat == 1:
						raise TypeError('Extra exp name %s' % self.curr)
					elif self.stat == 2:
						raise TypeError('Extra exp name %s' % self.curr)
					elif self.stat == 3:
						raise TypeError('Extra exp name %s' % self.curr)
					elif self.stat == 4:
						raise TypeError('Extra exp name %s' % self.curr)
					
			else:
				#print self.curr
				raise TypeError("Oop %d %s" % (self.curr, self.luaTblContent[self.curr]))


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
				if self.tmpKey in self.pyDict:
					del self.pyDict[self.tmpKey]
			else:
				self.pyDict[self.tmpKey] = self.tmpVal
			self.tmpKey = None
			self.tmpVal = None
			self.stat = 0
		elif self.stat == 0:
			pass
		elif self.stat == 4:
			self.tmpKey = None
			self.pyList.append(None)
			self.stat = 0
		else:
			raise TypeError("store stat eror %s "% self.curr)

	def _getStr(self, pat):
		'''curr to next real char'''
		if not self._next():
			raise TypeError('Error in %s: EOF', pat)
		ret = self.luaTblContent.find(pat, self.curr )
		if not ret:
			raise TypeError('Error in %s: no found', pat)
		else:			
			while True:
				count = 0
				pre = ret - 1
				while pre >= 0 and self.luaTblContent[pre] ==  "\\":
					count += 1
					pre -= 1
			
				if count % 2 == 0:
					break
				ret = self.luaTblContent.find(pat, ret + 1)
				if ret == -1:
					raise TypeError('Error in %s: no found', pat)
			ocurr = self.curr
			self.curr = ret + 1	
			return self._transAscii(self.luaTblContent[ocurr:ret])

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
			while self.luaTblContent[self.curr] not in ('\n'):
				if not self._next():
					break
			else:
				self._next()

	def _findRhs(self):
		spaces = ('\t', ' ', '\n', '\r', '\f', '\v')
		if self.curr >= len(self.luaTblContent):
			raise TypeError('stat -1 no ] %s', self.curr)


		while self.luaTblContent[self.curr] in spaces:
			if not self._next():
				raise TypeError('stat -1 no ] %s', self.curr)


		if self.luaTblContent[self.curr] == '-':
			if self._checkNext('-'):
				self._next()#--
				if self._checkNext('['):
					self._next()#--[
					if self._checkNext('=['):
						self._next()
						self._longBrackets()
					else:
						self._comment()
				else:
					self._comment()
			else:
				raise TypeError('stat -1 no ] %s', self.curr)
		else:
			while(self.luaTblContent[self.curr] != ']'):
				if self.luaTblContent[self.curr] not in spaces:
					raise TypeError('extra char  %s', self.curr)
				self._next()
				if self.curr >= len(self.luaTblContent):
					raise TypeError('stat -1 no ] %s', self.curr)
		self.stat = 4
		self._next()	
	
	def str2Num(self, strNum, begin):
		if strNum == '':
			raise TypeError('No strNum %s' % begin)
		if strNum.find('.') != -1 and self.decimal:
			raise TypeError('Too many . in num %s' %begin)
		if strNum[0] == '-' and self.negative:
			raise TypeError('Too many - in num %s' %begin)


		if strNum[0] == '0' and len(strNum) > 1 and strNum[1] in 'Xx':
			if len(strNum) == 2:
				raise TypeError('Error only 0x %s' % self.curr)

			if self.decimal:
				raise TypeError('Error .0x %s' % self.curr)

			if self.negative:
				strNum = '-' + strNum
				self.negative = False

			if '.' not in strNum and 'e' not in strNum and 'E' not in strNum and 'p' not in strNum and 'P' not in strNum:
				return int(strNum, 16)
			else:#0x.pP
				raise TypeError('0x.................%s' % strNum)
			
		else:
			if self.decimal:	
				strNum = '0.' + strNum
				self.decimal = False
			if self.negative:
				strNum = '-' + strNum
				self.negative = False

			if 'e' in strNum or '.' in strNum:
				iinums = ('0', '1', '2', '3', '4', '5', '6','7','8','9','e','E','.','-','+')
				for each in strNum:
					if each not in iinums:
						raise TypeError('%s', strNum)
				return float(strNum)
			else:
				iinums = ('0', '1', '2', '3', '4', '5', '6','7','8','9','e','E','.','-')
				for each in strNum:
					if each not in iinums:
						raise TypeError('dwadw')
				return int(strNum)

	def alter(self, tup):
		if self.curr > len(self.luaTblContent):
			return -1
		while self.luaTblContent[self.curr] not in tup:
			if not self._next():
				return -1
		return 0

	def alterNum(self):
		if self.curr > len(self.luaTblContent):
			return -1
		nums = ('0', '1', '2', '3', '4', '5', '6','7','8','9','e','E','p','P','.','x','X','-','+')
		nums += ('a','A','b','B','c','C','D','d','e','E','f','F')
		while self.luaTblContent[self.curr] in nums:
			if self.luaTblContent[self.curr] == '-':
				if self._checkNext('-'):
					return 0
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
				tmp = self._strLuaTrans(key)
				mystr += tmp
				mystr += '"'			
			else:#0-9
				mystr += str(key)

			mystr += ']'
			mystr += ' = ' 

			if isinstance(d[key] , dict):
				mystr += self._dict2lua(d[key])
			elif isinstance(d[key], list):
				raise TypeError('U see list god')
			elif d[key] == False:
				mystr += 'false'
			elif d[key] == True and d[key] != 1:
				mystr += 'true'
			elif isinstance(d[key], str):
				mystr += '"'
				tmp = self._strLuaTrans(d[key])
				mystr += tmp
				mystr += '"'
			elif d[key] == None:
				mystr += 'nil'
			else:
				mystr += str(d[key])
			mystr += ', '
		mystr += '}'
		return mystr

	def _longBrackets(self):
		'''curr to next real char'''
		eqC = 0
		while self.luaTblContent[self.curr] == '=':
			eqC += 1
			if not self._next():
				return None

		if self.luaTblContent[self.curr] != '[':
			if self.luaTblContent[self.curr] == '\n':
				self._next()
			else:
				while self.luaTblContent[self.curr] != '\n':
					if not self._next():
						break
				self._next()
			return None

		else:
			pat = ']' + '=' * eqC + ']'

			ret = self.luaTblContent.find(pat, self.curr + 1)
			if ret == -1:
				raise TypeError('No match %s %s'%(pat,self.curr))

			tmpstr = self.luaTblContent[self.curr + 1: ret]
			if tmpstr[0] == '\n':
				tmpstr = tmpstr[1:]
			self.curr = ret + len(pat) 
			return self._transAscii(tmpstr)

	def _list2Dict(self):
		if len(self.pyList) == 0:
			return
		for index, item in enumerate(self.pyList):
			if item == None:
				'''
				if index in self.pyDict:
					del self.pyDict[index]
				'''
				self.pyDict[index+1] = item
			else:
				self.pyDict[index+1] = item

	def _strLuaTrans(self, s):
		if not isinstance(s, str):
			raise TypeError('strLuaTrans input is not str"')

		result = ""
		for index,char in enumerate(s):
			if char == '"' and self._isReal(index, s):
				result += '\\"'
			else:
				result += char
		return result
	
	def _isReal(self, index, s):
		if s[index] != '"':
			raise TypeError('isReal input "')
		
		count = 0
		pre = index - 1
		while pre >= 0 and s[pre] ==  "\\":
			count += 1
			pre -= 1
		
		if count % 2 == 0:
			return True

		return False

	def _transAscii(self, s):
		nums = ('0', '1', '2', '3', '4', '5', '6','7','8','9')
		count = 0
		result = ''

		index = 0
		while index < (len(s)):
			if s[index] == '\\':
				count += 1
				if count == 2:
					result += '\\\\'
					count = 0
				index += 1
			elif s[index] in nums:
				if count == 0:
					result += s[index]
					index += 1
				elif count == 1:
					numstr = s[index]
					index += 1
					if index < len(s) and s[index] in nums:
						numstr += s[index]
						index += 1
						if index < len(s) and s[index] in nums:
							numstr += s[index]
							index += 1	
					if int(numstr) != 0:
						result += chr(int(numstr))
					count = 0
				else:
					raise TypeError('U see god in _transAscii')
			else:
				count = 0
				result += s[index]
				index += 1
		return result

	def cutHeadTail(self, s):
		if s[0] != '{':
			pass

		
if __name__ == '__main__':
	
	print 'Hello World'
	
		
	


