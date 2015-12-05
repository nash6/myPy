#PyLuaTblParser.py
#Written by lyc 2015.11.24
#For Netease codefly



class PyLuaTblParser(object):
	def __init__(self):
		self.pyDict = {}
		self.pyList = []

		self.luaTblContent = ''
		self.curr = 0

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
		0.5
		1
		2
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
		#self.pyDict = {}
		#self.pyList = []
		myd = {}
		if isinstance(d, list):
			ml = self.deepCopyList(d)
			self._list2Dict(ml, myd)
		else:
			myd = self.deepCopyDict(d)
		for key in myd:
			if isinstance(key, str) or isinstance(key, int) or isinstance(key, float):
				self.pyDict[key] = myd[key]


	def dumpDict(self):
		'''
		
		'''
		if len(self.pyDict) == 0:
			if len(self.pyList) == 0:
				return {}
			else:
				return self.deepCopyList(self.pyList)
		else:
			self._list2Dict(self.pyList, self.pyDict)
			return self.deepCopyDict(self.pyDict)

	#private fun
	def _lex(self):
		spaces = ('\t', ' ', '\n', '\r', '\f', '\v')
		nums = ('0', '1', '2', '3', '4', '5', '6','7','8','9')
		while True:
			if self._overRange():
				self._store()
				break

			if self.luaTblContent[self.curr] in spaces:
				self._next()
			elif self.luaTblContent[self.curr] == ']':
				if self.stat == 0.5:
					self.stat = 1
					self._next()
				else:
					raise TypeError('Extra ]')
			elif self.luaTblContent[self.curr] in ('\'','\"'):
				if self.stat == 0:
					self.tmpKey = self._getStr(self.luaTblContent[self.curr])
					self.stat = 2
				elif self.stat == -1:
					self.tmpKey = self._getStr(self.luaTblContent[self.curr])
					self.stat = 0.5
				elif self.stat == -2:
					self.tmpVal = self._getStr(self.luaTblContent[self.curr])
					self.stat = 2
				else:
					raise TypeError('Extra \' or " %s', self.curr)
					
			elif self.luaTblContent[self.curr] == '=':
				if self.stat == 1:
					self.stat = -2
					self._next()
				else:
					raise TypeError('Extra = %s', self.curr)

			elif self.luaTblContent[self.curr] in (',', ';'):
				if self.stat != 2:
					raise TypeError(" ", self.stat)
				self._store()
				self.stat = 0
				self._next()

			elif self.luaTblContent[self.curr] == '[':#[=[ or [key]
				if self._checkNext('=['):
					self._next()

					tmpstr = self._longBrackets()

					if tmpstr == None:
						raise TypeError('[=[ long string has no [')
									
					if self.stat == 0:
						self.tmpKey = tmpstr
						self.stat = 2
					elif self.stat == -1:
						self.tmpKey = tmpstr
						self.stat = 0.5
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
					if self._overRange():
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
							if self._longBrackets() == None:
								raise TypeError('{ [ error %s', self.curr)
						else:
							if not self._next():
								raise TypeError('No match for { %s', self.curr)
					elif self.luaTblContent[self.curr] == '-':					
						if self._checkNext('-'):
							self._ignoreComment()
						else:
							self._next()
					else:
						self._next()
				
				recur = PyLuaTblParser()
				recur.load(self.luaTblContent[begin:self.curr+1])

	
				if self.stat == 0:
					self.tmpKey = recur.dumpDict()
				else:
					self.tmpVal = recur.dumpDict()
				self.stat = 2
				self._next()

			elif self.luaTblContent[self.curr] == '.': #num
				if self.stat not in (0,-1,-2) or self.decimal == True:
					raise TypeError('Extra . %s' % self.curr)

				if self._checkNext(str(nums)):
					if self._checkNext('0'):
						if self._checkNext('xX'):
							raise TypeError('.0x %s' % self.curr)
					if self.decimal == True:
						raise TypeError('Too many .')
					self.decimal = True
					self._next()
				else:
					raise TypeError('Extra . %s' % self.curr)

			elif self.luaTblContent[self.curr] == '-':
				if self._checkNext('-'):				
					self._ignoreComment()
				elif self._checkNext('.'+str(nums)):
					if self.stat not in (0,-1,-2) or self.decimal == True:
						raise TypeError('Extra . %s' % self.curr)

					if self.negative == True:
						raise TypeError('Too many -')
					self.negative = True
					self._next()
				else:
					raise TypeError('Extra - %s' % self.curr)

			elif self.luaTblContent[self.curr] in nums:
				begin = self.curr
				if self.stat == -1:
					ret = self.alterNum()
					if ret == -1:
						raise TypeError('Extra Num %s' % self.curr)
					
					strNum = self.luaTblContent[begin:self.curr]
					
					realNum = self.str2Num(strNum, begin)

					self.tmpKey = realNum
					
					self.stat = 0.5

				elif self.stat == -2 or self.stat == 0:
		
					ret = self.alterNum()

					if ret == -1:
						strNum = self.luaTblContent[begin:]
					else:
						strNum = self.luaTblContent[begin:self.curr]

					realNum = self.str2Num(strNum, begin)

					if self.stat == -2:
						self.tmpVal = realNum
					else:
						self.tmpKey = realNum
					self.stat = 2
					
				elif self.stat == 1:
					raise TypeError('Extra Num %s' % self.curr)
				elif self.stat == 2:
					raise TypeError('Extra Num %s' % self.curr)
				elif self.stat == 0.5:
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
						self.tmpVal = 'nil'
						self.stat = 2
					elif self.stat == -2:
						self.tmpVal = None
						self.tmpKey = None
						self.stat = 2
					else:
						raise TypeError('Extra nil %s' % self.curr)
				elif name in ('false', 'true'):
					tmp = True
					if name == 'false':
						tmp = False
					if self.stat == 0:
						self.tmpKey = tmp
						self.stat = 2
					elif self.stat == -2:
						self.tmpVal = tmp
						self.stat = 2
					else:
						raise TypeError('Extra T/F %s' % self.curr)
				else:
					if self.stat == -2:
						if not name[0] == '_':
							raise TypeError()
						raise TypeError('Extra exp name %s %s' % (name,self.curr))
					elif self.stat == -1:
						raise TypeError('Extra exp name %s' % self.luaTblContent)
					elif self.stat == 0:
						self.stat = 1
						print name
						self.tmpKey = name
					elif self.stat == 0.5:
						raise TypeError('Extra exp name %s' % self.curr)
					elif self.stat == 1:
						raise TypeError('Extra exp name %s' % self.curr)
					elif self.stat == 2:
						raise TypeError('Extra exp name %s' % self.curr)
			else:
				#print self.curr
				raise TypeError("Oop %d %s" % (self.curr, self.luaTblContent[self.curr]))


	def _store(self):
		if self.stat in (-1,0.5,1,-2):
			raise TypeError("Wait for Key %s", self.curr)
		'''
		elif self.stat == -2:
			raise TypeError("Wait for Val %s", self.curr)
		elif self.stat == 1 or self.stat == 3:
			if self.tmpKey == None and self.stat == 1:
				raise TypeError("stat 1 but None tmpKey %s", self.curr)
			self.pyList.append(self.tmpKey)
			self.tmpKey = None
			self.stat = 0
		'''
		if self.stat not in (0,2):
			raise TypeError('Store when error stat %s', self.curr)

		if self.stat == 0:
			if self.tmpKey != None or self.tmpVal != None:
				raise TypeError('stat 0 has key or val %s', self.curr)
			return

		if self.tmpKey == None:
			if self.tmpVal == 'nil':
				self.pyList.append(None)
			else:
				pass
		else:
			if self.tmpVal == None:
				self.pyList.append(self.tmpKey)
			else:
				self.pyDict[self.tmpKey] = self.tmpVal
		self.stat = 0

		self.tmpKey = None
		self.tmpVal = None

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
			insideStr = self.luaTblContent[ocurr:ret]
			return self._transAscii(insideStr, 0 , pat)

	def _next(self):
		self.curr += 1
		if self._overRange():
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
					raise TypeError('--comment no \n')
			else:
				self._next()

	def _findRhs(self):
		spaces = ('\t', ' ', '\n', '\r', '\f', '\v')
		if self._overRange():
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
				if self._overRange():
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
		for key in d.keys():
			if isinstance(d[key], dict):
				result[key] = self.deepCopyDict(d[key])
			elif isinstance(d[key], list):
				result[key] = self.deepCopyList(d[key])
			else:
				result[key] = d[key]
		return result

	def deepCopyList(self, l):
		result = []
		for item in l:
			if isinstance(item, dict):
				result.append(self.deepCopyDict(item))
			elif isinstance(item, list):
				result.append(self.deepCopyList(item))
			else:
				result.append(item)
		return result


	def _2lua(self):
		mystr = '{'
		mystr += self._list2lua(self.pyList)
		mystr += self._dict2lua(self.pyDict)
		mystr += '}'

		return mystr
	def _dict2lua(self, d):
		if isinstance(d, list):
			return self._list2lua(d)
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

			if isinstance(d[key], list) or isinstance(d[key], dict):
				mystr += self._dict2lua(d[key])
			elif d[key] == False and isinstance(d[key], bool):
				mystr += 'false'
			elif d[key] == True and isinstance(d[key], bool):
				mystr += 'true'
			elif isinstance(d[key], str):
				mystr += '"'
				tmp = self._strLuaTrans(d[key])
				mystr += tmp
				mystr += '"'
			elif d[key] == None:
				mystr += 'nil'
			elif isinstance(d[key], PyLuaTblParser):
				mystr += d[key].dump()
			else:
				mystr += str(d[key])
			mystr += ', '
		mystr += '}'
		return mystr

	def _list2lua(self, l):
		mystr = '{'
		for item in l:
			if isinstance(item, list) or isinstance(item, dict):
				mystr += self._dict2lua(item)
			elif item == False and isinstance(item, bool):
				mystr += 'false'
			elif item == True and isinstance(item, bool):
				mystr += 'true'
			elif isinstance(item, str):
				mystr += '"'
				tmp = self._strLuaTrans(item)
				mystr += tmp
				mystr += '"'
			elif item == None:
				mystr += 'nil'
			else:
				mystr += str(item)
			mystr += ', '
		mystr += '}'
		return mystr

	def _longBrackets(self):
		'''
		call this when curr = '[=' or '[['
		curr to next real char
		'''
		eqC = 0
		while self.luaTblContent[self.curr] == '=':
			eqC += 1
			if not self._next():
				return None

		if self.luaTblContent[self.curr] != '[':
			if self.luaTblContent[self.curr] == '\n':
				self._next()
			else:
				self._comment()
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
			return self._transAscii(tmpstr, 1)

	def _list2Dict(self, l , d):
		if len(l) == 0:
			return
		for index, item in enumerate(l):
			if item == None:
				'''
				if index in self.pyDict:
					del self.pyDict[index]
				'''
				d[index+1] = item
			else:
				d[index+1] = item

	def _strLuaTrans(self, s):
		if not isinstance(s, str):
			raise TypeError('strLuaTrans input is not str"')

		result = ""
		pre = False
		for index,char in enumerate(s):
			#if char == '"' and self._isReal(index, s):
				#result += '\\"'
			#else:
				#result += char
			if char == '\\':
				result += '\\\\'
			elif char == '"':
				result += '\\"'
			elif char == '\a':
				result += '\\a'
			elif char == '\b':
				result += '\\b'
			elif char == '\f':
				result += '\\f'
			elif char == '\n':
				result += '\\n'
			elif char == '\r':
				result += '\\r'
			elif char == '\v':
				result += '\\v'
			elif char == '\t':
				result += '\\t'
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

	def _transAscii(self, s, longStr = 0, pat = '\''):
		'''
		lua str to py str
		'''
		nums = ('0', '1', '2', '3', '4', '5', '6','7','8','9')
		c = 'abfnrtv'
		char = tuple(c)
		if pat == '\'':
			fool = '\''
		else:
			fool = '"'

		#fool = None

		pre = False
		result = ''

		if longStr == 0:
			index = 0
			while index < (len(s)):
				if pre:
					if s[index] == '\\':
						result += '\\'	
										
					#elif s[index] in char:
						#result += '\\\\' + s[index]						
					#elif s[index] in nums:
						#result += '\\\\' + s[index]		
								
					elif s[index] == fool:
						result += s[index]
					elif s[index] == 'a':
						result += '\a'
					elif s[index] == 'b':
						result += '\b'
					elif s[index] == 'f':
						result += '\f'
					elif s[index] == 'n':
						result += '\n'	
					elif s[index] == 'r':
						result += '\r'	
					elif s[index] == 't':
						result += '\t'	
					elif s[index] == 'v':
						result += '\v'			
					else:
						result += '\\'
						result += s[index]
						#raise TypeError('in short str \\ error')
					pre = False	
				else:
					if s[index] == '\\':
						pre = True
					else:
						result += s[index]
				index += 1
			return result
		else:
			return s

	
	def _overRange(self):
		if self.curr >= len(self.luaTblContent):
			return True
		else:
			return False

	def _ignoreComment(self):
		'''
		call this func only with curr = '-' and next =' -' 
		finished with curr = next real one or overRange	
		'''
		if self.luaTblContent[self.curr] != '-' or not self._checkNext('-'):
			raise TypeError('Comment begin with no --')
		
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

	def _getTbl(self, s):
		'''
		s[0] = '{'
		find '}'
		'''
		tmp = PyLuaTblParser()
		tmp.luaTblContent = s
		
		
		if not tmp._next():
			raise TypeError('{')

		while tmp.luaTblContent[tmp.curr] in spaces:
			if not tmp._next():
				raise TypeError('{')

		if tmp.luaTblContent[tmp.curr] == '-':
			tmp._ignoreComment()
		




if __name__ == '__main__':
	
	print 'Hello World'
	
		
	


