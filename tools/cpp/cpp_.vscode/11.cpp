#include <iostream>
#include <vector>

class Solution {
public:
    int func(std::vector<int>& nums) {
        // nums[j]结尾的数组的最长严格递增子序列的长度为dp[j]
        // 每一个i，对应的dp[i]（即最长递增子序列）起始大小至少是1
        std::vector<int> dp(nums.size(), 1);
        // 此处的res包括上一行全部初始化成1 因为最长严格递增子序列的长度至少为1
        int res=1; 
        for (int j=1;j<nums.size();j++){
            for(int i=0;i<j;i++)
                if (nums[j]>nums[i])
                    dp[j] = std::max(dp[i]+1, dp[j]);
            res = std::max(res, dp[j]);// 错误 res写到内层循环里
        }
        return res;
    }
};

int main(){
    std::vector<int> x = {10, 9, 2, 5, 3, 7, 101, 18};
    Solution sol;
    std::cout << sol.func(x) << std::endl;
}