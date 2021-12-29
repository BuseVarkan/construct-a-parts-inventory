#example is like bike_tree=
# ['bike',['wheel',['rim',[],[],[]],['spoke',[],[],[]],['hub',['gear',[],[],[]],['axle',['bolt',[],[],[]],['nut',[],[],[]]],[]]],
# ['frame',['rearframe',[],[],[]],['frontframe',['fork'],['handle'],[]]],[]]

def get_root(part_list):
    index = -1
    for i in range(len(part_list)):
        count = 1
        for satir in range(len(part_list)):
            for j in range(1, len(part_list[satir])):
                if type(part_list[satir][j]) == tuple:
                    if part_list[satir][j][1] == part_list[i][0]:
                        count += 1
        if count == 1: #rootun adi bir defa geciyor
            index = i
    return index # rootun indeksi


def find_element(e,part_list):
    for i in part_list:
        if i[0] == e:
            return i


def rec_tree_builder(node,part_list):
    part = node[1]
    e = find_element(part,part_list)

    if len(e) == 2 and type(e[1]) == float:
        node.append(e[1])
    else:
        for i in e[1:]:
            l = []
            for j in i:
                l.append(j)
            node.append(l)
        for i in node[2:]:
            rec_tree_builder(i,part_list)

def build_tree(part_list):
    tree = []
    root = part_list[get_root(part_list)]
    tree.append(1)
    tree.append(root[0])
    rec_tree_builder(tree,part_list)
    if len(part_list)==1:
        tree= [1,part_list[0][0],part_list[0][1]]
    return tree   #agac olustu cok sukur



def calculate_price(part_list):
    my_tree=build_tree(part_list)
    return helper_calculate(my_tree[2:])

def helper_calculate(my_tree):
    sum=0
    if type(my_tree[0])==float:
        sum+=my_tree[0]*1
    else:
        for i in my_tree:  # children list
            if type(i[2:]) == float:
                sum += my_tree[2:]*my_tree[0]
            else:
                sum+=helper_calculate(i[2:])*i[0]
    return sum

def required_parts(part_list):
    my_tree=build_tree(part_list)
    return helper_required_parts(my_tree,1)


def helper_required_parts(my_tree,total):
    result=[]
    if type(my_tree[2])==float:
        result.append((total,my_tree[1]))
    else:
        for i in my_tree[2:]: # children list
            if type(i[2])==float:
                result.append((total*i[0],i[1]))
            else:
                result.append(helper_required_parts(i,total*i[0]))
    return flatten(result)
def flatten(lst):
    if lst==[]:
        return []
    if type(lst[0])==list:
        return flatten(lst[0]) +flatten(lst[1:])
    else:
        return [lst[0]]+flatten(lst[1:])



#stock_list = [(2, "rim"), (2, "spoke"), (4, "gear"), (8, "bolt"), (12, "nut"),(1, "rearframe"), (1, "fork"), (1, "handle")]


def stock_check(part_list,stock_list):
   return helper_stock_check(part_list,stock_list)

def helper_stock_check(part_list,stock_list):
    names_for_j = []
    result = []
    for j in stock_list:
        names_for_j.append(j[1])
    for i in required_parts(part_list):
        if not i[1] in names_for_j:
            result.append((i[1], i[0]))
        else:
            for j in stock_list:
                if i[1] == j[1]:
                    N = i[0]
                    M = j[0]
                    if M < N:
                        result.append((i[1], N - M))
    return result