1.模块使用说明：
PyLuaTblParser为所需类，包含了6个规定的成员函数。

2.作业说明：
实现方式为简单的状态机，基本思路是逐个字符扫描（当然，遇到{}、字符串以及注释做跳跃处理），遇到特定字符做出相应操作，并变更当前状态。
共有六个状态，以数字标识，如下：
	-2 wait for val when left is = #左侧有个等号
	-1 wait for key when left is [ #左侧有个key的左括号
	0 normal 					   #常规状态
	0.5 						   #已获得key，等待] 
	1							   #已获得key
	2							   #已获得key和value，或只有value
	'''
					name
	|---------------->--------------->|
	|                                 |
	| 	[       num or str        ]   |   =       exp
	0 ----> -1 -----------> 0.5 ----> 1 ----> -2 ----> 2 ----> End
	|                     exp                          |         |
	|---------------------->-------------------------->|         |
	|                    , or ;                		   |         |
	|<-----------------------<-------------------------|         |
	|                                                            |
	|-------------->---------------------->--------------------->|

	'''
	num str name exp的定义参考Lua文档和题目要求
由于实验室项目紧张，并没有完成进阶要求，测试用例改动之后也没有做相应的改动。

3.已知的几个未完成的测试用例：
a)输入的Tbl外层含注释的，例如"--comment\n{}--comment2"
b)十六进制中含小数的，例如"0x.01"
c)十六进制中含p的，例如"0x3p-1"
