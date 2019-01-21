# ------- #
# Imports #
# ------- #

from copy import copy
from simple_chalk import green, red
from types import SimpleNamespace as obj
from another_linked_list.index import LinkedList, node
from another_linked_list.fns import isLaden, joinWith, map_, passThrough
import os


# ---- #
# Init #
# ---- #

x = red("✘")
o = green("✔")


# ---- #
# Main #
# ---- #


def runTests():
    errors = passThrough(
        [], [testSuccess, testModifyMany, testSpecialMethods, testFail]
    )

    if isLaden(errors):
        errorOutput = passThrough(
            errors, [map_(prepend(f"{x} ")), joinWith(os.linesep)]
        )
        print(errorOutput)
    else:
        print(f"{o} all tests")


def testSuccess(errors):
    # list of size 1
    code = "len(LinkedList(['a']))"
    result = LinkedList(["a"])
    firstNode = result.firstNode
    passed = (
        firstNode is result.lastNode
        and firstNode.element == "a"
        and firstNode.previous is None
        and firstNode.next_ is None
    )
    if not passed:
        errors.append(code)

    # append
    code = "result.append('b'))"
    result = LinkedList(["a"])
    result.append("b")
    passed = isAToB(result)
    if not passed:
        errors.append(code)

    # prepend
    code = "result.prepend('a'))"
    result = LinkedList(["b"])
    result.prepend("a")
    passed = isAToB(result)
    if not passed:
        errors.append(code)

    # insertAfter
    code = "result.insertAfter(nodeWithA, 'b'))"
    result = LinkedList(["a", "c"])
    nodeA = result.firstNode
    result.insertAfter(nodeA, "b")
    passed = isAToBToC(result)
    if not passed:
        errors.append(code)

    # insertBefore
    code = "result.insertBefore(nodeWithC, 'b'))"
    result = LinkedList(["a", "c"])
    nodeC = result.lastNode
    result.insertBefore(nodeC, "b")
    passed = isAToBToC(result)
    if not passed:
        errors.append(code)

    # findFirstNode
    code = "result.findFirstNode('b')"
    result = LinkedList(["a", "b", "c"])
    nodeB = result.firstNode.next_
    passed = result.findFirstNode("b") is nodeB
    if not passed:
        errors.append(code)

    # removeFirstElement
    code = "result.removeFirstElement('c')"
    result = LinkedList(["a", "c", "b"])
    passed = isAToB(result.removeFirstElement("c"))
    if not passed:
        errors.append(code)

    # removeNode
    code = "result.removeNode(nodeWithC)"
    result = LinkedList(["a", "c", "b"])
    nodeC = result.firstNode.next_
    passed = isAToB(result.removeNode(nodeC))
    if not passed:
        errors.append(code)

    return errors


def testModifyMany(errors):
    # appendAll
    code = "result.appendAll(['b', 'c']))"
    result = LinkedList(["a"])
    result.appendAll(["b", "c"])
    passed = isAToBToC(result)
    if not passed:
        errors.append(code)

    # prependAll
    code = "result.prependAll(['a', 'b']))"
    result = LinkedList(["c"])
    result.prependAll(["a", "b"])
    passed = isAToBToC(result)
    if not passed:
        errors.append(code)

    # insertAllAfter
    code = "result.insertAllAfter(nodeWithA, ['b', 'c']))"
    result = LinkedList(["a", "d"])
    nodeA = result.firstNode
    result.insertAllAfter(nodeA, ["b", "c"])
    passed = isAToBToCToD(result)
    if not passed:
        errors.append(code)

    # insertAllBefore
    code = "result.insertAllBefore(nodeWithD, ['b', 'c']))"
    result = LinkedList(["a", "d"])
    nodeD = result.lastNode
    result.insertAllBefore(nodeD, ["b", "c"])
    passed = isAToBToCToD(result)
    if not passed:
        errors.append(code)

    return errors


