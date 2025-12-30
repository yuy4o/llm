#pragma once

// Definition for singly-linked list.
struct ListNode {
    int val;
    ListNode* next;
    ListNode(int x): val(x), next(nullptr){} // ListNode() : val(0), next(nullptr) {}
    ListNode(int x, ListNode *next) : val(x), next(next) {}
};

// 法一分类讨论
ListNode* removeElements1(ListNode* head, int val){
    // 删除头结点
    while(head!=nullptr&&head->val==val){
        ListNode* temp = head;
        head = head->next;
        delete temp;
    }
    // 删除非头结点
    ListNode* cur = head;
    while(cur!=nullptr && cur->next!=nullptr){
        if (cur->next->val==val){
            ListNode* temp = cur->next;
            cur->next = cur->next->next;
            delete temp;
        }else{
            cur = cur->next;
        }
    }
    return head;
}

// 法二虚拟头结点
ListNode* removeElements2(ListNode* head, int val){
    ListNode* dummyHead = new ListNode(0, head);
    ListNode* cur = dummyHead;
    while(cur->next!=nullptr){
        if (cur->next->val == val){
            ListNode* temp = cur->next;
            cur->next = cur->next->next;
            delete temp;
        } else{
            cur = cur->next;
        }
    }
    head = dummyHead->next;// 原head位置会变，遍历时要定义临时指针，不要动head
    delete dummyHead;
    return head;
}
