import time
import csv

#Function to load file and return lists of Transactions
def Load_data(filename):
    with open(filename) as f:
        content = f.readlines()

    content = [x.strip() for x in content]
    Transaction = []

    for i in range(0, len(content)):
        Transaction.append(content[i].split())

    return Transaction

#To convert initial transaction into frozenset
def create_initialset(dataset):
    retDict = {}
    for trans in dataset:
        retDict[frozenset(trans)] = 1
    return retDict

#class of FP TREE node
class TreeNode:
    def __init__(self, Node_name,counter,parentNode):
        self.name = Node_name
        self.count = counter
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}
        
    def increment_counter(self, counter):
        self.count += counter

#To create Headertable and ordered itemsets for FP Tree
def create_FPTree(dataset, minSupport):
    HeaderTable = {}
    for transaction in dataset:
        for item in transaction:
            HeaderTable[item] = HeaderTable.get(item,0) + dataset[transaction]
    for k in list(HeaderTable):
        if HeaderTable[k] < minSupport:
            del(HeaderTable[k])

    frequent_itemset = set(HeaderTable.keys())

    if len(frequent_itemset) == 0:
        return None, None

    for k in HeaderTable:
        HeaderTable[k] = [HeaderTable[k], None]

    retTree = TreeNode('Null Set',1,None)
    for itemset,count in dataset.items():
        frequent_transaction = {}
        for item in itemset:
            if item in frequent_itemset:
                frequent_transaction[item] = HeaderTable[item][0]
        if len(frequent_transaction) > 0:
            ordered_itemset = [v[0] for v in sorted(frequent_transaction.items(), key=lambda p: p[1], reverse=True)]
      
            updateTree(ordered_itemset, retTree, HeaderTable, count)
    return retTree, HeaderTable

#To create the FP Tree using ordered itemsets
def updateTree(itemset, FPTree, HeaderTable, count):
    if itemset[0] in FPTree.children:
        FPTree.children[itemset[0]].increment_counter(count)
    else:
        FPTree.children[itemset[0]] = TreeNode(itemset[0], count, FPTree)

        if HeaderTable[itemset[0]][1] == None:
            HeaderTable[itemset[0]][1] = FPTree.children[itemset[0]]
        else:
            update_NodeLink(HeaderTable[itemset[0]][1], FPTree.children[itemset[0]])

    if len(itemset) > 1:
        updateTree(itemset[1::], FPTree.children[itemset[0]], HeaderTable, count)

#To update the link of node in FP Tree
def update_NodeLink(Test_Node, Target_Node):
    while (Test_Node.nodeLink != None):
        Test_Node = Test_Node.nodeLink

    Test_Node.nodeLink = Target_Node

#To transverse FPTree in upward direction
def FPTree_uptransveral(leaf_Node, prefixPath):
 if leaf_Node.parent != None:
    prefixPath.append(leaf_Node.name)
    FPTree_uptransveral(leaf_Node.parent, prefixPath)

#To find conditional Pattern Bases
def find_prefix_path(basePat, TreeNode):
 Conditional_patterns_base = {}

 while TreeNode != None:
    prefixPath = []
    FPTree_uptransveral(TreeNode, prefixPath)
    if len(prefixPath) > 1:
        Conditional_patterns_base[frozenset(prefixPath[1:])] = TreeNode.count
    TreeNode = TreeNode.nodeLink

 return Conditional_patterns_base

#function to mine recursively conditional patterns base and conditional FP tree
def Mine_Tree(FPTree, HeaderTable, minSupport, prefix, frequent_itemset):
    bigL = [v[0] for v in sorted(HeaderTable.items(),key=lambda p: p[1][0])]
    for basePat in bigL:
        new_frequentset = prefix.copy()
        new_frequentset.add(basePat)
        frequent_itemset.append(new_frequentset)
        Conditional_pattern_bases = find_prefix_path(basePat, HeaderTable[basePat][1])
        Conditional_FPTree, Conditional_header = create_FPTree(Conditional_pattern_bases,minSupport)

        if Conditional_header != None:
            Mine_Tree(Conditional_FPTree, Conditional_header, minSupport, new_frequentset, frequent_itemset)

def get_support_count(v,dataset):
    count=0
    n=len(v)
    a={}
    x=0
    for i in dataset:
        a[x]=set(i)
        x+=1
    for key,value in a.items():
        if v.issubset(value):
            count+=1
    return count


def generate_association_rules(dataset,itemset,confidence):
    for i in itemset:
        count=get_support_count(set(i),dataset)
        if len(i)==2:
            x=i[0]
            y=i[1]
            x_count=get_support_count(set([x]),dataset)
            y_count=get_support_count(set([y]),dataset)
            if x_count!=0:
                if((count/x_count)*100 >=confidence):
                    print(x,"==>",y)
            if y_count!=0:
                if((count/y_count)*100 >=confidence):
                    print(y,"==>",x)
        if len(i)==3:
            x=i[0]
            y=i[1]
            z=i[2]
            x_count=get_support_count(set([y]+[z]),dataset)
            y_count=get_support_count(set([x]+[z]),dataset)
            z_count=get_support_count(set([x]+[y]),dataset)
            if x_count!=0:
                if((count/x_count)*100 >=confidence):
                    print(y,"^",z,"==>",x)
            if y_count!=0:
                if((count/y_count)*100 >=confidence):
                    print(x,"^",z,"==>",y)
            if z_count!=0:
                if((count/z_count)*100 >=confidence):
                    print(x,"^",y,"==>",z)


def read_dataset():
    data=[]
    with open("test_dataset_1.csv",'r') as csvfile:
        csvreader=csv.reader(csvfile)
        for i in csvreader:
            data.append(i)
    return data


dataset=read_dataset()
min_Support = 2   
csv_file ="test_dataset_1.csv"
txt_file = "data.txt"
with open(txt_file, "w") as my_output_file:
    with open(csv_file, "r") as my_input_file:
        [ my_output_file.write(" ".join(row)+'\n') for row in csv.reader(my_input_file)]
    my_output_file.close()

initSet = create_initialset(Load_data("data.txt"))
start = time.time()
FPtree, HeaderTable = create_FPTree(initSet, min_Support)

frequent_itemset = []
Mine_Tree(FPtree, HeaderTable, min_Support, set([]), frequent_itemset)
end = time.time()

itemset=[]
for i in frequent_itemset:
    if len(i)!=1:
        itemset.append(list(i))

print("Frequent Itemset using FPtree:")
for i in itemset:
    print(i)
confidence=60
print("association rule")
generate_association_rules(dataset,itemset,confidence)



