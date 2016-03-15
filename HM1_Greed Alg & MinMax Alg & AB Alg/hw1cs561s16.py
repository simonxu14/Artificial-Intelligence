import sys

class gridNode(object):

    num = 0
    holder = 0
    row = 0
    column = 0
    depth = 0
    earn = 0
    alpha = 0
    beta = 0

    list = []

    def __init__(self, num):
        self.num = num
        self.holder = 0
        self.row = 0
        self.column = 0
        self.earn = 0
        self.depth = 0
        self.alpha = 0
        self.beta = 0
        self.list = []

    def nodetostring(self):
        result = ""
        if self.depth == 0:
            result += "root,0,"
            if self.earn == 10000:
                result += "Infinity"
            elif self.earn == -10000:
                result += "-Infinity"
            else:
                result += str(self.earn)
            result += "\n"
            return result
        result += self.getNodeColumn()
        result += str(self.getNodeRow())
        result += ","
        result += str(self.depth)
        result += ","
        if self.earn == 10000:
            result += "Infinity"
        elif self.earn == "-10000":
            result += "-Infinity"
        else:
            result += str(self.earn)
        result += "\n"
        return result

    def nodetostring2(self):
        result = ""
        if self.depth == 0:
            result += "root,0,"
            if self.earn == 10000:
                result += "Infinity"
            elif self.earn == -10000:
                result += "-Infinity"
            else:
                result += str(self.earn)

            result += ","
            if self.alpha == 10000:
                result += "Infinity"
            elif self.alpha == -10000:
                result += "-Infinity"
            else:
                result += str(self.alpha)

            result += ","
            if self.beta == 10000:
                result += "Infinity"
            elif self.beta == -10000:
                result += "-Infinity"
            else:
                result += str(self.beta)

            result += "\n"
            return result
        result += self.getNodeColumn()
        result += str(self.getNodeRow())
        result += ","
        result += str(self.depth)
        result += ","
        if self.earn == 10000:
            result += "Infinity"
        elif self.earn == -10000:
            result += "-Infinity"
        else:
            result += str(self.earn)

        result += ","
        if self.alpha == 10000:
            result += "Infinity"
        elif self.alpha == -10000:
            result += "-Infinity"
        else:
            result += str(self.alpha)

        result += ","
        if self.beta == 10000:
            result += "Infinity"
        elif self.beta == -10000:
            result += "-Infinity"
        else:
            result += str(self.beta)

        result += "\n"
        return result


    def getNodeColumn(self):
        if self.column == 0:
            return "A"
        elif self.column == 1:
            return "B"
        elif self.column == 2:
            return "C"
        elif self.column == 3:
            return "D"
        else:
            return "E"

    def getNodeRow(self):
        return self.row + 1


    # return the position of this node ex. A1
    def getNodePosition(self):
        string = ""
        if self.column == 0:
            string += "A"
        elif self.column == 1:
            string += "B"
        elif self.column == 2:
            string += "C"
        elif self.column == 3:
            string += "D"
        else:
            string += "E"
        string += str(self.row + 1)
        return string

    # check if this node has upper node
    def hasUp(self):
        if self.row == 0:
            return False
        else:
            return True

    # check if this node has lower node
    def hasDown(self):
        if self.row == 4:
            return False
        else:
            return True

    # check if this node has left node
    def hasLeft(self):
        if self.column == 0:
            return False
        else:
            return True

    # check if this node has right node
    def hasRight(self):
        if self.column == 4:
            return False
        else:
            return True


# grid is the object of the 5*5 grid
class grid(list):

    # return the list of neighbor nodes
    def neighbor(self, node):
        list = []
        if node.hasUp():
            list.append(self[node.row-1][node.column])
        if node.hasDown():
            list.append(self[node.row+1][node.column])
        if node.hasLeft():
            list.append(self[node.row][node.column-1])
        if node.hasRight():
            list.append(self[node.row][node.column+1])
        return list

    # check if there is a node have the target holder in the list of neighbor nodes
    def hasNeighborHolder(self, node, holder):
        list = self.neighbor(node)
        for node in list:
            if node.holder == holder:
                return True
        return False

    def checkgrid(self):
        for i in range(len(self)):
            for j in range(len(self[0])):
                if self[i][j].holder == 0:
                    return True




