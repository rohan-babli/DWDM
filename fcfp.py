import csv
class TreeNode:
    def __init__(self, Node_name,counter,parentNode):
        self.name = Node_name
        self.count = counter
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}
        
    def increment_counter(self, counter):
        self.count += counter
class Node:
	def __init__(self,item,count,parent):
		self.name = node_name
		self.count=count
		self.nodelink=None
		self.parent=parent
		self.children = {}

def create_initialset(dataset):
    retDict = {}
    for trans in dataset:
        retDict[frozenset(trans)] = 1
    return retDict

def Load_data(filename):
    with open(filename) as f:
        content = f.readlines()

    content = [x.strip() for x in content]
    Transaction = []

    for i in range(0, len(content)):
        Transaction.append(content[i].split())

    return Transaction

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

# to compress infrequent items
def compress(itemset,FPTree,HeaderTable,count):
	pass

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
#update Header Tbale and Head
def update_table(new,HeaderTable,Head,minSupport):
	for row in new:
		for item in row:
			if item in HeaderTable.keys():
				HeaderTable[item][0]+=1
			else:
				HeaderTable[item]=[1,None]
	Head = [v[0] for v in sorted(HeaderTable.items(), key=lambda p: p[1][0], reverse=True)]
	return HeaderTable,Head

def adjacent_adj(FPtree,new_Header,head,new_head,i,j):
	a=new_Header[head[i]][1]
	b=new_Header[new_head[j]][1]
	a1=Node(a.name,a.count-b.count,a.parent)
	a.count=b.count
	for key,value in a.children.items():
		if key != b.name:
			child=value
			child.parent=a1
			a1.children[chlid.name]=child
			del(a.children[child.name])
	b.parent=a.parent
	a.parent=b
	del(a.children[b.name])
	par=b.parent
	for key,value in par.children.items():
		if key==b.name and value!=b:
			X=value
			b.count=X.count+b.count
			for item,value in X.children.items():
				value.parent=b
				b.childeren[value.name]=value
			del(X)

	return FPtree

def non_adjacent_adj(FPtree,new_Header,head,new_head,i,j):
	e=new_Header[new_Header[j]][1]
	while e != None:
		d=e.parent
		while new_Header[d.name][0]< new_Header[e.name][0]:
			d1=Node(d.name,d.count-e.count,None)
			if d1.count!=0:
				d.count=e.count
				for key,value in d.children.items():
					if key != e.name:
						child=value
						child.parent=d1
						d1.children[chlid.name]=child
						del(d.children[child.name])
				

				par=d.parent
				for item,value in par.children.items():
					if item == e.name and value != e:
						X=value
						e.count=X.count+e.count
						for i,v in X.children.items():
							v.parent=X.parent
						del(X)
					if item != e.name:
						X=value
						for i,v in X.children.items():
							if i==e.name:
								e.count=e.count+v.count
								for i1,v1 in v.children.items():
									v1.parent=v.parent
								del(v)
				e.parent=d.parent
				d.parent=e
				del(d.children[e.name])
				d=e.parent
	return FPtree

def adjust_fcfp(FPtree,HeaderTable,head,minSupport,new_Header,new_head):
	for i in range(len(head)):
		if new_Header[head[i]][0]>=minSupport and HeaderTable[head[i]][0]>=minSupport:
			f==1
			if head[i] != new_head[i]:
				for j in range(i,len(new_head)):
					if new_head[j]==head[i]:
						f==0
						break
			if f==0:
				if abs(i-j)==1:
					FPtree=adjacent_adj(FPtree,new_Header,head,new_head,i,j)
				else:
					FPtree=non_adjacent_adj(FPtree,new_Header,head,new_head,i,j)

		if new_Header[head[i]][0]>=minSupport and HeaderTable[head[i]][0]<minSupport:
			f==1
			if head[i] != new_head[i]:
				for j in range(i,len(new_head)):
					if new_head[j]==head[i]:
						f==0
						break
			node=new_Header[head[i]][1]
			while node.nodelink != None:
				if node.iscompressed==True:
					new_node=Node(head[i],node.count,node.parent)      #vary this code depending on compression
					node.parent=new_node
					new_node.children[node.item]=node

			if f==0:
				if abs(i-j)==1:
					FPtree=adjacent_adj(FPtree,new_Header,head,new_head,i,j)
				else:
					FPtree=non_adjacent_adj(FPtree,new_Header,head,new_head,i,j)



#To add new dataset
def add_data(NDS,FPTree,HeaderTable,Head,minSupport):
	min_Support = minSupport  
	csv_file =NDS
	new_data=[]
	with open(NDS,'r') as file:
		reader = csv.reader(file)
		for row in reader:
			new_data.append(row)
	new_head, new_Header = update_table(new_data,HeaderTable,Head,minSupport)

	txt_file = "data.txt"
	with open(txt_file, "w") as my_output_file:
	    with open(csv_file, "r") as my_input_file:
	        [ my_output_file.write(" ".join(row)+'\n') for row in csv.reader(my_input_file)]
	    my_output_file.close()

	newSet = create_initialset(Load_data("data.txt"))
	FPtree, HeaderTable = create_FPTree(newSet, min_Support)
	Head = [v[0] for v in sorted(HeaderTable.items(), key=lambda p: p[1][0], reverse=True)]

	frequent_itemset = []
	Mine_Tree(FPtree, HeaderTable, min_Support, set([]), frequent_itemset)

	itemset=[]
	for i in frequent_itemset:
	    if len(i)!=1:
	        itemset.append(list(i))

	print("Frequent Itemset using FPtree:")
	for i in itemset:
	    print(i)
	f=int(input(("enter 0 to get association rules: ")))
	if f==0:
		confidence=int(input("enter confidence: "))
		dataset=read_dataset(NDS)
		print("association rule")
		generate_association_rules(dataset,itemset,confidence)


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


def read_dataset(file):
    data=[]
    with open(file,'r') as csvfile:
        csvreader=csv.reader(csvfile)
        for i in csvreader:
            data.append(i)
    #print("Data",data[:10])
    return data




###############################################################################################
csv_file =input("enter dataset: ")
min_Support = int(input("enter minimum support: "))
txt_file = "data.txt"
with open(txt_file, "w") as my_output_file:
    with open(csv_file, "r") as my_input_file:
        [ my_output_file.write(" ".join(row)+'\n') for row in csv.reader(my_input_file)]
    my_output_file.close()

initSet = create_initialset(Load_data("data.txt"))
FPtree, HeaderTable = create_FPTree(initSet, min_Support)
#print(HeaderTable)
Head = [v[0] for v in sorted(HeaderTable.items(), key=lambda p: p[1][0], reverse=True)]

frequent_itemset = []
Mine_Tree(FPtree, HeaderTable, min_Support, set([]), frequent_itemset)

itemset=[]
for i in frequent_itemset:
    if len(i)!=1:
        itemset.append(list(i))

print("Frequent Itemset using FPtree:")
for i in itemset:
    print(i)

f=int(input(("enter 0 to get association rules: ")))
if f==0:
	confidence=int(input("enter confidence: "))
	dataset=read_dataset(csv_file)
	print("association rule")
	generate_association_rules(dataset,itemset,confidence)
##############################################################################################
loop=True
while loop:
	y=int(input("enter 0 to add new dataset: "))
	if y==0:
		NDS=input("entert file name: ")
		support=int(input("enter minimum support: "))
		add_data(NDS,FPtree,HeaderTable,Head,support)
	else:
		loop=False


