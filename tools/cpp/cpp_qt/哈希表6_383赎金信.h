#pragma once

// 数组作为哈希表
bool canConstruct(std::string ransomNote, std::string magazine) {
    int record[26] = {0};
    int mag_size = magazine.size(), ran_size = ransomNote.size();
    if (mag_size < ran_size) return false;
    for (int i = 0; i < mag_size; ++i){
        record[magazine[i]-'a']++;
    }
    for (int j = 0; j < ran_size; ++j)
    {
        record[ransomNote[j]-'a']--;
        if (record[ransomNote[j]-'a'] < 0){
            return false;
        }
    }
    return true;
}

// 暴力解法
// bool canConstruct(std::string ransomNote, std::string magazine) {
//     int mag_size = magazine.size(), ran_size = ransomNote.size();
//     for (int j = 0; j < mag_size; j++){
//         for (int i = 0; i < ran_size; i++){
//             if (ransomNote[i] == magazine[j]){
//                 ransomNote.erase(ransomNote.begin() + i);
//                 break;
//             }
//         }
//     }
//     if (ransomNote.size() == 0){ // 不能用ran_size，恒为正
//         return true;
//     }
//     return false;
// }