class file(object):

    # read the file and store the data
    def readfile(self, filename):
        f = open(filename)

        task = int(f.readline())

        line = f.readline()
        if 'X' in line:
            player = 1
        else:
            player = 2

        depth = int(f.readline())

        if task == 4:
            alg = depth
            depth = int(f.readline())

            line = f.readline()
            if 'X' in line:
                player2 = 1
            else:
                player2 = 2

            alg2 = int(f.readline())
            depth2 = int(f.readline())

            line = f.readline()
            newGrid = grid()

            for i in range(5):
                line_list = line.split(" ")
                grid_line = []
                for j in range(len(line_list)):
                    node = gridNode(int(line_list[j]))
                    node.column = j
                    node.row = i
                    grid_line.append(node)
                newGrid.append(grid_line)
                line = f.readline()

            for m in range(5):
                for n in range(5):
                    if line[n] == '*':
                        newGrid[m][n].holder = 0
                    if line[n] == 'X':
                        newGrid[m][n].holder = 1
                    if line[n] == 'O':
                        newGrid[m][n].holder = 2
                line = f.readline()
            f.close()
            return [task, player, alg, depth, player2, alg2, depth2, newGrid]

        line = f.readline()
        newGrid = grid()

        for i in range(5):
            line_list = line.split(" ")
            grid_line = []
            for j in range(len(line_list)):
                node = gridNode(int(line_list[j]))
                node.column = j
                node.row = i
                grid_line.append(node)
            newGrid.append(grid_line)
            line = f.readline()

        for m in range(5):
            for n in range(5):
                if line[n] == '*':
                    newGrid[m][n].holder = 0
                if line[n] == 'X':
                    newGrid[m][n].holder = 1
                if line[n] == 'O':
                    newGrid[m][n].holder = 2
            line = f.readline()

        f.close()
        return [task, player, depth, newGrid]

    def writefile(self, newGrid):
        output = open("next_state.txt", "w")
        for m in range(5):
            str_line = ""
            for n in range(5):
                if newGrid[m][n].holder == 1:
                    str_line += 'X'
                elif newGrid[m][n].holder == 2:
                    str_line += 'O'
                else:
                    str_line += '*'
            str_line += "\n"
            output.write(str_line)

    def writefileMiniMax(self, result):
        output = open("traverse_log.txt", "w")
        output.write(result)

    def writefileState(self, result):
        output = open("trace_state.txt", "w")
        output.write(result)



class greedy(object):

    # the main search part
    def search(self, grid, player):

        # max: the max we can get
        # max_row & max column: the position we find max
        max = 0
        max_row = 0
        max_column = 0
        temp = 0

        # find the max in grid
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j].holder == 0:
                    temp = self.check(grid[i][j], grid, player)
                    if temp > max:
                        max = temp
                        max_row = i
                        max_column = j

        # return the position of the max we just found
        return [max_row,max_column]

    # check each node and find the movement(raid or sneak) we use to go there
    def check(self, node, grid, player):

        if grid.hasNeighborHolder(node, player):
            return self.raid(node, grid, player)
        else:
            return self.sneak(node)

    # we raid to this point and return the total value we can earn if we raid to this point
    def raid(self, node, grid, player):
        value = node.num
        if grid.hasNeighborHolder(node, self.changeplayer(player)):
            list = grid.neighbor(node)
            for node_check in list:
                if node_check.holder == self.changeplayer(player):
                    value += node_check.num
        return value

    # we sneak to this point and return the value we can earn if we sneak to this point
    def sneak(self, node):
        return node.num

    def changeplayer(self, player):
        if player == 1:
            return 2
        else:
            return 1





