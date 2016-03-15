import sys
# a single atomic sentence is always a fact with no variable.
class atom(object):
    predicate = ""
    argument_list = []

    def __init__(self, predicate, argument_list):
        self.predicate = predicate
        self.argument_list = argument_list

    def toString(self):
        str = ""
        str += self.predicate
        str += "("
        for ele in self.argument_list:
            # str += ele
            if ele[0].islower():
                str += "_"
            else:
                str += ele
            str += ", "
        str = str[:-2]
        str += ")"
        return str

    def isFact(self):
        for ele in self.argument_list:
            if ele[0].islower():
                return False
        return True



class implication(object):
    lhs = []
    rhs = atom("", [])

    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def toString(self):
        str = ""
        for ele in self.lhs:
            str += ele.toString()
            str += " && "
        str = str[:-4]
        str += " => "
        str += self.rhs.toString()
        return str


class file(object):
    # read the file and store the data
    def readfile(self, filename):
        f = open(filename)
        query_temp = f.readline()
        query_temp = query_temp[0:-1]
        if "&&" in query_temp:
            query = []
            atom_list = query_temp.split(" && ")
            for ele in atom_list:
                pos = ele.find("(")
                predicate  = ele[:pos]
                arguments = ele[pos+1:-1]
                argument_list = arguments.split(", ")
                atom_ele = atom(predicate, argument_list)
                query.append(atom_ele)
        else:
            pos = query_temp.find("(")
            predicate  = query_temp[:pos]
            arguments = query_temp[pos+1:-1]
            argument_list = arguments.split(", ")
            query = atom(predicate, argument_list)
        # print query.predicate, query.argument_list

        clause_num = int(f.readline())

        fact_list = []
        implication_list = []
        for i in range(clause_num):
            clause = f.readline()
            clause = clause[0:-1]
            if clause.find("=>") == -1:
                pos = clause.find("(")
                predicate  = clause[:pos]
                arguments = clause[pos+1:-1]
                argument_list = arguments.split(", ")
                new_atom = atom(predicate, argument_list)
                fact_list.append(new_atom)
            else:
                lhs_list = []
                implication_temp = clause.split(" => ")
                lhs = implication_temp[0]
                rhs = implication_temp[1]
                lhs_list_temp = lhs.split(" && ")
                for ele in lhs_list_temp:
                    pos = ele.find("(")
                    predicate  = ele[:pos]
                    arguments = ele[pos+1:-1]
                    argument_list = arguments.split(", ")
                    new_atom = atom(predicate, argument_list)
                    lhs_list.append(new_atom)
                pos = rhs.find("(")
                predicate  = rhs[:pos]
                arguments = rhs[pos+1:-1]
                argument_list = arguments.split(", ")
                rhs_standard = atom(predicate, argument_list)
                implication_standard = implication(lhs_list, rhs_standard)
                implication_list.append(implication_standard)

        alg = algorithm()
        result = []
        if type(query) == atom:
            alg.FOL_BC_ASK(fact_list, implication_list, query, result)
        if type(query) == list:
            for i in range(len(query)):
                alg.FOL_BC_ASK(fact_list, implication_list, query[i], result)
                if result[-1] == "False":
                    continue
                if result[-1] == "True" and i != len(query)-1:
                    result.pop()
        return result



