#pragma once

// 用unordered_map作为哈希表
std::vector<int> twoSum(std::vector<int>& nums, int target) {
    std::unordered_map<int, int> result_map;
    int size = nums.size();
    for (int i = 0; i < size; i++){
        auto it = result_map.find(target - nums[i]);
        if (it != result_map.end()){
            return {it->second, i};
        }
        result_map.insert(std::pair<int, int>(nums[i], i));     
    }
    return {};
}

// 暴力O(n^2)
// std::vector<int> twoSum(std::vector<int>& nums, int target) {
//     int size = nums.size();
//     std::vector<int> res;
//     for (int i = 0; i < size; i++){
//         for (int j = i; j < size; j++){
//             if ((i != j) && nums[i] + nums[j] == target){
//                 res.push_back(i);
//                 res.push_back(j);
//             }
//         }
//     }
//     return res;
// }