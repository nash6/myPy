#PyLuaTblParser.py
#Written by lyc 2015.11.24
#For Netease codefly



class PyLuaTblParser(object):
	def __init__(self):
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

	

	def _luaParse(self,s):	#s is a string
		rs = self.__preParse(s)
		self.data = self.__parse(rs)
		#print self.data
		

	def __findTwin(self, s, a = ',', b = ';'):
		af = s.find(a)
		bf = s.find(b)
		if af == -1:
			if bf == -1:
				return -1
			else:
				return bf
		else:
			if bf != -1:
				return min(af, bf)
			else:
				return af

	def __parse(self,s):
		#synatx
		#tableconstructor ::= '{' [fieldlist] '}'
		if s[0] != '{' or s[-1] != '}':
			raise TypeError('Input is NOT tableconstructor!')
		#get fieldlist  
		fieldlist = s[1:-1]
		#fieldlist ::= field {fieldsep field} [fieldsep]
		index = self.__findTwin(s)
		if index == -1:
			pass
		else:
			pass

		return fieldlist

	def __preParse(self,s):
		#if string or not
		if type(s) != type('str'):
			raise TypeError('Input is NOT string!')
		#remove \t \n and whitespace
		return s.replace('\t','').replace('\n','').replace(' ','')

tPy = PyLuaTblParser()
tPy._luaParse(''' {  {a fieldlist}	} ''')
