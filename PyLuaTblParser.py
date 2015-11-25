#PyLuaTblParser.py
#Written by lyc 2015.11.24
#For Netease codefly



class PyLuaTblParser(object):
	def __init__(self):
		self.listCount = 0
		self.pyDict = {}
		self.pyList = []
		pass

	def load(self, s):

		pass
	
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

	#from now on
	#fun are private

	def __addList(self, l):
		

	def __addDict(self, d):

	def _luaParse(self, s):	
		if not self.__isStr(s):
			raise TypeError('Input is NOT string!')
		if not self.__isTableCons(s):
			raise TypeError('Input is NOT tableconstructor!')

		self.__analyse(s)

	
	def __getKey(self, s):
		s = self.__cutHeadTail(s)
		if s.isdigit():
			return int(s)
		elif s[0] == '\"' and s[-1] == '\"':
			return s[1:-1]
		else:
			raise TypeError('Key is not NUM or STR!')

	def __getValue(self, s):
		s = self.__cutHeadTail(s)
		
		if s.isdigit():
			return int(s)
		elif s[0] == '\"' and s[-1] == '\"':
			return s[1:-1]
		elif s[0] == '{':
			pass
			#return self.__
		else:
			return s

	def __getNext(self, s, pat):
		s = self.__cutHeadTail(s)
		index = s.find(pat)
		return index

	def __analyse(self, s):#s is table constructor
		s = self.__cutHeadTail(s)
		s = s[1:-1]
		s = self.__cutHeadTail(s)

		if s[0] == '[':
			rhs = s.find(']')
			if rhs == -1:
				raise TypeError('Input is NOT tableconstructor!')
			#tmpKey is the Key
			tmpKey = self.__getKey(s[1:rhs])
			s = s[rhs + 1:]

			tmpEq = self.__getNext(s, '=')
			if tmpEq == -1:
				raise TypeError('Input is NOT tableconstructor!')
			s = s[tmpEq + 1:]

			
			tmpEnd = self.__getNext(s, ',')
			
			tmpValue = []
			if tmpEnd == -1:
				tmpValue = self.__getValue(s[tmpEq+1:])
			else:
				tmpValue = self.__getValue(s[tmpEq+1:tmpEnd])
			
			print tmpValue
		else:#other 2 cont
			pass


	def __isTableCons(self, s):
		'''see s is table constructor or not'''
		tmps = self.__cutHeadTail(s)
		if tmps[0] == '{' and tmps[-1] == '}':
			return True
		else:
			return False

	def __isStr(self, s):
		'''see s is string or not'''
		if isinstance(s, str):
			return True
		else:
			return False

	def __cutHeadTail(self, s):
		'''cut the head and tail of s where is whitespace, '\t', '\n'''
		#rm whitespace
		s = s.lstrip().rstrip()
		spaceList = ('\t', '\n')
		#rm head
		while s[0] in spaceList:
			del s[0]
		#rm tail
		while s[-1] in spaceList:
			del s[-1]	
		return s





tPy = PyLuaTblParser()
tPy._luaParse('  \t   \n\n{  [ "av"  ] = abc 	}  \n  \t\t')
