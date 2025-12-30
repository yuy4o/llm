#pragma once

struct ListNode{
    int val;
    ListNode* next;
    ListNode(int x): val(x), next(nullptr){}
};

ListNode *detectCycle(ListNode *head) {
    ListNode* fast = head;
    ListNode* slow = head;
    while(fast!=nullptr && fast->next!=nullptr){
        fast = fast->next->next;
        slow = slow->next;
        if (fast == slow){
            ListNode* index1 = fast;
            ListNode* index2 = head;
            while (index1 != index2){
                index1 = index1->next;
                index2 = index2->next;
            }
            return index1;
        }
    }
    return nullptr;
}


//int main() {
//    ListNode* fourth = new ListNode(4);
//    ListNode* third = new ListNode(0);
//    ListNode* second = new ListNode(2);
//    ListNode* first = new ListNode(3);

//    first->next = second;
//    first->next->next = third;
//    first->next->next->next =fourth;
//    first->next->next->next->next =second;

//    ListNode* res = detectCycle(first);
//    cout << res->val;
//}
