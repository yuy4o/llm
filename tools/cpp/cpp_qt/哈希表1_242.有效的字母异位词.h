#pragma once

// 数组哈希表
bool isAnagram(std::string s, std::string t){
    int hash[26] = {0}; // 哈希数组
    int i;
    for (i = 0; i<s.size(); ++i){
        hash[s[i] - 'a']++; // 'a'类型是char，"a"是字符串，包含字符'a'和'\0'，类型是const char[2]
    }
    for (i = 0; i < t.size(); ++i){
        hash[t[i] - 'a']--;
    }
    for(i = 0; i < 26; ++i){
        if (hash[i] != 0){
            return false;
        }
    }
    return true;
}

// 用auto
// bool isAnagram(std::string s, std::string t){
//     int hash[26] = {0};
//     for (char i : s) hash[i - 'a']++;
//     for (char i : t) hash[i - 'a']--;
//     for (int i : hash) if (i != 0) return false;
//     return true;
// }


// 1.哈希表适合解决：判断一个元素是否出现在集合中/查询一个元素是否出现过
// 2.数组适合数据量小的。一千万个数就用set，”0，1，1000000“索引很大的也用set
//   直接使用set 不仅占用空间比数组大，而且速度要比数组慢，set把数值映射到key上都要做hash计算的
//   数组直接用下标做哈希映射，比set先通过哈希映射转成内部存储值+开辟空间，更快