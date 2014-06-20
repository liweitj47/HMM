from __future__ import division
from math import log
class Sentence:
    '''
    classdocs
    '''

    def __init__(self, tag_num):
        '''
        Constructor
        '''
        self.word_tag = []
        self.tag_num = tag_num
        self.add_word_tag('*', '*')
        self.add_word_tag('*', '*')
        self.tag_dict = {'B' : 0, 'I' : 1, 'E' : 2, 'S' : 3, '$':4, '*':5}
        self.tag_dict_rev = ['B', 'I', 'E', 'S', '$', '*']
    
    def add_word_tag(self, word, tag):
        self.word_tag.append((word, tag))
        
    def finish(self, word_dict, word_tag_dict, tag_uni_count, tag_bigram_count, tag_trigram_count):
        self.add_word_tag('$', '$')
        self.cal_word_tag_count(word_tag_dict)
        self.cal_tag_uni_count(tag_uni_count)
        self.cal_tag_bigram_count(tag_bigram_count)
        self.cal_tag_trigram_count(tag_trigram_count)
        self.cal_word_count(word_dict)
    
    def cal_word_count(self, word_dict):
        for i in range(len(self.word_tag)):
            if self.word_tag[i][0] in word_dict:
                word_dict[self.word_tag[i][0]] += 1
            else:
                word_dict[self.word_tag[i][0]] = 1
    
    def cal_word_tag_count(self, word_tag_dict):
        for i in range(2, len(self.word_tag)):
            if self.word_tag[i][0] not in word_tag_dict:
                word_tag_dict[self.word_tag[i][0]] = [0 for j in range(self.tag_num)]
            word_tag_dict[self.word_tag[i][0]][self.tag_dict[self.word_tag[i][1]]] += 1
    
    def cal_tag_uni_count(self, tag_uni_count):
        for i in range(len(2, self.word_tag)):
            tag_uni_count[self.tag_dict[self.word_tag[i][1]]] += 1
        
    def cal_tag_bigram_count(self, tag_bigram_count):
        for i in range(1, len(self.word_tag) - 1):
            tag_bigram_count[self.tag_dict[self.word_tag[i][1]]][self.tag_dict[self.word_tag[i + 1][1]]] += 1
                
    def cal_tag_trigram_count(self, tag_trigram_count):
        for i in range(0, len(self.word_tag) - 2):
            tag_trigram_count[self.tag_dict[self.word_tag[i][1]]][self.tag_dict[self.word_tag[i + 1][1]]][self.tag_dict[self.word_tag[i + 2][1]]]
    
    def Viterbi(self, word_tag_prob, tag_trigram_prob, result_list):
        '''
        right_num = 0
        result = []
        trans_prob = [[(0, 0) for j in range(self.tag_num)] for i in range(len(self.word_tag))]
        trans_prob[0][0] = (1, 0)
        trans_prob[0][3] = (1, 0)
        for i in range(1, len(self.word_tag)):  # the first character must be 'B'
            for j in range(self.tag_num):
                tem_prob = [0 for k in range(self.tag_num)]
                max_pos = 0
                max_value = 0
                for k in range(self.tag_num):
                    tem_prob[k] = (trans_prob[i - 1][k][0] * tag_bigram_prob[k][j]) * word_tag_prob[self.word_tag[i][0]][j]
                    if max_value < tem_prob[k]:
                        max_value = tem_prob[k]
                        max_pos = k 
                trans_prob[i][j] = (max_value, max_pos)
        max_pos = 0
        max_value = 0
        for j in range(self.tag_num):
            if max_value < trans_prob[-1][j][0]:
                max_pos = j
                max_value = trans_prob[-1][j][0]
        for i in range(len(trans_prob) - 1, 0, -1):
            max_pos = trans_prob[i][max_pos][1]
            result.append(self.tag_dict_rev[max_pos])
            
        # result.append('B')
        result.reverse()
        for i in range(len(self.word_tag) - 1):
            result_list.append(result[i])
            if result[i] == self.word_tag[i][1]:
                right_num += 1
        result_list.append('$')
        return right_num
        '''
        Pi = [[[(0, 0) for k in range(len(self.word_tag))] for j in range(self.tag_num)] for i in range(self.tag_num)]
        Pi[1][self.tag_dict['*']][self.tag_dict['*']] = 1
        for k in range(2, len(self.word_tag)):
            for u in range(self.tag_num):
                for v in range(self.tag_num):
                    for w in range(self.tag_num):
                        tem_prob = Pi[k - 1][w][u] * tag_trigram_prob[v][w][u] * word_tag_prob[self.word_tag[k][0]][v]
                        if tem_prob > Pi[k][u][v][0]:
                            Pi[k][u][v][0] = tem_prob
                            Pi[k][u][v][1] = w
        
        result = []
        max_pos = (0, 0)
        max_value = 0
        for j in range(self.tag_num):
            for k in range(self.tag_num):
                if max_value < Pi[-1][j][k][0]:
                    max_pos = (j, k)
                    max_value = Pi[-1][j][k][0]
        for i in range(len(Pi) - 1, 1, -1):
            max_pos = (Pi[i][max_pos[0]][max_pos[1]][1], max_pos[0])
            result.append(self.tag_dict_rev[max_pos][1])
            
        # result.append('B')
        result.reverse()
        right_num = 0
        for i in range(len(self.word_tag) - 1):
            result_list.append(result[i])
            if result[i] == self.word_tag[i][1]:
                right_num += 1
        result_list.append('$')
        return right_num