def testFail(errors):
    # validate input
    code = "LinkedList(1)"
    try:
        LinkedList(1)
        errors.append(code)
    except Exception as e:
        expected = "aList is not an instance of list"
        if expected not in str(e):
            errors.append(code)

    # findFirstNode
    code = "LinkedList().findFirstNode('doesnt exist')"
    try:
        LinkedList().findFirstNode("doesnt exist")
        errors.append(code)
    except Exception as e:
        expected = "The element passed does not exist in this linked list"
        if expected not in str(e):
            errors.append(code)

    # removeFirstElement
    code = "LinkedList().removeFirstElement('doesnt exist')"
    try:
        LinkedList().removeFirstElement("doesnt exist")
        errors.append(code)
    except Exception as e:
        expected = "The element passed does not exist in this linked list"
        if expected not in str(e):
            errors.append(code)

    # validate node: element missing
    code = "LinkedList().insertAfter(nodeWithoutEl)"
    try:
        nodeWithoutEl = obj(next_=node("d"), previous=node("a"))
        ll = LinkedList()
        ll.insertAfter(nodeWithoutEl, "c")
        errors.append(code)
    except Exception as e:
        expected = "node has no attribute 'element'"
        if expected not in str(e):
            errors.append(code)

    # validate node: next_ missing
    code = "LinkedList().insertAfter(nodeWithoutNext)"
    try:
        nodeWithoutNext = obj(element="b", previous=node("a"))
        ll = LinkedList()
        ll.insertAfter(nodeWithoutNext, "c")
        errors.append(code)
    except Exception as e:
        expected = "node has no attribute 'next_'"
        if expected not in str(e):
            errors.append(code)

    # validate node: previous missing
    code = "LinkedList().insertAfter(nodeWithoutPrev)"
    try:
        nodeWithoutPrev = obj(element="b", next_=node("d"))
        ll = LinkedList()
        ll.insertAfter(nodeWithoutPrev, "c")
        errors.append(code)
    except Exception as e:
        expected = "node has no attribute 'previous'"
        if expected not in str(e):
            errors.append(code)

    # validate node: not in linked list
    code = "LinkedList().insertAfter(nodeNotInList)"
    try:
        nodeNotInList = obj(element="b", next_=node("d"), previous=node("a"))
        ll = LinkedList()
        ll.insertAfter(nodeNotInList, "c")
        errors.append(code)
    except Exception as e:
        expected = "The node given is not in this linked list, thus you cannot"
        if expected not in str(e):
            errors.append(code)

    return errors


def testSpecialMethods(errors):
    # __len__
    code = "len(LinkedList(['a']))"
    result = LinkedList(["a"])
    passed = len(result) == 1
    if not passed:
        errors.append(code)

    # __iter__
    code = "for el in LinkedList(['a', 'b'])"
    aList = ["a", "b"]
    result = []
    for el in LinkedList(aList):
        result.append(el)

    passed = aList == result
    if not passed:
        errors.append(code)

    # __reversed__
    code = "for el in reversed(LinkedList(['a', 'b']))"
    result = []
    for el in reversed(LinkedList(["b", "a"])):
        result.append(el)

    passed = result == ["a", "b"]
    if not passed:
        errors.append(code)

    # __copy__
    code = "copy(LinkedList(['a1', 'b']))"
    original = LinkedList(["a1", "b"])
    result = copy(original)
    result.firstNode.element = "a2"
    passed = original is not result and original.firstNode.element == "a1"
    if not passed:
        errors.append(code)

    return errors


# ------- #
# Helpers #
# ------- #


def prepend(leftStr):
    def prepend_inner(rightStr):
        return leftStr + rightStr

    return prepend_inner


def isAToB(result):
    return (
        len(result) == 2
        and result.lastNode.element == "b"
        and result.lastNode.previous.element == "a"
        and result.firstNode.next_ is result.lastNode
        and result.lastNode.previous is result.firstNode
    )


def isAToBToC(result):
    return (
        len(result) == 3
        and result.lastNode.element == "c"
        and result.lastNode.previous.element == "b"
        and result.lastNode.previous.previous.element == "a"
        and result.firstNode.next_.next_ is result.lastNode
        and result.lastNode.previous.previous is result.firstNode
    )


def isAToBToCToD(result):
    return (
        len(result) == 4
        and result.lastNode.element == "d"
        and result.lastNode.previous.element == "c"
        and result.lastNode.previous.previous.element == "b"
        and result.lastNode.previous.previous.previous.element == "a"
        and result.firstNode.next_.next_.next_ is result.lastNode
        and result.lastNode.previous.previous.previous is result.firstNode
    )
