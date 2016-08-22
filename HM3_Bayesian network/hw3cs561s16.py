import sys
import math
import copy

query_list = []
event_list = []
event_dict = {}
dec_list = []
output = []
query_type = ""

class Event(object):
    name = ""
    positive = 0
    negative = 0
    has_parent = False
    parent_list = []
    prob = {}

    def __init__(self):
        self.name = ''
        self.positive = 0
        self.negative = 0
        self.has_parent = False
        self.parent_list = []
        self.prob = {}

class Query(object):
    type = ""
    has_parent = False
    left_part = []
    right_part = []

    def __init__(self):
        self.type = ""
        self.has_parent = False
        self.left_part = []
        self.right_part = []

class Utility():
    list  = []
    table = {}

    def __init__(self):
        self.list = []
        self.table = {}

utility = Utility()




def read(filename):
    with open(filename, 'r') as file:
        sentence = file.readline().strip("\n")
        while sentence != "******":
            query = sentence_to_query(sentence)
            query_list.append(query)
            sentence = file.readline().strip("\n")

        while True:
            sentence = file.readline().strip("\n")
            event = sentence_to_event(sentence)
            num = len(event.parent_list)
            number = int(math.pow(2, num))

            for i in range(number):
                sentence = file.readline().strip("\n")
                if sentence == 'decision':
                    dec_list.append(event)
                    event.positive = 1.00
                    event.negative = 1.00
                    pass
                else:
                    sentence_to_prob(event, sentence)

            event_list.append(event)
            sentence = file.readline().strip("\n")
            if sentence != "***":
                break
        sentence = file.readline().strip('\n')
        if sentence:
            temp = sentence.split(' | ')
            utility.list = temp[1].strip(' ').split(' ')
            sentence_nums = int(math.pow(2, len(utility.list)))

            for i in xrange(sentence_nums):
                sentence = file.readline().strip('\n')
                temp = sentence.split(' ')
                sign = temp[1:]
                new_tuple = ()
                for ele in sign:
                    new_tuple += (ele,)
                utility.table[new_tuple] = temp[0]
    file.close()

def sentence_to_query(sentence):
    query = Query()
    if sentence[0] == 'P':
        type = 'P'
        index = 2
    elif sentence[0] == 'E':
        type = 'EU'
        index = 3
    else:
        type = 'MEU'
        index = 4
    query.type = type

    if '|' in sentence:
        query.has_parent = True
    else:
        query.has_parent = False

    temp = sentence[index: len(sentence) - 1]
    if query.has_parent == False:
        k = temp.split(', ')
        for m in k:
            new_tuple = to_tuple(m)
            query.right_part.append(new_tuple)
    else:
        q = temp.split(' | ')
        l = q[0].split(', ')
        for m in l:
            new_tuple = to_tuple(m)
            query.left_part.append(new_tuple)

        r = q[1].split(', ')
        for m in r:
            new_tuple = to_tuple(m)
            query.right_part.append(new_tuple)
    return query

def to_tuple(k):
    array = k.split(" = ")
    if len(array) == 1:
        new_name = array[0]
        new_sign = "?"
    else:
        new_name = array[0]
        new_sign = array[1]

    new_tuple = (new_sign, new_name)
    return new_tuple

def sentence_to_event(sentence):
    event = Event()
    if "|" in sentence:
        event.has_parent = True
    else:
        event.has_parent = False

    if event.has_parent:
        k = sentence.strip(" ").split(" | ")
        event.name = k[0]
        parent = k[1]
        event.parent_list = parent.split(" ")
        return event
    else:
        k = sentence.strip(" ").split(" ")
        event.name = k[0]
        return event

def sentence_to_prob(event, sentence):
    temp = sentence.split(" ")
    if len(temp) == 1:
        event.positive = float(temp[0])
        event.negative = 1 - float(temp[0])
    else:
        key = ()
        for sign in temp[1:]:
            key = key + (sign,)
        event.prob[key] = float(temp[0])



def create_event_dict():
    for event in event_list:
        event_dict[event.name] = event










def alg():
    global query_type
    for index, query in enumerate(query_list):
        if query.type == "P":
            query_type = "P"
            alg_P(query)
        if query.type == "EU":
            query_type = "EU"
            alg_EU(query)
        if query.type == "MEU":
            query_type = "MEU"
            alg_MEU(query)

    for index, ele in enumerate(output):
        sys.stdout.write(str(ele))
        if index < len(output) - 1:
            print

def alg_P(query):
    result = 0
    Q  = {}
    E  = {}
    Y  = {}
    BN = {}

    Q_init(query, Q)
    E_init(query, E)
    Y_init(query, Q, E, Y)
    BN_init(query, Q, E, Y, BN)

    BN2 = []
    BN2_init(BN, BN2)
    new_BN = copy.deepcopy(BN)
    m_pos =  compute(Q, E, Y, BN, BN2)
    result = m_pos
    BN = new_BN

    if len(Q) != 0:
        for ele in Q:
            origin = BN[ele]
            if origin == '+':
                BN[ele] = '-'
            elif origin == '-':
                BN[ele] = '+'
            BN2 = []
            BN2_init(BN, BN2)
            neg = compute(Q, E, Y, BN, BN2)
            BN[ele] = origin

            result = normal(m_pos, neg)
    output.append(str("%.2f" %result))
    return result


