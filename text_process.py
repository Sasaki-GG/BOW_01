# -*- coding: utf-8 -*-

__author__ = 'GG.Pan && Mr.Dai'

import jieba
import jieba.posseg as pseg
import sys

reload (sys)
sys.setdefaultencoding("utf-8")

jieba.load_userdict('emotion_dict/pos_all_dict.txt')
jieba.load_userdict('emotion_dict/neg_all_dict.txt')

# 读取
def read_lines(file_name):
	tmp = open(file_name,'r')
	result = []
	for i in tmp.readlines():
		i = i.strip()
		i = i.decode("utf-8")
		result.append(i)
	tmp.close()
	return result

# 分词
def segmentation(sentence):
	seg_list = jieba.cut(sentence)
	result = []
	for i in seg_list:
		result.append(i)
	return result

# 分句
def cut_sentence(text):
	text = text.decode("utf-8")
	# 位置
	s = 0
	i = 0
	result = []
	token = 'Null'
	punt_list = ',.!?;~，。！？；～… '.decode('utf-8')
	for word in text:
		# 非标点
		if word not in punt_list:
			i += 1
			token = list(text[s:i+2]).pop()
		# 省略号
		elif word in punt_list and token in punt_list:
			i += 1
			token = list(text[s:i+2]).pop()
		# 断句
		else:
			result.append(text[s:i+1])
			s = i+1
			i += 1
	if s<len(text):
		result.append(text[s:])
	return result

# 去除停止词
def del_stopwords(text):
	stopwords = read_lines("emotion_dict/stop_words.txt")
	result = []
	for word in text:
		if word in stopwords:
			continue
		else:
			result.append(word)
	return result