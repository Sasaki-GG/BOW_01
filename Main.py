# -*- coding: utf-8 -*-

__author__ = 'GG.Pan && Mr.Dai'

import text_process as tp
import json
# import numpy as np

def max(a,b):
	if a>b:
		return a
	else:
		return b
def min(a,b):
	if a<b:
		return a
	else:
		return b

# 在控制台输出中文 ，输入为已经通过Jieba完成编码的list
def PrintCH(seg_list):
	print " /  ".join(seg_list)

# 通过lambda表达式排序
def json_srot(frequency):
	result = sorted(frequency.items(), key=lambda item:item[1])
	# print json.dumps(result,encoding='utf-8',ensure_ascii=False)


# 读取现有的词典
print "Loading the dictionary ..."
# 正负情感词
posdict = tp.read_lines("emotion_dict/pos_all_dict.txt")
negdict = tp.read_lines("emotion_dict/neg_all_dict.txt")
# 程度词
mostdict = tp.read_lines('degree_dict/most.txt')   					# 权值为2
verydict = tp.read_lines('degree_dict/very.txt')   					# 权值为1.75
moredict = tp.read_lines('degree_dict/more.txt')   					# 权值为1.5
ishdict = tp.read_lines('degree_dict/ish.txt')     					# 权值为1.25
insufficientdict = tp.read_lines('degree_dict/insufficiently.txt')  # 权值为0.5
inversedict = tp.read_lines('degree_dict/inverse.txt')  			# 权值为-1.0
print "Load completed ."	


# 词袋模型的系数匹配程度词
def match_Dict(word, sentiment_value):
	if word in mostdict:
		sentiment_value *= 2.00
	elif word in verydict:
		sentiment_value *= 1.75
	elif word in moredict:
		sentiment_value *= 1.50
	elif word in ishdict:
		sentiment_value *= 1.25
	elif word in insufficientdict:
		sentiment_value *= 0.50
	elif word in inversedict:
		sentiment_value *= -1.00
	return sentiment_value

#增加相同值，防止出现负数
def sent_abs(pos_score,neg_score):
	if pos_score>=0 and neg_score>=0:
		return (pos_score,neg_score)
	else:
		a = max(pos_score,neg_score)
		b = min(pos_score,neg_score)
		tmp = a - b
		if pos_score>=neg_score:
			return (tmp,0)
		else:
			return (0,tmp)


# 计算得分
def get_Score(text_target):
	# 单句得分
	single_score = []
	# 划分句子
	sentence = tp.cut_sentence(text_target)

	for sent in sentence:
		seg = tp.segmentation(sent)
		seg = tp.del_stopwords(seg)[:]
		#位置
		i = 0
		sen_position = 0
		#得分
		pos_score = 0
		neg_score = 0

		for word in seg:
			#积极
			if word in posdict:
				pos_score += 1
				for w in seg[sen_position:i]:
					pos_score = match_Dict(w,pos_score)
				sen_position = i + 1
			#消极
			elif word in negdict:
				neg_score += 1
				for w in seg[sen_position:i]:
					neg_score = match_Dict(w,neg_score)
				sen_position = i + 1 
			#句末
			elif word == ". ".decode("utf-8") or word == ".".decode("utf-8")  or word == "! ".decode("utf-8") or word == "! ".decode("utf-8"):
				for w in seg[::-1]:
					if w in posdict:
						pos_score += 2
						break
					elif w in negdict:
						neg_score += 2
						break
			i += 1
		# print "Positive: ",pos_score
		# print "Negetive: ",neg_score
		single_score.append(sent_abs(pos_score,neg_score))
	#最终分
	pos_final, neg_final = 0, 0
	for p_score, n_score in single_score:
		pos_final += p_score
		neg_final += n_score
	# print "Positive_F: ",pos_final
	# print "Negetive_F: ",neg_final

	ans = pos_final - neg_final
	ans = round(ans,1)
	return ans


# 运行
def run():
	X_test = open('test_data.txt','r')
	tmp = []
	for i in X_test.readlines():
		i = i.strip()
		i = i.decode("utf-8")
		tmp.append(i)
	# print tmp
	X_test.close()
	result = []
	for i in tmp:
		ans = get_Score(i)
		result.append((ans,i))
	return result

# 写入文件
def write_File(result):
	X_result = open('result_data.txt','w')
	# print result
	for tmp in result:
		X_result.write(str(tmp[0]))
		X_result.write(' : ')
		# print 'BUG'
		X_result.write(tmp[1])
		X_result.write('\n')
	X_result.close()


if __name__ == '__main__':
	# load_Dict()
	result = run()
	write_File(result)
	print 'Finished !'
