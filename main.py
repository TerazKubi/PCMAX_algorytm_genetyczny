import random

from pcmaxgen import PCmaxGen

if __name__ == '__main__':
    pop_num = 2000
    m_prob = 10
    a = (1/100)
    p = PCmaxGen("m10n200.txt", pop_num, m_prob, a)
    p.show_info()
    p.algo()





