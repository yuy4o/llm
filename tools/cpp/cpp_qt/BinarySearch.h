#pragma once
int BinarySearch(std::vector<int>& nums, int target, int left, int right){
    while (left <= right){
        int mid = left +(right-left)/2;
        if (nums[mid] == target){
            return mid;
        }
        else if(nums[mid] < target){
            left = mid+1;
        }
        else right = mid-1;
    }
    return -1;
}
