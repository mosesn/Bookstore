import random
import time
import math

LOAD = 1

#O(n)
def randomize(input_lst):
    random.shuffle(input_lst)
    return input_lst

class Node:
    def __init__(self,my_val):
        self.next = None
        self.val = my_val

#    def __str__(self):
#        return str(self.val) + str(self.next)

    def get_val(self):
        return self.val

    def set_next(self, new_next):
        self.next = new_next

    def get_next(self):
        return self.next

class LList:
    def __init__(self,my_node):
        self.head = my_node
        self.tail = my_node

    def prepend(self,node,tail):
        if not node:
            return True
        tmp = self.head
        self.head = node
        tail.next = tmp
        if not self.tail:
#            print tail
            self.tail = tail
#        print self.head


    def set_cannibal_head(self):
        self.head.set_next(None)
        self.tail = self.head

    def get_follow(self):
        return self.head.get_next()

    def __str__(self):
        return str(self.head)

    def get_head(self):
        return self.head

    def set_head(self, my_head):
#        print "setting head"
        if self.head == my_head:
            return
        if self.head:
            if my_head:
                my_head.set_next(self.head)
                self.head = my_head
            else:
                self.head = my_head
                self.tail = my_head
        else:
            if my_head:
                my_head.set_next(self.head)
                self.head = my_head
                self.tail = my_head
            else:
                self.head = my_head
                self.tail = my_head

    def get_tail(self):
        return self.tail

    def set_tail(self, my_tail):
        self.tail.set_next(my_tail)
        self.tail = my_tail

def print_ll(llist):
    for ll in llist:
        if ll != None and ll.get_head() != None:
            print "head " +str(ll.get_head().get_val())+ ":" + print_nodes(ll.get_head()) + ": tail " +  str(ll.get_tail().get_val())
        elif ll.get_head() == None:
            print "None!"
            if ll.get_tail() != None:
                print ll.get_tail().get_val()
    print "list over"

def print_nodes(node):
    if node:
        return str(node.get_val()) + " , " + print_nodes(node.get_next())
    else:
        return "None!"

#O(n)
#generates the numbers from 0 to n-1
def gen_lst(n):
    return [x for x in range(n)]

def print_follow(node):
    cur_node = node
    while cur_node != None:
        print cur_node.get_val()
        cur_node = cur_node.get_next()

def balance(input_lst,sorts):
    tail = None
    old_node = None

    for i in range(sorts):
        input_lst[i].prepend(old_node,tail)
#                    print_ll(sort_lst)
        old_node = input_lst[i].get_follow()
#                    print_follow(old_node)
        if old_node:
            tail = input_lst[i].get_tail()
#                        print "Tail: " + str(tail.get_val())

        input_lst[i].set_cannibal_head()
                        #sort_lst[i] = first
                        #prepend next with follow
    return sorts

def sort(input_lst):
    #O(n)
    #the structure of the list is a little complicated, and pretty important
    #[[value,next,head]
    sort_lst = [LList(Node(elt)) for elt in input_lst]
    lsts = 0
    sorts = 0
    for elt in sort_lst:
#        print "There are " + str(sorts) + " sorts"
#        print "There are " + str(lsts) + " lists."
#        print_ll(sort_lst)
        if lsts > 0:
#            print str((float(sorts) - float(lsts)) / float(lsts))
            if (float(sorts) - float(lsts)) / float(lsts) > LOAD:
#                print "load balance error"
                lsts = balance(sort_lst,sorts)


#        print "searching for " + str(elt.get_head().get_val())
        result = bin_search(sort_lst,elt.get_head(),0,lsts - 1)
#        print "result is " + str(result)
        if result + 1 >= lsts and lsts > 0 and sort_lst[lsts-1].get_tail().get_val()<elt.get_head().get_val():
            if sorts != lsts:
                sort_lst[lsts].set_head(sort_lst[sorts].get_head())
                sort_lst[sorts].set_head(None)
            lsts += 1

        elif result < 0:
            sort_lst[0].set_head(sort_lst[sorts].get_head())
            if sorts != 0:
                sort_lst[sorts].set_head(None)
            else:
                lsts += 1

        else:
            prev = sort_lst[result].get_head()
            
            #linear search
            while prev.get_next():
                cur = prev.get_next()
                if cur.get_val() > elt.get_head().get_val():
                    prev.set_next(elt.get_head())
                    elt.get_head().set_next(cur)
                    sort_lst[sorts].set_head(None)

#                    print "breaking!"
                    break
                else:
                    prev = cur

            if not prev.get_next():
                sort_lst[result].set_tail(elt.get_head())
                sort_lst[sorts].set_head(None)

        sorts += 1
#    lsts = balance(sort_lst,sorts)
#    print_ll(sort_lst)

def bin_search(input_lst, elt, lower, upper):
    #if we want to speed this up a little, we can return a tuple
    #that tells you if you precisely found your number
#    print str(lower) + " , " + str(upper)
    if lower >= upper:
        #needs to be more sophisticated
        if lower > upper:
#            print "Your hypothesis was wrong"
            pass

        #the hypothesis is that the only possible case is lower == upper
        used = 0
        if input_lst[upper]:
            used = upper
        else:
            used = upper + 1
 #       print used
        if elt.get_val() < input_lst[used].get_head().get_val():
#            print "smaller"
            return upper - 1
        else:
#            print "bigger"
            return upper

    else:
        #fetches the value of the head of the midval
        check = input_lst[(lower+upper)/2].get_head().get_val()
        if check < elt.get_val():
#            print str(check) + " too small"
            if (lower+upper)/2 != lower:
                return bin_search(input_lst,elt,(lower+upper)/2,upper)
            else:
                return bin_search(input_lst,elt,(lower+upper)/2 + 1,upper)
        elif check > elt.get_val():
#            print str(check) + " too big"
            if (lower+upper)/2 != upper:
                return bin_search(input_lst,elt,lower,(lower+upper)/2)
            else:
                return bin_search(input_lst,elt,lower,(lower+upper)/2 - 1)                
        else:
            return (lower+upper)/2


t1 = time.time()
sort(randomize(gen_lst(100000)))
t2 = time.time()
diff1 = t2-t1
print str(t2-t1)
ratio = 2*math.log(100000)/math.log(50000)

t1 = time.time()
sort(randomize(gen_lst(50000)))
t2 = time.time()
diff2 = t2-t1
print str(t2-t1)
print str(ratio)
print str(float(diff1)/float(diff2))


#in_lst = [0,1,2,3,4,5,6,7,8,3]

#sor_lst = [[[in_lst[i],-1],i] for i in range(len(in_lst))]

#print bin_search(sor_lst,9,0,9)
