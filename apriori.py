# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 21:19:19 2019

@author: lenovo
"""

'''---------------------使用Apriori算法进行关联分析-------------
从大规模数据集中寻找物品见的隐含关系称为关联分析
Apriori算法
频繁项集生成
关联规则生成
投票中的关联规则发现

优点：易编码实现
缺点：在大数据集上可能比较慢
适用数据类型：数值型或者标称型数据

频繁项集（frequent item sets）: 经常出现在一块的物品的集合。
关联规则（associational rules）: 暗示两种物品之间可能存在很强的关系。

频繁项集: {葡萄酒, 尿布, 豆奶} 就是一个频繁项集的例子。
关联规则: 尿布 -> 葡萄酒 就是一个关联规则。这意味着如果顾客买了尿布，那么他很可能会买葡萄酒。
频繁 的定义：
度量方法：支持度和可信度。
 
支持度: 数据集中包含该项集的记录所占的比例。
例如上图中，{豆奶} 的支持度为 4/5。{豆奶, 尿布} 的支持度为 3/5。

可信度: 针对一条诸如 {尿布} -> {葡萄酒} 这样具体的关联规则来定义的。这条规则的 可信度 被定义为 
支持度({尿布, 葡萄酒})/支持度({尿布})，从图中可以看出 支持度({尿布, 葡萄酒}) = 3/5，支持度({尿布}) = 4/5，
所以 {尿布} -> {葡萄酒} 的可信度 = 3/5 / 4/5 = 3/4 = 0.75。
支持度 和 可信度 是用来量化 关联分析 是否成功的一个方法。 

假设想找到支持度大于 0.8 的所有项集，应该如何去做呢？
 一个办法是生成一个物品所有可能组合的清单，然后对每一种组合统计它出现的频繁程度，
 但是当物品成千上万时，上述做法就非常非常慢了。 
 
 我们需要详细分析下这种情况并讨论下 Apriori 原理，该原理会减少关联规则学习时所需的计算量。



Apriori 原理，即某个项集是频繁的，那么它的所有子集也是频繁的。 
也就是说如果一个项集是 非频繁项集，那么它的所有超集也是非频繁项集

Apriori算法（发现频繁项集的方法）的流程步骤：
收集数据：使用任意方法。
* 准备数据：任何数据类型都可以，因为我们只保存集合。
* 分析数据：使用任意方法。
* 训练数据：使用Apiori算法来找到频繁项集。
* 测试算法：不需要测试过程。
* 使用算法：用于发现频繁项集以及物品之间的关联规则。

算法思想
 Apriori 算法：
 输入：参数分别是最小支持度和数据集。 
生成所有单个物品的项集列表。
if:
    那些不满足最小支持度要求的集合会被去掉。 
else:
    接着扫描交易记录来查看哪些项集满足最小支持度要求，

for燃尽后对生下来的集合:
    进行组合以声场包含两个元素的项集。 
    for接下来再重新扫描交易记录，
    去掉不满足最小支持度的项集。
    该过程重复进行直到所有项集被去掉。


数据扫描的伪代码如下: 
---------------------从交易记录里获取交易记录子集-候选项集-------------------
对数据集中的每条交易记录 tran:
    对每个候选项集 can
    检查一下 can 是否是 tran 的子集: 
        如果是则增加 can 的计数值
------------------------历遍候选项集获取满足支持度的候选项集---------------------
for每个候选项集:
    if 其支持度不低于最小值:
        则保留该项集
返回所有频繁项集列表 以下是一些辅助函数。
'''
'''-------------------------获取频繁项集-----------------------'''
# 创建了用于测试的简单数据集
def loadDataSet():
    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]

#数据集去重
# 创建集合 C1。即对 dataSet 进行去重，排序，放入 list 中，然后转换所有的元素为 frozenset
def createC1(dataSet):
    """createC1（创建集合 C1）

    Args:
        dataSet 原始数据集
    Returns:
        frozenset 返回一个 frozenset 格式的 list
    """

    C1 = []
    for transaction in dataSet:   #历遍数据集的交易记录
        for item in transaction:   #历遍交易记录的每个项集
            if not [item] in C1:    #如果项集
                # 遍历所有的元素，如果不在 C1 出现过，那么就 append
                C1.append([item])
    # 对数组进行 `从小到大` 的排序
    #print('sort 前=', C1)
    C1.sort()
    # frozenset 表示冻结的 set 集合，元素无改变；可以把它当字典的 key 来使用
    #print('sort 后=', C1)
    #print('frozenset=', map(frozenset, C1)) 
    return list(map(frozenset, C1))  #将C1转换成frozenset格式，并以list列表形式返回

#计算支持度，并进行筛选
#计算候选数据集 CK 在数据集 D 中的支持度，并返回支持度大于最小支持度（minSupport）的数据
def scanD(D, Ck, minSupport):
    """scanD（计算候选数据集 CK 在数据集 D 中的支持度，并返回支持度大于最小支持度 minSupport 的数据）

    Args:
        D 数据集
        Ck 候选项集列表
        minSupport 最小支持度
    Returns:
        retList 支持度大于 minSupport 的集合
        supportData 候选项集支持度数据
    """

    # ssCnt 临时存放选数据集 Ck 的频率. 例如: a->10, b->5, c->8
    ssCnt = {}
    for tid in D:      #对于数据集的每条记录
        for can in Ck:     #对于
            # s.issubset(t)  测试是否 s 中的每一个元素都在 t 中
            if can.issubset(tid):   
                if can not in ssCnt:  #如果该元素啊没有在D数据集中(与python2代码不同)
                    ssCnt[can] = 1          #在D中创建该键，并赋值1
                else:
                    ssCnt[can] += 1         #根据出现次数，累计其value
    numItems = float(len(D)) # 数据集 D 的数量,map,无len，外加一个list
    retList = []    #存储满足支持度大于最小支持度的键
    supportData = {}  #用字典存储满足支持度的键和value
    for key in ssCnt.keys():
        # 支持度 = 候选项（key）出现的次数 / 所有数据集的数量
        support = ssCnt[key]/numItems
        if support >= minSupport:
            # 在 retList 的首位插入元素，只存储支持度满足频繁项集的值
            retList.append(key)
        # 存储所有的候选项（key）和对应的支持度（support）
        supportData[key] = support
    return retList, supportData

#导入数据
dataSet=loadDataSet()
#构建第一个候选项集
c1=createC1(dataSet)
#构建集合表示的数据集
D=list(map(set,dataSet))   #相对于python2的改进
D
len(D)
L1,suppData0=scanD(D,c1,0.5)
L1
suppData0

'''--------------------完整的Apriori---------------------'''
#对保留的项集进行合并由L1-C2
''' 输入频繁项集列表 Lk 与返回的元素个数 k，然后输出所有可能的候选项集 Ck

整个Aprior算法的伪代码:
while数据集中项的个数大于0:
    构建一个k个项组成的候选项集的列表
    检查数据以确保每个项集都是频繁的
    保留频繁项集并构建k+1项组成的候选项集的列表
'''

def aprioriGen(Lk, k):
    """aprioriGen（输入频繁项集列表 Lk 与返回的元素个数 k，然后输出候选项集 Ck。
       例如: 以 {0},{1},{2} 为输入且 k = 2 则输出 {0,1}, {0,2}, {1,2}. 以 {0,1},{0,2},{1,2} 为输入且 k = 3 则输出 {0,1,2}
       仅需要计算一次，不需要将所有的结果计算出来，然后进行去重操作
       这是一个更高效的算法）

    Args:
        Lk 频繁项集列表
        k 返回的项集元素个数（若元素的前 k-2 相同，就进行合并）
    Returns:
        retList 元素两两合并的数据集
    """
# 如果数据长度为n，取前n-1个元素相同的两个数据合并组成新的数据，这样不必计算所有的组合，可以省略剪枝步骤
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk):     #对i以后的进行历遍
            L1 = list(Lk[i])[: k-2]
            L2 = list(Lk[j])[: k-2]
            #print('-----i=', i, k, Lk, Lk[i], list(Lk[i])[: k-2])
            #print('-----j=', j, k, Lk, Lk[j], list(Lk[j])[: k-2])
            L1.sort()     #对元素进行排序
            L2.sort()
            # 第一次 L1,L2 为空，元素直接进行合并，返回元素两两合并的数据集
            # if first k-2 elements are equal
            if L1 == L2:     #如果两集合前k-2个元素相同，则将集合进行合并
                #set union
                #print('union=', Lk[i] | Lk[j], Lk[i], Lk[j])
                retList.append(Lk[i] | Lk[j])   #|求并集，将两集合合并成大小为k的集合
    return retList   #元素合并的数据集

# 找出数据集 dataSet 中支持度 >= 最小支持度的候选项集以及它们的支持度。即我们的频繁项集。
def apriori(dataSet, minSupport=0.5):
    """apriori（首先构建集合 C1，然后扫描数据集来判断这些只有一个元素的项集是否满足最小支持度的要求。那么满足最小支持度要求的项集构成集合 L1。然后 L1 中的元素相互组合成 C2，C2 再进一步过滤变成 L2，然后以此类推，知道 CN 的长度为 0 时结束，即可找出所有频繁项集的支持度。）

    Args:
        dataSet 原始数据集
        minSupport 支持度的阈值
    Returns:
        L 频繁项集的全集
        supportData 所有元素和支持度的全集
    """
    # C1 即对 dataSet 进行去重，排序，放入 list 中，然后转换所有的元素为 frozenset
    C1 = createC1(dataSet)     
    # 对每一行进行 set 转换，然后存放到集合中
    D = list(map(set, dataSet))
    #print('D=', D)
    # 计算候选数据集 C1 在数据集 D 中的支持度，并返回支持度大于 minSupport 的数据
    L1, supportData = scanD(D, C1, minSupport)
    # print "L1=", L1, "\n", "outcome: ", supportData
    # L 加了一层 list, L 一共 2 层 list
    L = [L1]
    k = 2
    # 判断 L 的第 k-2 项的数据长度是否 > 0。第一次执行时 L 为 [[frozenset([1]), frozenset([3]), frozenset([2]), frozenset([5])]]。L[k-2]=L[0]=[frozenset([1]), frozenset([3]), frozenset([2]), frozenset([5])]，最后面 k += 1
    while (len(L[k-2]) > 0):   #创建包含更大项集的更大列表,直到下一个大的项集为1
        #print('k=', k, L, L[k-2])
        Ck = aprioriGen(L[k-2], k) # 例如: 以 {0},{1},{2} 为输入且 k = 2 则输出 {0,1}, {0,2}, {1,2}. 以 {0,1},{0,2},{1,2} 为输入且 k = 3 则输出 {0,1,2}
        #print('Ck', Ck)

        Lk, supK = scanD(D, Ck, minSupport) # 计算候选数据集 CK 在数据集 D 中的支持度，并返回支持度大于 minSupport 的数据
        # 保存所有候选项集的支持度，如果字典没有，就追加元素，如果有，就更新元素
        supportData.update(supK)
        # Lk 表示满足频繁子项的集合，L 元素在增加，例如: 
        # l=[[set(1), set(2), set(3)]]
        # l=[[set(1), set(2), set(3)], [set(1, 2), set(2, 3)]]
        L.append(Lk)
        k += 1
        # print 'k=', k, len(L[k-2])
    return L, supportData

L, supportData=apriori(dataSet, minSupport=0.5)
L
L[0]
L[1]
L[2]
L[3]

#共组成6个组合集合，其中四个保留在L[1]中，剩下两个集合被scanD()过滤掉
aprioriGen(L[0],2)

#支持度为70%的结果
L, supportData=apriori(dataSet, minSupport=0.7)
L
L[0]
L[1]
L[2]


'''-----------------------------从频繁项集中挖掘关联规则----------------------'''
'''
从频繁项集中挖掘关联规则
前面我们介绍了用于发现 频繁项集 的 Apriori 算法，现在要解决的问题是如何找出 关联规则。

对于 关联规则，我们也有类似的量化方法，这种量化指标称之为 可信度。
一条规则 A -> B 的可信度定义为 support(A | B) / support(A)。
（注意: 在 python 中 | 表示集合的并操作，而数学书集合并的符号是 U,A | B 是指所有出现在集合 A 或者集合 B 中的元素。)

由于我们先前已经计算出所有 频繁项集 的支持度了，现在我们要做的只不过是提取这些数据做一次除法运算即可

如果某条规则并不满足 最小可信度 要求，那么该规则的所有子集也不会满足 最小可信度 的要求。

'''
# 计算可信度（confidence）
def calcConf(freqSet, H, supportData, brl, minConf=0.7):
    """calcConf（对两个元素的频繁项，计算可信度，例如： {1,2}/{1} 或者 {1,2}/{2} 看是否满足条件）

    Args:
        freqSet 频繁项集中的元素，例如: frozenset([1, 3])    
        H 频繁项集中的元素的集合，例如: [frozenset([1]), frozenset([3])]
        supportData 所有元素的支持度的字典
        brl 关联规则列表的空数组
        minConf 最小可信度
    Returns:
        prunedH 记录 可信度大于阈值的集合
    """
    # 记录可信度大于最小可信度（minConf）的集合
    prunedH = []
    for conseq in H: # 假设 freqSet = frozenset([1, 3]), H = [frozenset([1]), frozenset([3])]，那么现在需要求出 frozenset([1]) -> frozenset([3]) 的可信度和 frozenset([3]) -> frozenset([1]) 的可信度

        # print 'confData=', freqSet, H, conseq, freqSet-conseq
        conf = supportData[freqSet]/supportData[freqSet-conseq] # 支持度定义: a -> b = support(a | b) / support(a). 假设  freqSet = frozenset([1, 3]), conseq = [frozenset([1])]，那么 frozenset([1]) 至 frozenset([3]) 的可信度为 = support(a | b) / support(a) = supportData[freqSet]/supportData[freqSet-conseq] = supportData[frozenset([1, 3])] / supportData[frozenset([1])]
        if conf >= minConf:
            # 只要买了 freqSet-conseq 集合，一定会买 conseq 集合（freqSet-conseq 集合和 conseq 集合是全集）
            print(freqSet-conseq, '-->', conseq, 'conf:', conf)
            brl.append((freqSet-conseq, conseq, conf))
            prunedH.append(conseq)
    return prunedH

# 递归计算频繁项集的规则
def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):
    """rulesFromConseq

    Args:
        freqSet 频繁项集中的元素，例如: frozenset([2, 3, 5])    
        H 频繁项集中的元素的集合，例如: [frozenset([2]), frozenset([3]), frozenset([5])]
        supportData 所有元素的支持度的字典
        brl 关联规则列表的数组
        minConf 最小可信度
    """
    # H[0] 是 freqSet 的元素组合的第一个元素，并且 H 中所有元素的长度都一样，长度由 aprioriGen(H, m+1) 这里的 m + 1 来控制
    # 该函数递归时，H[0] 的长度从 1 开始增长 1 2 3 ...
    # 假设 freqSet = frozenset([2, 3, 5]), H = [frozenset([2]), frozenset([3]), frozenset([5])]
    # 那么 m = len(H[0]) 的递归的值依次为 1 2
    # 在 m = 2 时, 跳出该递归。假设再递归一次，那么 H[0] = frozenset([2, 3, 5])，freqSet = frozenset([2, 3, 5]) ，没必要再计算 freqSet 与 H[0] 的关联规则了。
    m = len(H[0])   #计算H中频繁项集m的大小
    if (len(freqSet) > (m + 1)):   #判断该频繁项集m是否大到可以移除大小为m的子集
        print('freqSet******************', len(freqSet), m + 1, freqSet, H, H[0])
        # 生成 m+1 个长度的所有可能的 H 中的组合，假设 H = [frozenset([2]), frozenset([3]), frozenset([5])]
        # 第一次递归调用时生成 [frozenset([2, 3]), frozenset([2, 5]), frozenset([3, 5])]
        # 第二次 。。。没有第二次，递归条件判断时已经退出了
        Hmp1 = aprioriGen(H, m+1) #生成H元素的无重复组合，将为下次迭代的H，包含所有可能的规则
        # 返回可信度大于最小可信度的集合
        Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)
        print('Hmp1=', Hmp1)
        print('len(Hmp1)=', len(Hmp1), 'len(freqSet)=', len(freqSet))
        # 计算可信度后，还有数据大于最小可信度的话，那么继续递归调用，否则跳出递归
        if (len(Hmp1) > 1): #如果不知一条规则满足要求，调用rulesFromConseq函数来判断是否可以进一步组合规则
            print('----------------------', Hmp1)
            # print len(freqSet),  len(Hmp1[0]) + 1
            rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)
            
            
# 生成关联规则
def generateRules(L, supportData, minConf=0.7):
    """generateRules

    Args:
        L 频繁项集列表
        supportData 频繁项集支持度的字典
        minConf 最小置信度
    Returns:
        bigRuleList 可信度规则列表（关于 (A->B+置信度) 3个字段的组合）
    """
    bigRuleList = []
    # 假设 L = [[frozenset([1]), frozenset([3]), frozenset([2]), frozenset([5])], [frozenset([1, 3]), frozenset([2, 5]), frozenset([2, 3]), frozenset([3, 5])], [frozenset([2, 3, 5])]]
    for i in range(1, len(L)):
        # 获取频繁项集中每个组合的所有元素
        for freqSet in L[i]:
            # 假设：freqSet= frozenset([1, 3]), H1=[frozenset([1]), frozenset([3])]
            # 组合总的元素并遍历子元素，并转化为 frozenset 集合，再存放到 list 列表中
            H1 = [frozenset([item]) for item in freqSet]
            # 2 个的组合，走 else, 2 个以上的组合，走 if
            if (i > 1): #如果频繁集元素数目超过2，那么对他做进一步合并
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:     #如果频繁集只有两个元素，使用calcConf()函数计算可信度值
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList


#生成最小支持度是0.5的频繁项集的集合
L, supportData=apriori(dataSet, minSupport=0.5)
rules=generateRules(L,supportData,minConf=0.7)

rules=generateRules(L,supportData,minConf=0.5)
rules



'''------------在更大的真实数据集上测试利用Apriori算法测试关联分析的效果-------'''
'''
在美国国会记录中发现关联规则
（1）搜集数据：使用votesmart模块来访问投票记录
（2）准备数据:构造函数来将投票转化成一串交易记录
（3）分析数据：在python提示符下查看准备的数据，以确保其正确性
（4）训练算法：使用apriori()和generateRules()函数来发现投票记录中的有趣信息
（5）测试算法：没有测试过程
（6）使用算法：可以使用分析结果来为政治竞选活动服务，或者预测选举官员会如何投票

数据处理：使每行代表美国国会的一个成员，每列为他们投票的对象，








