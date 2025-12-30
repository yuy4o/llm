#pragma once

class MyLinkedList
{
public:
    struct ListNode {
        int val;
        ListNode* next;
        ListNode(int x): val(x), next(std::nullptr){}
    };

    MyLinkedList() {
        dummyHead = new ListNode(0);
        size = 0;
    }// 构造函数

    int get(int index){
        if (index > (size-1) || index <0){
            return -1;
        }
        ListNode*cur = dummyHead->next;
        while(index--){
            cur = cur->next;
        }
        return cur->val;
    }

    void addAtHead(int val){
        ListNode* newnode = new ListNode(val);
        newnode->next = dummyHead->next;
        dummyHead->next =newnode;
        size++;
    }

    void addAtTail(int val){
        ListNode* newcode = new ListNode(val);
        ListNode* cur = dummyHead;
        while(cur->next!=nullptr){
            cur = cur->next;
        }
        cur->next = newcode;
        size++;
    }

    void addAtIndex(int index, int val){
        if (index > size) return; // 如果index等于链表的长度，则说明是新插入的节点为链表的尾结点
        if (index < 0) index =0;
        ListNode* newcode = new ListNode(val);
        ListNode* cur = dummyHead;
        while (index--){
            cur = cur->next;
        }// cur停在index-1处，确保index对应cur->next
        newcode->next = cur->next; //先右后左
        cur->next =newcode;
        size++;
    }

    void deleteAtIndex(int index){
        if(index>size-1 || index<0) return;
        ListNode* cur = dummyHead;
        while (index--){
            cur = cur->next;
        }
        ListNode* temp = cur->next;
        cur->next = cur->next->next;
        delete temp;
        size--;
    }

    void printLinkedList(){
        ListNode* cur = dummyHead;
        while (cur!=nullptr){
            std::cout << cur->val << " ";
            cur = cur->next;
        }
    }

    void test(){
        addAtHead(5);
        addAtTail(10);
        addAtIndex(2,100);
        deleteAtIndex(0);
        std::cout << get(1)<< std::endl;
        printLinkedList();
    }
private:
    int size;
    ListNode* dummyHead;
};

//int main(){
//    MyLinkedList().test(); //用构造函数实例化后调用成员函数
//}
