# Stack Module

class Node:
    def __init__(self, item, link):
        self.item = item
        self.next = link


class StackLink:
    def __init__(self):
        self.top = None
        self.size = 0

    def push(self, item):
        self.top = Node(item, self.top)
        self.size += 1

    def pop(self):
        if self.size != 0:
            temp = self.top.item
            self.top = self.top.next
            self.size -= 1
        return temp

    def print_stack(self):
        p = self.top
        while p:
            if p.next != None:
                print(p.item, '-->', end = '')
            else:
                print(p.item, end = '')
            p = p.next
        print()


if __name__ == "__main__":
    top = StackLink()
    top.push("apple")
    top.push("mango")
    top.push("cherry")
    top.push("banana")
    top.pop()

    top.print_stack()
