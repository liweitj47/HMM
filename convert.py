# encoding=utf-8

import re
p = re.compile('[\\s]+')

if __name__ == '__main__':
    lines = open('train').readlines()
    w = open('train-crf', 'w')
    for i in range(len(lines)):
        l = lines[i].decode('utf-8').strip('\n')
        if len(l) > 0:
            words = p.split(l)
            for word in words:
                for j in range(len(word)):
                    w.write(word[j].encode('utf-8'))
                    if len(word) == 1:
                        w.write(' S S')
                    elif j == 0:
                        w.write(' B B')
                    elif j == len(word) - 1:
                        w.write(' E E')
                    else:
                        w.write(' I I')
                        '''
                    if j == 0:
                        w.write('B-')
                    else:
                        w.write('I-')
                        '''
                    
                    # w.write(word[j].encode('utf-8'))
                    w.write('\n')
            w.write('\n')
        else:
            w.write('\n')
w.close()
