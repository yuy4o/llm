#pragma once
// 双指针
std::vector<int> sortedSquares(std::vector<int>& nums) {
    std::vector<int> result(nums.size(), 0);
    int i = 0;
    int j = nums.size()-1;
    int k = nums.size()-1;
    for (;i<=k;){
        if (nums[i]*nums[i] > nums[k]*nums[k]){
            result[j--] = nums[i]*nums[i];
            i++;
        }
        else{
            result[j--] = nums[k]*nums[k];
            k--;
        }
    }
    return result;
}
