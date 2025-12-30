#pragma once

ListNode* swapPairs(ListNode* head) {
    ListNode* dummyHead = new ListNode(0);
    ListNode* cur = dummyHead;
    dummyHead->next = head;
    // &&前后顺序不能交换，cur->next为nullptr时cur->next->next会报空指针错误
    while (cur->next!=nullptr&&cur->next->next!=nullptr) {
        ListNode*temp = cur->next;
        ListNode*temp1 = cur->next->next->next;

        // cur位置固定，把保存的temp值赋给cur->next，cur->next->next和cur->next->next->next
        cur->next = cur->next->next;
        cur->next->next = temp;
        cur->next->next->next = temp1;

        cur = cur->next->next;
    }
    return dummyHead->next;
}
