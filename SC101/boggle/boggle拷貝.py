"""
File: boggle.py
Name: Dennis
----------------------------------------
已完成，需要優化
"""
import time
# This is the file name of the dictionary txt file
# we will be checking if a word exists by searching through it
FILE = 'dictionary.txt'
NUMBER = 4


def main():
	# input 處理
	boggle_list = {}
	for y in range(NUMBER):
		row = input(f'{y} row of letters ').lower().split()
		if check_input(row):
			print('Illegal input')
			break
		elif len(row) != NUMBER:
			print('Illegal input')
			break
		else:
			count_x = 0
			for char in row:
				boggle_list[f"{count_x}{y}"] = char
				count_x += 1
	# dictionary內容處理
	dict_list = {}
	read_dictionary(dict_list, boggle_list)
	start = time.time()
	# find boggle
	ans_list = []
	for boggle_x in range(NUMBER):
		for boggle_y in range(NUMBER):
			# 將xy合併成一個xy字串
			find_boggle(dict_list, boggle_list, ans_list, '', [], f'{boggle_x}{boggle_y}')
	print(f'There are {len(ans_list)} words in total')
	end = time.time()
	print('----------------------------------')
	print(f'The speed of your boggle algorithm: {end - start} seconds.')
	"""
	boggle_list
	{'00': 'f', '10': 'y', '20': 'c', '30': 'l',
	'01': 'i', '11': 'o', '21': 'm', '31': 'g',
	'02': 'o', '12': 'r', '22': 'i', '32': 'l',
	'03': 'h', '13': 'j', '23': 'h', '33': 'u'
	}
	"""


def check_input(row):
	"""
	:param row: a string
	:return: (bool) if it is an alphabet
	"""
	for i in row:
		if len(i) != 1:
			return True
		if not i.isalpha():
			return True
	return False


def find_neighbor(x_y_position):
	"""
	:param x_y_position: 當下字母的座標
	:return: 周圍所有可以走的座標(a list of "xy" positions)
	"""
	legal_key_position = []
	x_n = int(x_y_position[0])
	y_n = int(x_y_position[1])
	for a in range(-1, 2):
		for b in range(-1, 2):
			if 0 <= x_n + a <= NUMBER-1 and 0 <= y_n + b <= NUMBER-1:
				legal_key_position.append(f'{x_n + a}{y_n + b}')
	legal_key_position.remove(f'{x_n}{y_n}')						# 得到所有可行的全部座標(不能包含原本)
	return legal_key_position


def find_boggle(dict_list, boggle_list, ans_list, current, index_store, x_y_positions):
	"""
	:param dict_list: all possible words, a dict
	:param boggle_list: a 4x4 dict
	:param ans_list: store the possible boggle, need an empty list
	:param current: record the string every step, need an empty string
	:param index_store: 已經走過的座標index already pass through, need an empty list
	:param x_y_positions: 當下的座標
	:return:
	"""
	"""
	不使用base-case寫法
	if len(current) >= 4 and current in dict_list and current not in ans_list:
		ans_list.append(current)
		print(f'Found: "{current}"')
	for index in find_neighbor(x_y_positions):		# for-loop所有可以走的座標
		if index not in index_store:				# 沒有走過的才可以走
			current += boggle_list[index]			# 紀錄座標在boggle_list對應的的字母
			index_store.append(index)				# 紀錄走過的座標
			# explore
			if has_prefix(dict_list, current):		# 確認dict是否有該字串的開頭
				find_boggle(dict_list, boggle_list, ans_list, current, index_store, index)		# x_y_position傳入要改成index
			# Un_choose
			index_store.remove(index)
			current = current[:-1]
	"""
	if len(current) >= 4 and current in dict_list and current not in ans_list: 			# 改一下就跑出roomy了(?)
		ans_list.append(current)
		print(f'Found: "{current}"')
	else:
		# choose
		for index in find_neighbor(x_y_positions):		# for-loop所有可以走的座標
			if index not in index_store:				# 沒有走過的才可以走
				current += boggle_list[index]			# 紀錄座標在boggle_list對應的的字母
				index_store.append(index)				# 紀錄走過的座標
				# explore
				if has_prefix(dict_list, current):		# 確認dict是否有該字串的開頭
					find_boggle(dict_list, boggle_list, ans_list, current, index_store, index)		# x_y_position傳入要改成index
				# Un_choose
				index_store.remove(index)
				current = current[:-1]


def read_dictionary(dict_list, boggle_list):
	"""
	This function reads file "dictionary.txt" stored in FILE
	and appends words in each line into a Python dict
	"""
	# store all the  value of dictionary
	value = {}
	for key in boggle_list:
		# value.append(boggle_list[key])
		value[boggle_list[key]] = boggle_list[key]
	with open("dictionary.txt", "r") as r:
		for word in r:
			data = word.strip()
			if len(data) >= 4 and check(data, value):
				dict_list[data] = data


def check(data, value):
	"""
	:param data: a string of word
	:param value:  value list of boggle dict
	:return: (bool) if there is any words with the input letters
	"""
	for i in data:
		if i not in value:
			return False
	return True


def has_prefix(dict_list, sub_s):
	"""
	:param dict_list: list
	:param sub_s: (str) A substring that is constructed by neighboring letters on a 4x4 square grid
	:return: (bool) If there is any words with prefix stored in sub_s
	"""
	for i in dict_list:
		if i.startswith(sub_s):
			return True
	return False


if __name__ == '__main__':
	main()
