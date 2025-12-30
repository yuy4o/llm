#pragma once
int removeElement(std::vector<int>& nums, int val) {
    int s = 0;
    int l = 0;
    for (;l<nums.size();l++){
        if(nums[l] != val){
            nums[s++] = nums[l]; //双指针
        }
    }
    return s;
}