class miniMax(object):

    # the main search part
    def search(self, player, depth, grid):

        # total1 = 0
        # total2 = 0
        #
        # for i in range(len(grid)):
        #     for j in range(len(grid[0])):
        #         if grid[i][j].holder == 1:
        #             total1 += grid[i][j].num
        #         if grid[i][j].holder == 2:
        #             total2 += grid[i][j].num

        # max: the max we can get
        # max_row & max column: the position we find max
        max = 0
        max_row = 0
        max_column = 0
        temp = 0

        root = gridNode(-1)
        root.row = -1
        root.column = -1
        root.holder = -1
        root.depth = 0
        root.earn = -10000

        result = ""
        result += "Node,Depth,Value"
        result += "\n"
        result = self.recursive_search(grid, root, player, depth, result)
        newfile = file()
        newfile.writefileMiniMax(result)


        # find the max in grid
        max_row = 0
        max_column = 0
        max = -10000
        for node in root.list:
            if node.earn > max:
                max_row = node.row
                max_column = node.column
                max = node.earn

        # return the position of the max we just found
        return [max_row,max_column]



    def recursive_search(self, grid, root, player, count, result):
        temp = root.nodetostring()
        # if temp.find("10000"):
        #     temp.replace("10000", "Infinity")
        result += temp
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j].holder == 0:
                    new_node = gridNode(grid[i][j].num)
                    new_node.holder = player
                    new_node.row = grid[i][j].row
                    new_node.column = grid[i][j].column
                    new_node.depth = root.depth + 1
                    new_node.list = []
                    # new_node.earn = self.total(grid, player) + self.check(new_node, grid, player)

                    if self.do_check(new_node, grid, player) == "do_raid":
                        node_change = self.do_raid(new_node, grid, player)
                        if new_node.depth == count and count == 1:
                            new_node.earn = self.total(grid, player)
                        elif new_node.depth == count and count == 2:
                            new_node.earn = (-1) * self.total(grid, player)
                        else:
                            new_node.earn = 10000
                            result = self.recursive_search(grid, new_node, self.changeplayer(player), count, result)
                        grid[new_node.row][new_node.column].holder = 0
                        for nodeX in node_change:
                            grid[nodeX.row][nodeX.column].holder = self.changeplayer(player)
                    if self.do_check(new_node, grid, player) == "do_sneak":
                        self.do_sneak(new_node, grid, player)
                        if new_node.depth == count and count == 1:
                            new_node.earn = self.total(grid, player)
                        elif new_node.depth == count and count == 2:
                            new_node.earn = (-1) * self.total(grid, player)
                        else:
                            new_node.earn = 10000
                            result = self.recursive_search(grid, new_node, self.changeplayer(player), count, result)
                        grid[new_node.row][new_node.column].holder = 0

                    if new_node.depth != 1 or count != 2:
                        result += new_node.nodetostring()

                    root.list.append(new_node)
                    if root.depth == 0:
                        if root.earn < new_node.earn:
                            root.earn = new_node.earn
                            result += root.nodetostring()
                        else:
                            result += root.nodetostring()
                    else:
                        if root.earn > new_node.earn:
                            root.earn = new_node.earn
                            result += root.nodetostring()
                        else:
                            result += root.nodetostring()
        return result


    # check each node and find the movement(raid or sneak) we use to go there
    def check(self, node, grid, player):

        if grid.hasNeighborHolder(node, player):
            return self.raid(node, grid, player)
        else:
            return self.sneak(node)

    def do_check(self, node, grid, player):
        if grid.hasNeighborHolder(node, player):
            return "do_raid"
        else:
            return "do_sneak"

    # we raid to this point and return the total value we can earn if we raid to this point
    def raid(self, node, grid, player):
        value = node.num
        if grid.hasNeighborHolder(node, self.changeplayer(player)):
            list = grid.neighbor(node)
            for node_check in list:
                if node_check.holder == self.changeplayer(player):
                    value += node_check.num
        return value

    def do_raid(self, node, grid, player):
        new_grid = grid
        node_change = []
        new_grid[node.row][node.column].holder = player
        if new_grid.hasNeighborHolder(node, self.changeplayer(player)):
            list = new_grid.neighbor(node)
            for node_check in list:
                if node_check.holder == self.changeplayer(player):
                    node_check.holder = player
                    node_change.append(node_check)
        return node_change


    # we sneak to this point and return the value we can earn if we sneak to this point
    def sneak(self, node):
        return node.num

    def do_sneak(self, node, grid, player):
        new_grid = grid
        new_grid[node.row][node.column].holder = player

    def total(self, grid, player):
        total1 = 0
        total2 = 0

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j].holder == player:
                    total1 += grid[i][j].num
                if grid[i][j].holder == self.changeplayer(player):
                    total2 += grid[i][j].num
        return total1 - total2

    def changeplayer(self, player):
        if player == 1:
            return 2
        else:
            return 1




