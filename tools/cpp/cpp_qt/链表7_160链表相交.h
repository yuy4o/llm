#pragma once

struct ListNode{
    int val;
    ListNode* next;
    ListNode(int x): val(x), next(nullptr){}
};

ListNode *getIntersectionNode(ListNode *headA, ListNode *headB) {
    ListNode* curA = headA;
    ListNode* curB = headB;
    int lenA = 0, lenB = 0;
    while (curA!=nullptr){
        lenA++;
        curA = curA->next;
    }
    while (curB!=nullptr){
        lenB++;
        curB = curB->next;
    }
    curA = headA;
    curB = headB;
    if (lenA < lenB){
        std::swap(lenA, lenB);
        std::swap(curA, curB);
    }
    int gap = lenA-lenB;
    while(gap--){
        curA = curA->next;
    }
    while(curA!=nullptr){
        // 两个链表的交点（引用完全相同，即：内存地址完全相同的交点）
        if(curA == curB){ //不是curA->val == curB->val，指针相同包括值和地址都要相同
            return curA;
        }
        curA = curA->next;
        curB = curB->next;
    }
    return nullptr;
}

// 测试，若curA->val == curB->val输出 1，8，4，5
//int main() {
//    // 链表初始化方式, new加构造函数
//    ListNode* fifth = new ListNode(5);
//    ListNode* fourth = new ListNode(4);
//    ListNode* third = new ListNode(8);
//    ListNode* second = new ListNode(1);
//    ListNode* first = new ListNode(4);
//    ListNode* one = new ListNode(5);
//    ListNode* two = new ListNode(0);
//    ListNode* three = new ListNode(1);


//    first->next = second;
//    first->next->next = third;
//    first->next->next->next =fourth;
//    first->next->next->next->next =fifth;

//    one->next = two;
//    two->next = three;
//    three->next = third;

//    first = getIntersectionNode(first, one);
//    while (first!=nullptr){
//        cout << first->val <<" ";
//        first =first->next;
//    }
//}
