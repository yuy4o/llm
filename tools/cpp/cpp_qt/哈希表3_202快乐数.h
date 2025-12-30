#pragma once

int getSum(int n){
    int sum = 0;
    while (n){
        sum += (n % 10) * (n % 10);
        n = n/10; 
    }
    return sum;
}


bool isHappy(int n) {
    std::unordered_set<int> result_set;
    while (1){
        int sum = getSum(n);
        if (sum == 1) return true;
        // 哈希表查找之前是否出现过
        if(result_set.find(sum) == result_set.end()){
            result_set.insert(sum);
        }
        else{
            return false;
        }
    n = sum;
    }
}