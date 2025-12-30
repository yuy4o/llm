#pragma once

// 滑动窗口
int minSubArrayLen(int target, std::vector<int>& nums) {
    int size = nums.size();
    int result = INT32_MAX;
    int sum = 0; // 滑动窗口数值之和
    int start = 0; // 滑动窗口起点
    int subLength = 0; // 滑动窗口长度
    int end = 0;
    for (;end<size;end++){
        sum += nums[end];
        while (sum >= target){
            subLength = end - start +1;
            result = result < subLength ? result:subLength;
            sum -= nums[start++];
        }
    }
    return result == INT32_MAX ? 0:result; // result没被赋值返回0
}
