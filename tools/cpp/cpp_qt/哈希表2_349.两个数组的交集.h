#pragma once

// 用set作为哈希表，针对大容量nums1，效率没有数组哈希表高
// std::vector<int> intersection(std::vector<int>& nums1, std::vector<int>& nums2) {
//     std::unordered_set<int> result_set;
//     // 先把nums1处理/映射成哈希表，把nums2放到哈希表里查询，输出结果
//     // unordered_set看成无限存装的数组
//     std::unordered_set<int> nums_set(nums1.begin(), nums1.end());
//     for (int num : nums2){
//         if (nums_set.find(num) != nums_set.end()){
//             result_set.insert(num);
//         }
//     }
//     return std::vector<int>(result_set.begin(), result_set.end());
// }

// 用数组作为哈希表（已知nums1数据种类在1000以内）
std::vector<int> intersection(std::vector<int>& nums1, std::vector<int>& nums2) {
    std::unordered_set<int> result_set;
    int hash[1004] = {0};
    for (int num : nums1){
        hash[num] = 1; 
    }
    for (int num : nums2){
        if (hash[num] == 1){
            result_set.insert(num);
        }
    }
    return std::vector<int> (result_set.begin(), result_set.end());
}

// 暴力解法
// std::vector<int> intersection(std::vector<int>& nums1, std::vector<int>& nums2) {
//     std::vector<int> res;
//     int i, j, k, h;
//     for (i=0; i < nums1.size(); i++){
//         for (j=0; j < nums2.size(); j++){
//             if (nums1[i]==nums2[j]){
//                 res.push_back(nums1[i]);
//             }
//         }
//     }
//     sort(res.begin(), res.end());
//     auto it = unique(res.begin(), res.end());
//     res.erase(it, res.end());
//     return res;
// }
