#pragma once

int fourSumCount(std::vector<int>& nums1, std::vector<int>& nums2, std::vector<int>& nums3, std::vector<int>& nums4) {
    std::unordered_map <int, int> umap;
    for (int a: nums1){
        for (int b: nums2){
            umap[a+b]++; // umap[key]= value  数组[key索引]=元素，生成哈希表
        }
    }
    int count = 0;
    // 在哈希表中查找
    for (int c: nums3){
        for (int d: nums4){
            if (umap.find(0-(c+d))!=umap.end()){
                count += umap[0-(c+d)];
            }
        }

    }
    return count;
}