def Q_init(query, Q):
    if len(query.left_part) != 0:
        for ele in query.left_part:
            Q[ele[1]] = ele[0]

def E_init(query, E):
    if len(query.right_part) != 0:
        for ele in query.right_part:
            E[ele[1]] = ele[0]

def Y_init(query, Q, E, Y):

    for ele in Q:
        if event_dict[ele].has_parent == True:
            for p in event_dict[ele].parent_list:
                if p not in Q and p not in E:
                    Y[p] = '?'
    for ele in E:
        if event_dict[ele].has_parent == True:
            for p in event_dict[ele].parent_list:
                if p not in Q and p not in E:
                    Y[p] = '?'
    Y2 = copy.deepcopy(Y)
    for ele in Y2:
        if event_dict[ele].has_parent == True:
            for p in event_dict[ele].parent_list:
                if p not in Q and p not in E and p not in Y:
                    Y[p] = '?'

def BN_init(query, Q, E, Y, BN):

    for ele in Q:
        if ele not in BN:
            BN[ele] = Q[ele]

    for ele in E:
        if ele not in BN:
            BN[ele] = E[ele]

    for ele in Y:
        if ele not in BN:
            BN[ele] = Y[ele]

def BN2_init(BN, BN2):
    for ele in BN:
        new_tuple = (ele, BN[ele])
        BN2.append(new_tuple)

def compute(Q, E, Y, BN, BN2):
    if len(BN2) == 0:
        return 1.0

    first_event = BN2[0]
    first_event_name = first_event[0]
    sign = BN[first_event_name]
    sign_comb = ()

    if event_dict[first_event_name].has_parent:
        new_tuple = (first_event_name, sign)
        combi, modi = has_parent(new_tuple, BN)

        sum = 0
        for idx, item in enumerate(combi):
            m  = modi[idx]
            c = combi[idx]

            BN_copy = copy.deepcopy(BN)
            for ele in m:
                BN[ele] = m[ele]

            prob = event_dict[first_event_name].prob[c]

            if sign == '+':
                sum += prob * compute(Q, E, Y, BN, BN2[1:])
            elif sign == '-':
                sum += (1 - prob) * compute(Q, E, Y, BN, BN2[1:])
            else:
                ori = BN[first_event_name]
                BN[first_event_name] = '+'
                sum1 =  prob * compute(Q, E, Y, BN, BN2[1:])
                BN[first_event_name] = '-'
                sum2 = (1 - prob) * compute(Q, E, Y, BN, BN2[1:])
                BN[first_event_name] = ori
                sum += (sum1 + sum2)

            BN = BN_copy
        return sum
    else:
        tuple_list = has_no_parent((first_event_name, sign))
        sum = 0
        for t in tuple_list:
            new_subst = t[0]
            prob = t[1]
            BN_copy = copy.deepcopy(BN)
            for ele in new_subst:
                BN[ele] = new_subst[ele]
            sum += prob * compute(Q, E, Y, BN, BN2[1:])
            BN = BN_copy
        return sum

def has_no_parent(new_tuple):
    name = new_tuple[0]
    sign = new_tuple[1]
    result = []
    if sign == '+':
        dict = {}
        dict[name] = '+'
        result.append((dict, event_dict[name].positive))
    elif sign == '-':
        dict = {}
        dict[name] = '-'
        result.append((dict, event_dict[name].negative))
    else:
        new_dict = {}
        new_dict[name] = '+'
        result.append((new_dict, event_dict[name].positive))
        new_dict2 = {}
        new_dict2[name] = '-'
        result.append((new_dict2, event_dict[name].negative))
    return result


def has_parent(new_tuple, BN):
    name = new_tuple[0]
    sign = new_tuple[1]
    parent_list = event_dict[name].parent_list
    sign_list = []
    new_tuple2 = ()
    sign_list.append(new_tuple2)

    sign_list_mod = []
    dict  = {}
    sign_list_mod.append(dict)

    for p_name in parent_list:
        parent_sign = BN[p_name]
        if parent_sign != '?':
            for index, ele in enumerate(sign_list):
                sign_list[index] += (parent_sign,)

        else:
            list_copy = copy.deepcopy(sign_list)
            for index, ele in enumerate(sign_list):
                sign_list[index] += ('+',)
            for index, ele in enumerate(list_copy):
                list_copy[index] += ('-',)
            sign_list.extend(list_copy)

            copy_list2 = copy.deepcopy(sign_list_mod)
            for index, ele in enumerate(sign_list_mod):
                sign_list_mod[index][p_name] = '+'
            for index, ele in enumerate(copy_list2):
                copy_list2[index][p_name] = '-'
            sign_list_mod.extend(copy_list2)

    return sign_list, sign_list_mod