class alphaBeta(object):

    # the main search part
    def search(self, player, depth, grid):

        # total1 = 0
        # total2 = 0
        #
        # for i in range(len(grid)):
        #     for j in range(len(grid[0])):
        #         if grid[i][j].holder == 1:
        #             total1 += grid[i][j].num
        #         if grid[i][j].holder == 2:
        #             total2 += grid[i][j].num

        # max: the max we can get
        # max_row & max column: the position we find max
        max = 0
        max_row = 0
        max_column = 0
        temp = 0

        root = gridNode(-1)
        root.row = -1
        root.column = -1
        root.holder = -1
        root.depth = 0
        root.earn = -10000
        root.alpha = -10000
        root.beta = 10000

        result = ""
        result += "Node,Depth,Value,Alpha,Beta"
        result += "\n"
        result = self.recursive_search(grid, root, player, depth, result)
        newfile = file()
        newfile.writefileMiniMax(result)


        # find the max in grid
        max_row = 0
        max_column = 0
        max = -10000
        for node in root.list:
            if node.earn > max:
                max_row = node.row
                max_column = node.column
                max = node.earn

        # return the position of the max we just found
        return [max_row,max_column]



    def recursive_search(self, grid, root, player, count, result):
        temp = root.nodetostring2()
        result += temp
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j].holder == 0:

                    new_node = gridNode(grid[i][j].num)
                    new_node.holder = player
                    new_node.row = grid[i][j].row
                    new_node.column = grid[i][j].column
                    new_node.depth = root.depth + 1
                    new_node.list = []
                    # new_node.earn = self.total(grid, player) + self.check(new_node, grid, player)

                    if self.do_check(new_node, grid, player) == "do_raid":
                        node_change = self.do_raid(new_node, grid, player)
                        if new_node.depth == count and count%2 == 1:
                            new_node.earn = self.total(grid, player)
                            new_node.alpha = root.alpha
                            new_node.beta = root.beta
                        elif new_node.depth == count and count %2 == 0:
                            new_node.earn = (-1) * self.total(grid, player)
                            new_node.alpha = root.alpha
                            new_node.beta = root.beta
                        else:
                            if new_node.depth%2 == 1:
                                new_node.earn = 10000
                                new_node.alpha = root.alpha
                                new_node.beta = root.beta
                                result = self.recursive_search(grid, new_node, self.changeplayer(player), count, result)
                            else:
                                new_node.earn = -10000
                                new_node.alpha = root.alpha
                                new_node.beta = root.beta
                                result = self.recursive_search(grid, new_node, self.changeplayer(player), count, result)
                        grid[new_node.row][new_node.column].holder = 0
                        for nodeX in node_change:
                            grid[nodeX.row][nodeX.column].holder = self.changeplayer(player)
                    elif self.do_check(new_node, grid, player) == "do_sneak":
                        self.do_sneak(new_node, grid, player)
                        if new_node.depth == count and count%2 == 1:
                            new_node.earn = self.total(grid, player)
                            new_node.alpha = root.alpha
                            new_node.beta = root.beta
                        elif new_node.depth == count and count %2 == 0:
                            new_node.earn = (-1) * self.total(grid, player)
                            new_node.alpha = root.alpha
                            new_node.beta = root.beta
                        else:
                            if new_node.depth%2 == 1:
                                new_node.earn = 10000
                                new_node.alpha = root.alpha
                                new_node.beta = root.beta
                                result = self.recursive_search(grid, new_node, self.changeplayer(player), count, result)
                            else:
                                new_node.earn = -10000
                                new_node.alpha = root.alpha
                                new_node.beta = root.beta
                                result = self.recursive_search(grid, new_node, self.changeplayer(player), count, result)
                        grid[new_node.row][new_node.column].holder = 0

                    if new_node.depth == count:
                        result += new_node.nodetostring2()

                    root.list.append(new_node)
                    if new_node.depth == 1:
                        if root.earn < new_node.earn:
                            root.earn = new_node.earn
                            root.alpha = new_node.earn
                            result += root.nodetostring2()
                        else:
                            result += root.nodetostring2()
                    elif new_node.depth == 2:
                        if root.earn > new_node.earn:
                            if new_node.earn <= root.alpha:
                                root.earn = new_node.earn
                                result += root.nodetostring2()
                                return result
                            else:
                                root.earn = new_node.earn
                                root.beta = new_node.earn
                                result += root.nodetostring2()
                        else:
                            result += root.nodetostring2()
        return result


    # check each node and find the movement(raid or sneak) we use to go there
    def check(self, node, grid, player):

        if grid.hasNeighborHolder(node, player):
            return self.raid(node, grid, player)
        else:
            return self.sneak(node)

    def do_check(self, node, grid, player):
        if grid.hasNeighborHolder(node, player):
            return "do_raid"
        else:
            return "do_sneak"

    # we raid to this point and return the total value we can earn if we raid to this point
    def raid(self, node, grid, player):
        value = node.num
        if grid.hasNeighborHolder(node, self.changeplayer(player)):
            list = grid.neighbor(node)
            for node_check in list:
                if node_check.holder == self.changeplayer(player):
                    value += node_check.num
        return value

    def do_raid(self, node, grid, player):
        new_grid = grid
        node_change = []
        new_grid[node.row][node.column].holder = player
        if new_grid.hasNeighborHolder(node, self.changeplayer(player)):
            list = new_grid.neighbor(node)
            for node_check in list:
                if node_check.holder == self.changeplayer(player):
                    node_check.holder = player
                    node_change.append(node_check)
        return node_change


    # we sneak to this point and return the value we can earn if we sneak to this point
    def sneak(self, node):
        return node.num

    def do_sneak(self, node, grid, player):
        new_grid = grid
        new_grid[node.row][node.column].holder = player

    def total(self, grid, player):
        total1 = 0
        total2 = 0

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j].holder == player:
                    total1 += grid[i][j].num
                if grid[i][j].holder == self.changeplayer(player):
                    total2 += grid[i][j].num
        return total1 - total2

    def changeplayer(self, player):
        if player == 1:
            return 2
        else:
            return 1





