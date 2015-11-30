#PyLuaTblParser.py
#Written by lyc 2015.11.24
#For Netease codefly



class PyLuaTblParser(object):
	def __init__(self):
		self.pyDict = {}
		self.pyList = []
		

	def load(self, s):
		'''load Lua table'''
		if not isinstance(s, str):
			raise TypeError('Input is NOT string!')

		s = s.strip()
		if not (s[0] == '{' and s[-1] == '}'):
			raise TypeError('Input is NOT tableconstructor!')

		s = s[1:-1].strip()

		self.luaTblContent = s
		self.curr = 0
		self.stat = 0
		'''
		-2 wait for val when =
		-1 wait for key when []
		0 normal
		1 has str or [] key
		2 has key and val
		3 has 'str' list
		'''
		self._lex()

		print self.pyDict
		print self.pyList

	def dump(self):
		pass

	def loadLuaTable(self, f):
		pass

	def dumpLuaTable(self, f):
		pass

	def loadDict(self, d):
		pass

	def dumpDict(self):
		pass

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
				else:
					raise TypeError('Extra = %s', self.curr)
			elif self.luaTblContent[self.curr] in (',', ';'):
				self._store()
				self._next()
			elif self.luaTblContent[self.curr] == '[':
				if self.stat == 0:
					self.stat = -1
					self._next()
				else:
					raise TypeError('Extra [ %s', self.curr)

			elif self.luaTblContent[self.curr] == '{':
				pass
			elif self.luaTblContent[self.curr] == '.': #num
				pass
			elif self.luaTblContent[self.curr] == '-':
				pass
			elif self.luaTblContent[self.curr] in nums:
				pass
			elif self.luaTblContent[self.curr] == '\\':
				pass
			elif self.luaTblContent[self.curr].isalpha():
				pass	
			else:
				print "Oop"

	def _store(self):
		if self.stat == -1:
			raise TypeError("Wait for Key %s", self.curr)
		elif self.stat == -2:
			raise TypeError("Wait for Val %s", self.curr)
		elif self.stat == 1 or self.stat == 3:
			if self.tmpKey == None:
				raise TypeError("stat 1 but No tmpKey %s", self.curr)
			self.pyList.append(self.tmpKey)
			self.tmpKey = None
			self.stat = 0
		elif self.stat == 2:
			if self.tmpKey == None:
				raise TypeError('No tmpKey when stat 2 %s', self.curr)
			if self.tmpVal == None:
				raise TypeError('No tmpVal when stat 2 %s', self.curr)
			self.pyDict[self.tmpKey] = self.tmpVal
			self.tmpKey = None
			self.tmpVal = None
			self.stat = 0

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

	

	

if __name__ == '__main__':
	tPy = PyLuaTblParser()
	tPy.load('{["abc"] = "123", "456" ,"av", }')