def normal(prob1, prob2):
    return float(prob1 / (prob1 + prob2))











def EU_init_Q(query, Q):
    if query.type == 'EU':
        for item in utility.list:
            Q[item] = '?'


def EU_init_E(query, Q, E):
    if query.type == 'EU':
        for tuple in query.left_part:
            E[tuple[1]] = tuple[0]
        for tuple in query.right_part:
            E[tuple[1]] = tuple[0]
    for item in E:
        if item in Q and Q[item] == '?':
            Q[item] = E[item]


def EU_init_Y(query, Q, E, Y):
    for item in Q:
        if event_dict[item].has_parent == True:
            for parent in event_dict[item].parent_list:
                if parent not in Q and parent not in E:
                    Y[parent] = '?'
    for item in E:
        if event_dict[item].has_parent == True:
            for parent in event_dict[item].parent_list:
                if parent not in Q and parent not in E:
                    Y[parent] = '?'
    copy_Y = copy.deepcopy(Y)
    for item in copy_Y:
        if event_dict[item].has_parent == True:
            for parent in event_dict[item].parent_list:
                if parent not in Q and parent not in E and parent not in Y:
                    Y[parent] = '?'


def EU_init_BN(query, Q, E, Y, BN):
    BN_init(query, Q, E, Y, BN)


def compute_utility(mid_list):
    prob_sum = 0
    utility_sum = 0

    for tuple in mid_list:
        prob_sum += tuple[0]

    for tuple in mid_list:
        utility_sum += tuple[0] / prob_sum * tuple[1]

    return utility_sum


def alg_EU(query):
    Q  = {}
    E  = {}
    Y  = {}
    BN = {}
    EU_init_Q(query, Q)
    EU_init_E(query, Q, E)
    EU_init_Y(query, Q, E, Y)
    EU_init_BN(query, Q, E, Y, BN)

    BN2 = []
    BN2_init(BN, BN2)
    new_BN = copy.deepcopy(BN)

    subst_list = []
    list = utility.list
    table = utility.table
    event_num = len(list)

    for s_tuple in table:
        flag = False
        value = table[s_tuple]
        dict = {}
        for i in xrange(event_num):
            if BN[list[i]] != '?' and BN[list[i]] != s_tuple[i]:
                    flag = True
                    break
            else:
                dict[list[i]] = s_tuple[i]
        if flag == True:
            continue
        subst_list.append((dict, value))


    sum = 0
    mm_list = []
    for subst in subst_list:
        modify_dict = subst[0]
        value = float(subst[1])
        BN = copy.deepcopy(new_BN)
        for item in modify_dict:
            BN[item] = modify_dict[item]
        prob = compute(Q, E, Y, BN, BN2)
        mm_list.append((prob, value))

    BN = copy.deepcopy(new_BN)
    sum = compute_utility(mm_list)

    if query_type == 'EU':
        output.append(int(round(sum)))
    return sum



def alg_MEU(query):
    max_value = -100000
    new_query = copy.deepcopy(query)
    best = ()

    num = len(dec_list)
    origin = []
    dict = {}
    origin.append(dict)

    for index, ele in enumerate(dec_list):
        copy_d = copy.deepcopy(origin)
        for m in origin:
            m[ele.name] = "+"
        for n in copy_d:
            n[ele.name] = "-"
        origin.extend(copy_d)

    for dec in origin:
        query = copy.deepcopy(new_query)

        query.type = 'EU'
        c_l = []
        for ele in query.left_part:
            name = ele[1]
            if name in dec:
                c_l.append((dec[name], name))
            else:
                c_l.append(ele)
        query.left_part = c_l

        c_r = []
        for tuple in query.right_part:
            name = tuple[1]
            if name in dec:
                c_r.append((dec[name], name))
            else:
                c_r.append(tuple)

        query.right_part = c_r

        value = alg_EU(query)

        if value > max_value:
            best = (dec, value)
            max_value = value

    res = []
    for ele in new_query.left_part:
        name = ele[1]
        if ele[0] == '?':
            res.append(best[0][name])
    for ele in new_query.right_part:
        name = ele[1]
        if ele[0] == '?':
            res.append(best[0][name])
    res.append(int(round(best[1])))
    result = ''

    for index,ele in enumerate(res):
        result += str(ele)
        if index != len(res) - 1:
            result += ' '

    output.append(result)



def run():
    filename = sys.argv[-1]
    # filename = "sample02.txt"
    read(filename)
    create_event_dict()
    alg()
    with open('output.txt', 'w') as file:
        for index, ele in enumerate(output):
            file.write(str(ele))
            if index < len(output) - 1:
                file.write('\n')
    file.close()

run()