class algorithm(object):
    # def STANDARDIZE_VARIABLES(self, implication_old):
    #     new_lhs = list()
    #     new_rhs = atom(implication_old.rhs.predicate, implication_old.rhs.argument_list[:])
    #     for atom_ele in implication_old.lhs:
    #         atom_temp = atom(atom_ele.predicate, atom_ele.argument_list[:])
    #         new_lhs.append(atom_temp)
    #     for ele in new_lhs:
    #         for i in range(len(ele.argument_list)):
    #             if len(ele.argument_list[i]) == 1 and ele.argument_list[i].islower:
    #                 temp = ele.argument_list[i]
    #                 ele.argument_list[i] = temp + "1"
    #                 for j in range(len(new_rhs.argument_list)):
    #                     if new_rhs.argument_list[j] == temp:
    #                         new_rhs.argument_list[j] = temp + "1"
    #                 if i == len(ele.argument_list)-1:
    #                     continue
    #                 for k in new_lhs:
    #                     for n in range(len(k.argument_list)):
    #                         if k.argument_list[n] == temp:
    #                             k.argument_list[n] == temp + "1"
    #     for p in range(len(new_rhs.argument_list)):
    #         if len(new_rhs.argument_list[p]) == 1 and new_rhs.argument_list[p].islower:
    #             temp = new_rhs.argument_list[p]
    #             new_rhs.argument_list[p] = temp + "1"
    #     new_imp = implication(new_lhs, new_rhs)
    #     return new_imp



    def STANDARDIZE_VARIABLES(self, implication_old, goal):
        new_lhs = list()
        new_rhs = atom(implication_old.rhs.predicate, implication_old.rhs.argument_list[:])
        for atom_ele in implication_old.lhs:
            atom_temp = atom(atom_ele.predicate, atom_ele.argument_list[:])
            new_lhs.append(atom_temp)
        for argu in goal.argument_list:
            if argu[0].islower():
                for ele in new_lhs:
                    for m in range(len(ele.argument_list)):
                        if ele.argument_list[m] == argu:
                            ele.argument_list[m] = argu + "1"
                for n in range(len(new_rhs.argument_list)):
                    if new_rhs.argument_list[n] == argu:
                        new_rhs.argument_list[n] = argu + "1"
        new_imp = implication(new_lhs, new_rhs)
        return new_imp





    def FOL_BC_ASK(self, fact_list, implication_list, query, result):
        result.append("Ask: " + query.toString() + "\n")
        print "Ask: " + query.toString()
        substitution = {}
        temp = 0
        if query.isFact():
            for fact in fact_list:
                if query.predicate == fact.predicate and len(query.argument_list) == len(fact.argument_list):
                    all_correct = 1
                    for i in range(len(query.argument_list)):
                        if query.argument_list[i] != fact.argument_list[i]:
                            all_correct = 0
                            break
                    if all_correct == 1:
                        temp = 1
                        result.append("True: " + fact.toString() + "\n")
                        result.append("True")
                        print "True: " + fact.toString()
                        print "True"
                        return
        else:
            substitution_list = []
            for fact in fact_list:
                substitution_k = self.UNIFY(fact, query, {})
                if substitution_k != False and substitution_k != None:
                    substitution_list.append(substitution_k)
                    temp = 1
            if len(substitution_list) == 1:
                query_new = self.SUBST(query, substitution_list[0])
                result.append("True: " + query_new.toString() + "\n")
                result.append("True")
                print "True: " + query_new.toString()
                print "True"
                return substitution_list[0]
            if len(substitution_list) > 1:
                print "if you visit this function, congratulation, it's wrong!"
                return substitution_list
        if temp == 0:
            new_substitution = self.FOL_BC_OR(fact_list, implication_list, query, substitution, result)
            if type(new_substitution) == bool and new_substitution == False:
                result.append("False: " + query.toString() + "\n")
                result.append("False")
                print "False: " + query.toString()
                print "False"
                return False
            else:
                first_goal = self.SUBST(query, new_substitution)
                result.append("True: " + first_goal.toString() + "\n")
                result.append("True")
                print "True: " + first_goal.toString()
                print "True"

    def FOL_BC_OR(self, fact_list, implication_list, goal, substitution, result):
        temp = 0
        num = 0
        for implication in implication_list:
            # print implication.toString()
            new_implication = self.STANDARDIZE_VARIABLES(implication, goal)
            # print new_implication.toString()
            new_substitution = self.UNIFY(new_implication.rhs, goal, {})

            if new_substitution != False:
                # print new_substitution
                # print new_substitution
                # for key in new_substitution.keys():
                #     if key not in goal.argument_list and new_substitution[key] not in goal.argument_list:
                #         new_substitution.pop(key)
                # print new_substitution
                # find one
                temp = 1
                num += 1
                if num > 1:
                    result.append("Ask: " + goal.toString() + "\n")
                    print "Ask: " + goal.toString()
                # for key in new_substitution.keys():
                #     if key not in substitution:
                #         substitution[key] = new_substitution[key]

                for num in range(len(new_implication.lhs)):
                    new_implication.lhs[num] = self.SUBST(new_implication.lhs[num], new_substitution)
                new_implication.rhs = self.SUBST(new_implication.rhs, new_substitution)

                # print implication.toString()
                new_substitution =  self.FOL_BC_AND(fact_list, implication_list, new_implication.lhs, new_substitution, result)

                if type(new_substitution) == bool and new_substitution == False:
                    temp = 0
                    num = num + 1
                    continue
                elif type(new_substitution) == dict:
                # if new_substitution != False and new_substitution != None:
                    for key in new_substitution.keys():
                        substitution[key] = new_substitution[key]
                    return substitution
                elif type(new_substitution) == list:
                    print "TTTTTTTTTT"
                    substitution_list = []
                    for ele in new_substitution:
                        substitution_k = {}
                        for q in substitution.keys():
                            substitution_k[q] = substitution[q]
                        for key in ele.keys():
                            substitution_k[key] = ele[key]
                        substitution_list.append(substitution_k)
                    return substitution_list
        if temp == 0:
            # print "UUU"
            return False
        else:
            # print substitution
            return substitution


    def FOL_BC_AND(self, fact_list, implication_list, goals, substitution, result):
        if substitution == False:
            return False
        elif len(goals) == 0:
            return substitution
        else:
            first_goal_temp = goals[0]
            rest_goal = goals[1:]
            first_goal =  self.SUBST(first_goal_temp, substitution)
            # print first_goal.toString()
            # print substitution
            result.append("Ask: " + first_goal.toString() + "\n")
            print "Ask: " + first_goal.toString()
            if first_goal.isFact():
                temp = 1
                for fact in fact_list:
                    if fact.predicate == first_goal.predicate and first_goal.argument_list == fact.argument_list:
                        temp = 0
                        result.append("True: " + first_goal.toString() + "\n")
                        print "True: " + first_goal.toString()
                        a = self.FOL_BC_AND(fact_list, implication_list, rest_goal, substitution, result)
                        if type(a) == bool and a == False:
                            # print "QQQ", first_goal.toString()
                            return False
                        else:
                            return a
                if temp == 1:
                    # print "AAA"
                    # print first_goal.toString()
                    # print substitution
                    k = self.FOL_BC_OR(fact_list, implication_list, first_goal, {}, result)
                    if type(k) == bool and k == False:
                        result.append("False: " + first_goal.toString() + "\n")
                        print "False: " + first_goal.toString()
                        # print "TTT", first_goal.toString()
                        return False
                    else:
                        result.append("True: " + first_goal.toString() + "\n")
                        print "True: " + first_goal.toString()
                        return self.FOL_BC_AND(fact_list, implication_list, rest_goal, substitution, result)
            else:
                temp = 1
                correct_substition_list = []
                for fact in fact_list:
                    new_substitution = self.UNIFY(fact, first_goal, {})
                    if new_substitution != False and new_substitution != None:
                        correct_substition_list.append(new_substitution)
                # print len(correct_substition_list)
                if len(correct_substition_list) == 1:
                    new_substitution = correct_substition_list[0]
                    if new_substitution != False and new_substitution != None:
                        fact_new = self.SUBST(first_goal, new_substitution)
                        result.append("True: " + fact_new.toString() + "\n")
                        print "True: " + fact_new.toString()
                        temp = 0
                        substitution = new_substitution
                        m = self.FOL_BC_AND(fact_list, implication_list, rest_goal, substitution, result)
                        # print m
                        if type(m) == bool and m == False:
                            temp = 1
                            # print "BBB1"
                        else:
                            # print "BBB2"
                            return m
                if len(correct_substition_list) > 1:
                    print "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"
                    return_list = []
                    num = 0
                    for substitution_t in correct_substition_list:
                        fact_new = self.SUBST(first_goal, substitution_t)
                        if num != 0:
                            result.append("ASK: " + first_goal.toString() + "\n")
                            print "ASK: " + first_goal.toString()
                        result.append("True: " + fact_new.toString() + "\n")
                        print "True: " + fact_new.toString()
                        substitution = substitution_t
                        return_sub = self.FOL_BC_AND(fact_list, implication_list, rest_goal, substitution, result)
                        return_list.append(return_sub)
                        num += 1
                    return return_list

                else:
                    k = self.FOL_BC_OR(fact_list, implication_list, first_goal, {}, result)
                    if type(k) == bool and k == False:
                        result.append("False: " + first_goal.toString() + "\n")
                        print "False: " + first_goal.toString()
                        return False
                    elif type(k) == dict:
                        for ele in k.keys():
                            if ele not in substitution.keys():
                                substitution[ele] = k[ele]
                        first_goal_k = atom(first_goal.predicate, first_goal.argument_list[:])
                        first_goal = self.SUBST(first_goal, substitution)
                        result.append("True: " + first_goal.toString() + "\n")
                        print "True: " + first_goal.toString()
                        n = self.FOL_BC_AND(fact_list, implication_list, rest_goal, substitution, result)

                        if type(n) == bool and n == False:
                            # print "AAA", first_goal_k.toString()
                            # rest_goal.insert(0, firt_goal_k)
                            # return self.FOL_BC_AND(fact_list, implication_list, rest_goal, substitution)
                            return False

                        else:
                            return n
                    elif type(k) == list:
                        substitution_list = []
                        goal_p = atom(first_goal.predicate, first_goal.argument_list[:])
                        pos_list = []
                        pos_list.append(len(result))
                        for substitution_k in k:
                            print "RRRRRRRRRRR"
                            goal_p = atom(first_goal.predicate, first_goal.argument_list[:])
                            substitution_temp = {}
                            for ele in substitution:
                                substitution_temp[ele] = substitution[ele]
                            for ele in substitution_k.keys():
                                if ele not in substitution_temp.keys():
                                    substitution_temp[ele] = substitution_k[ele]
                            goal_p = self.SUBST(goal_p, substitution_temp)
                            result.append("True: " + goal_p.toString() + "\n")
                            print "True: " + goal_p.toString()

                            n = self.FOL_BC_AND(fact_list, implication_list, rest_goal, substitution_temp, result)
                            pos_list.append(len(result))
                            if type(n) == bool and n == False:
                                continue
                            else:
                                substitution_list.append(n)
                                return n
                        if len(substitution_list) == 0:
                            if len(k) == 2:
                                temp1 = result[pos_list[0]-4:pos_list[0]-2]
                                temp2 = result[pos_list[0]-2:pos_list[0]]

                                tt1 = result[pos_list[0]:pos_list[1]]
                                tt2 = result[pos_list[1]:pos_list[2]]

                                new_result = result[:pos_list[0]-2]
                                for i in tt1:
                                    new_result.append(i)
                                for i in temp2:
                                    new_result.append(i)
                                for i in tt2:
                                    new_result.append(i)
                                print new_result
                                result[:] = new_result[:]

                            if len(k) == 3:
                                temp1 = result[pos_list[0]-6:pos_list[0]-4]
                                temp2 = result[pos_list[0]-4:pos_list[0]-2]
                                temp3 = result[pos_list[0]-2:pos_list[0]]
                                print temp1

                                tt1 = result[pos_list[0]:pos_list[1]]
                                tt2 = result[pos_list[1]:pos_list[2]]
                                tt3 = result[pos_list[2]:pos_list[3]]
                                print tt1
                                print tt2
                                print tt3

                                new_result = result[:pos_list[0]-4]
                                for i in tt1:
                                    new_result.append(i)
                                for i in temp2:
                                    new_result.append(i)
                                for i in tt2:
                                    new_result.append(i)
                                for i in temp3:
                                    new_result.append(i)
                                for i in tt3:
                                    new_result.append(i)
                                print new_result
                                result[:] = new_result[:]
                            return False
                        else:
                            return substitution_list[0]



    def SUBST(self, atom_old, substitution):
        atom_new = atom(atom_old.predicate, atom_old.argument_list[:])
        if substitution is None:
            return atom_new
        else:
            for var in substitution.keys():
                for k in range(len(atom_new.argument_list)):
                    if var == atom_new.argument_list[k]:
                        atom_new.argument_list[k] = substitution[var]
                # if var in atom_new.argument_list:
                #     atom_new.argument_list[atom_new.argument_list.index(var)] = substitution[var]
            return atom_new


    def UNIFY(self, x, y, substitution):
        if substitution == False:
            return False
        elif x == y:
            return substitution
        elif type(x) == str and x[0].islower():
            return self.UNIFY_VAR(x, y, substitution)
        elif type(y) == str and y[0].islower():
            return self.UNIFY_VAR(y, x, substitution)
        elif type(x) == atom and type(y) == atom:
            return self.UNIFY(x.argument_list, y.argument_list, self.UNIFY(x.predicate, y.predicate, substitution))
        elif type(x) == list and type(y) == list:
                return self.UNIFY(x[1:], y[1:], self.UNIFY(x[0], y[0], substitution))
        else:
            return False

    def UNIFY_VAR(self, var, x, substitution):
        if substitution.get(var) != None:
            return self.UNIFY(substitution.get(var), x, substitution)
        elif substitution.get(x) != None:
            return self.UNIFY(var, substitution.get(x), substitution)
        else:
            substitution[var] = x
            return substitution



if __name__ == '__main__':
    newFile = file()
    filename = sys.argv[-1]
    # filename = "sample05.txt"
    result = newFile.readfile(filename)
    print result


    output = open("output.txt", "w")
    str_line = ""
    for n in range(len(result)):
        str_line += result[n]
    output.write(str_line)

    # alg = algorithm()
    # lhs = list()
    # ele1 = atom("AAA", ["x", "y"])
    # ele2 = atom("BBB", ["x", "TTT"])
    # lhs.append(ele1)
    # lhs.append(ele2)
    # rhs = atom("CCC", ["y"])
    # goal = atom ("CCC", ["x"])
    # imp = implication(lhs, rhs)
    # print imp.toString()
    #
    # new_imp = alg.STANDARDIZE_VARIABLES(imp, goal)
    # print new_imp.toString()