if __name__ == '__main__':

    newFile = file()

    # filename = sys.argv[-1]
    filename = "input.txt"
    list = newFile.readfile(filename)
    task = list[0]
    player = list[1]
    depth = list[2]
    newGrid = list[3]

    if task == 1:

        greedy = greedy()
        max = greedy.search(newGrid, player)
        i = max[0]
        j = max[1]
        # print i, j
        newGrid[i][j].holder = player

        if newGrid.hasNeighborHolder(newGrid[i][j], player):
            list = newGrid.neighbor(newGrid[i][j])
            for node in list:
                if node.holder == greedy.changeplayer(player):
                    node.holder = player
        newFile.writefile(newGrid)


    if task == 2:
        miniMax = miniMax()
        max = miniMax.search(player, depth, newGrid)
        i = max[0]
        j = max[1]
        newGrid[i][j].holder = player

        if newGrid.hasNeighborHolder(newGrid[i][j], player):
            list = newGrid.neighbor(newGrid[i][j])
            for node in list:
                if node.holder == miniMax.changeplayer(player):
                    node.holder = player
        newFile.writefile(newGrid)

    if task == 3:
        alphaBeta = alphaBeta()
        max = alphaBeta.search(player, depth, newGrid)
        i = max[0]
        j = max[1]
        newGrid[i][j].holder = player

        if newGrid.hasNeighborHolder(newGrid[i][j], player):
            list = newGrid.neighbor(newGrid[i][j])
            for node in list:
                if node.holder == alphaBeta.changeplayer(player):
                    node.holder = player
        newFile.writefile(newGrid)

    if task == 4:
        player1 = list[1]
        alg1 = list[2]
        depth1 = list[3]
        player2 = list[4]
        alg2 = list[5]
        depth2 = list[6]
        newGrid = list[7]

        currentplayer = player1
        currentalg = alg1
        currentdepth = depth1

        result = ""

        while newGrid.checkgrid():
            if currentalg == 1:
                new_greedy = greedy()
                max = new_greedy.search(newGrid, currentplayer)
                i = max[0]
                j = max[1]
                newGrid[i][j].holder = currentplayer

                if newGrid.hasNeighborHolder(newGrid[i][j], currentplayer):
                    list = newGrid.neighbor(newGrid[i][j])
                    for node in list:
                        if node.holder == new_greedy.changeplayer(currentplayer):
                            node.holder = currentplayer

            elif currentalg == 2:
                new_miniMax = miniMax()
                max = new_miniMax.search(currentplayer, currentdepth, newGrid)
                i = max[0]
                j = max[1]
                newGrid[i][j].holder = currentplayer

                if newGrid.hasNeighborHolder(newGrid[i][j], currentplayer):
                    list = newGrid.neighbor(newGrid[i][j])
                    for node in list:
                        if node.holder == new_miniMax.changeplayer(currentplayer):
                            node.holder = currentplayer
            else:
                new_alphaBeta = alphaBeta()
                max = new_alphaBeta.search(currentplayer, currentdepth, newGrid)
                i = max[0]
                j = max[1]
                newGrid[i][j].holder = currentplayer

                if newGrid.hasNeighborHolder(newGrid[i][j], currentplayer):
                    list = newGrid.neighbor(newGrid[i][j])
                    for node in list:
                        if node.holder == new_alphaBeta.changeplayer(currentplayer):
                            node.holder = currentplayer

            for m in range(5):
                for n in range(5):
                    if newGrid[m][n].holder == 1:
                        result += 'X'
                    elif newGrid[m][n].holder == 2:
                        result += 'O'
                    else:
                        result += '*'
                result += "\n"

            if currentplayer == player1:
                currentplayer = player2
                currentalg = alg2
                currentdepth = depth2
            else:
                currentplayer = player1
                currentalg = alg1
                currentdepth = depth1
        newFile.writefileState(result)
