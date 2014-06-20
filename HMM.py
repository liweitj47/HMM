# encoding=utf-8
from __future__ import division
from Sentence import Sentence
import cPickle
class HMM:
    '''
    classdocs
    '''

    def __init__(self, train_filename, test_filename, tag_num, l1, l2):
        '''
        Constructor
        '''
        self.word_count = {}
        self.word_tag_count = {}
        self.tag_uni_count = [0 for i in range(tag_num)]
        self.tag_bigram_count = [[0 for j in range(tag_num)] for i in range(tag_num)]
        self.tag_trigram_count = [[[0 for k in range(tag_num)] for j in range(tag_num)] for i in range(tag_num)]
        self.sents = [Sentence(tag_num)]
        self.total_tag = 0
        self.__rare_word = {}

        lines = open(train_filename).readlines()
        for i in range(len(lines)):
            line = lines[i].decode('utf-8').strip('\n')
            if len(line) > 0:
                wt = line.split('-')
                self.sents[-1].add_word_tag(wt[1], wt[0])
            else:
                self.sents[-1].finish(self.word_count, self.word_tag_count, self.tag_uni_count, self.tag_bigram_count, self.tag_trigram_count)
                self.total_tag += len(self.sents[-1].word_tag) - 2
                self.sents.append(Sentence(tag_num))
        self.sents[-1].finish(self.word_count, self.word_tag_count, self.tag_uni_count, self.tag_bigram_count, self.tag_trigram_count)
        self.total_tag += len(self.sents[-1].word_tag) - 2
        # self.word_prob = {}
        
        for w in self.word_count.keys():
            if self.word_count[w] <= 1:
                self.__rare_word[w] = self.word_count[w]
        
        self.word_tag_prob = {}
        for w in self.word_tag_count.keys():
            if w in self.__rare_word:
                self.word_tag_prob['RARE'] = [0 for i in range(tag_num)]
                for i in range(tag_num):
                    self.word_tag_prob['RARE'][i] = self.word_tag_count['RARE'][i] / self.tag_uni_count[i]
            else:
                self.word_tag_prob[w] = [0 for i in range(tag_num)]
                for i in range(tag_num):
                    self.word_tag_prob[w][i] = self.word_tag_count[w][i] / self.tag_uni_count[i]
        # self.tag_uni_prob = [0 for i in range(tag_num)]
        # for i in range(tag_num):
        #    self.tag_uni_prob[i] = self.tag_uni_count[i] / self.total_word
        # self.tag_bigram_prob = [[0 for j in range(tag_num)] for i in range(tag_num)]
        # for i in range(tag_num):
        #    for j in range(tag_num):
        #        self.tag_bigram_prob[i][j] = (self.tag_bigram_count[i][j] / self.total_bigram) / \
        #                (self.tag_uni_prob[i])
        self.tag_trigram_prob = [[[0 for k in range(tag_num)] for j in range(tag_num)] for i in range(tag_num)]
        for i in range(tag_num):
            for j in range(tag_num):
                for k in range(tag_num):
                    # q(i|j,k) that is the order of the tags is j,k,i
                    self.tag_trigram_prob[i][j][k] = l1 * (self.tag_uni_count[i] / self.total_tag) + \
                                                    l2 * (self.tag_bigram_count[k][i] / self.tag_uni_count[i]) + \
                                                    (1 - l2 - l1) * (self.tag_trigram_count[j][k][i] / self.tag_bigram_count[k][i])
        
    def test(self, filename, tag_num):
        lines = open(filename).readlines()
        w = open('result', 'w')
        test_sents = [Sentence(tag_num)]
        for i in range(len(lines)):
            line = lines[i].decode('utf-8').strip('\n')
            if len(line) > 0:
                wt = line.split('-')
                test_sents[-1].add_word_tag(wt[1], wt[0])
            else:
                test_sents[-1].add_word_tag('$', '$')
                test_sents.append(Sentence(tag_num))
        test_sents[-1].add_word_tag('$', '$')
        right_num = 0
        total_num = 0
        result_list = []
        for s in test_sents:
            right_num += s.Viterbi(self.word_tag_prob, self.tag_trigram_prob, result_list)
            total_num += len(s.word_tag) - 1
        for i in range(len(result_list)):
            if result_list[i] != '$':
                w.write(result_list[i])
            w.write('\n')
        w.close()
        print right_num / total_num
    
if __name__ == '__main__':
    train = HMM('train-hmm', 'test-hmm', 6, 0.3, 0.3)
    cPickle.dump(train, open('hmm-model', 'w'))
    train.test('test-hmm', 6)
        
