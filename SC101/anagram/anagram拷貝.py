"""
File: anagram.py
Name:
----------------------------------
This program recursively finds all the anagram(s)
for the word input by user and terminates when the
input string matches the EXIT constant defined
at line 19

If you correctly implement this program, you should see the
number of anagrams for each word listed below:
    * arm -> 3 anagrams
    * contains -> 5 anagrams
    * stop -> 6 anagrams
    * tesla -> 10 anagrams
    * spear -> 12 anagrams
"""
import time                   # This file allows you to calculate the speed of your algorithm
# Constants
FILE = 'dictionary.txt'       # This is the filename of an English dictionary
EXIT = '-1'                   # Controls when to stop the loop
dict_list = {}


def main():
    print('Welcome to stanCode \"Anagram Generator\" (or -1 to quit)')
    while True:
        word = str(input('Find anagrams for: '))
        if word == EXIT:
            print('good bye~')
            break
        else:
            start = time.time()
            print("Searching...")
            read_dictionary(cut_word_as_list(word))
            print("dict number: ", len(dict_list))
            find_anagrams(word)
            end = time.time()
            print('----------------------------------')
            print(f'The speed of your anagram algorithm: {end - start} seconds.')


def cut_word_as_list(word):
    """
    :param word: a string, like 'spot', 'contains'
    :return: a list, like ['s', 'p', 'o', 't']
    """
    word_split_list = []
    for i in word:
        word_split_list.append(i)
    return word_split_list


def read_dictionary(lst):
    """
    :param lst: a list, like ['s', 'p', 'o', 't']
    :return: a dict contains all the word in 'dictionary.txt' that start_with the elements in lst
    """
    with open("dictionary.txt", "r") as r:
        for word in r:
            data = word.strip()
            # 字母長度相等
            if len(data) == len(lst) and check(data, lst):
                # 開頭為i(
                dict_list[data] = data
                # for i in lst:
                #     if data.startswith(i):
                #         # 最後一位假如也是i
                #         for j in lst:
                #             # for k in range(len(lst)):
                #             #     if data[k] == j:
                #             #         dict_list.append(data)
                #             if data[len(lst) - 1] == j:
                #                 # dict_list.append(data)          # 62個字 0.045s
                #                 dict_list[data] = data


def check(data, lst):
    """
    :param data: one string in dictionary
    :param lst:  a list, like ['s', 'p', 'o', 't']
    :return: boolean
    """

    for i in data:
        if i not in lst:
            return False
    return True


def has_prefix(sub_s):
    """
    :param sub_s: a string, if input a word 'stop', the given string may be 's', 'st', 'sto'...
    :return: True or False
    判斷sub_s是否存在dict_list，假如有會return true，全部跑完都沒有的話，return False
    """
    for i in dict_list:
        if i.startswith(sub_s):
            return True
    return False


def find_anagrams(s):
    """
    :param s: give a string
    :return: print the number of list and anagrams list
    """
    ans_lst = find_anagrams_helper(s, [], "", "")
    print(f"{len(ans_lst)} anagrams: {ans_lst}")


def find_anagrams_helper(input_s, ans_list, current_str, index_list):
    """
    :param input_s: give a string
    :param ans_list: store the possible anagram, need an empty list
    :param current_str: record the string every step, need an empty string
    :param index_list:  record the  index of input_s, need an empty list
    :return: a list contains anagrams of input_s
    """
    # base-case
    # 有到base-case -> 印出current_str
    if len(current_str) == len(input_s):
        if current_str in dict_list:
            if current_str not in ans_list:
                ans_list.append(current_str)
                print(current_str)
                print("Searching...")
    else:
        for i in range(len(input_s)):
            if str(i) not in index_list:
                # choose
                index_list += str(i)
                # 每次取index_list倒數第一個element
                current_str += input_s[int(index_list[-1])]
                if has_prefix(current_str):
                    # explore
                    find_anagrams_helper(input_s, ans_list, current_str, index_list)
                # Un-choose
                # 移除最後一個element
                current_str = current_str[:-1]
                index_list = index_list[:-1]

        ###### 改寫成dict #######
        # for i in range(len(input_s)):
        #     if str(i) not in index_list:
        #         # choose
        #         index_list[str(i)] = input_s[i]
        #         current_str += index_list[str(i)]
        #         # if len(current_str) == 1:
        #         #     find_anagrams_helper(input_s, ans_list, current_str, index)
        #         # else:
        #         if has_prefix(current_str):         # 每次取最後一個數字
        #             # explore
        #             find_anagrams_helper(input_s, ans_list, current_str, index_list)
        #         # Un-choose
        #         current_str = current_str[:-1]
        #         index_list.pop(str(i))
    return ans_list


if __name__ == '__main__':
    main()
