#pragma once

struct ListNode{
    int val;
    ListNode* next;
    ListNode(int x): val(x), next(nullptr){}
};

// 双指针
ListNode* reverseList(ListNode* head) {
    ListNode* cur = head;
    ListNode* pre = nullptr;
    ListNode* temp;
    while(cur!=nullptr){
        temp = cur->next; // 让temp指针（左边）指向cur->next（右边）
        // 换向
        cur->next = pre;
        // 将pre和cur一起向后移动
        pre = cur; // 让pre指针指向当前cur的位置
        cur = temp;// 让cur指针指向当前temp的位置
    }
    return pre;
}

// 递归法
ListNode* reverse(ListNode*pre, ListNode*cur){
    if(cur==nullptr) return pre;
    ListNode* temp = cur->next;
    cur->next = pre;
    return reverse(cur, temp);
}

ListNode* reverseList2(ListNode* head) {
    return reverse(nullptr, head);
}
