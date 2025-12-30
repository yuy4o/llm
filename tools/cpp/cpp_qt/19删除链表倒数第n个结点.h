#pragma once

struct ListNode{
        int val;
        ListNode* next;
        ListNode(int x): val(x), next(nullptr){}
    };

ListNode* removeNthFromEnd(ListNode* head, int n) {
        ListNode* dummyHead = new ListNode(0);
        dummyHead->next = head;
        ListNode* fast = dummyHead;
        ListNode* slow = dummyHead;

        while (n-- && fast!=nullptr){
            fast = fast->next;
        }
        fast = fast->next;
        while (fast!=nullptr){
            fast = fast->next;
            slow = slow->next;
        }

        ListNode* temp = slow->next;
        slow->next = slow->next->next;
        delete temp; //释放内存

        return dummyHead->next;
    }
