#include <iostream>

class Solution{
public:
    int search(std::vector<int>nums, int target){
        int left = 0, right = nums.size() -1;
        while (left <= right){
            int mid = (right +left)/2;
            if (nums[mid] == target) return mid;
            else if (nums[mid] > target) right = mid-1;
            else left = mid +1;
        }
        return -1;
    }
} example;


int main()
{
    std::vector<int> vec = {1,2,4};
    for (auto i:vec) std::cout << i << std::endl;

    std::cout << example.search(vec, 0) << std::endl;
//    ListNode* l;
//    l->val = 3;
//    l->next = nullptr;
//    std::cout << l->val << std::endl;
//    return 0;
}
