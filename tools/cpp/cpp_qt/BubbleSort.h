#pragma once

std::vector<int> BubbleSort(std::vector<int> nums){
    int size = nums.size();
    int i = 0;
    for(;i<size-1;i++){
        int j = 0;
        for(;j<size-1-i;j++){
            if(nums[j]>nums[j+1]){
                std::swap(nums[j], nums[j+1]);
            }
        }
    }
    return nums;
}
