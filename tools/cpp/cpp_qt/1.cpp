#include <iostream>
#include <vector>
#include <map>
using namespace std;

class Solution {
public:
    bool containsNearbyDuplicate(vector<int>& nums, int k) {
        int len = nums.size();
        vector<int> select;
        for (auto i : nums){
            auto ct = count(nums.begin(), nums.end(), i);
            if (select.empty()){
                select.push_back(i);
            } else{
                if (ct != 1 && !(*find(select.begin(), select.end(), i))){
                    select.push_back(i);
                }
            }

        }
        map<int, int> temp;
        for (int i = 0; i < len; i++){
            int x = nums[i];
            temp[i] = x;
        }
        map<int, int>::iterator it;

        for (auto s: select) {
            vector<int> t;
            for (it = temp.begin(); it != temp.end(); it++) {
                if (s == it->second){
                    t.push_back(it->first);
                }
            }
            for(auto t1 : t){
                for (auto t2 : t){
                    if (t1 != t2 && abs(t1 - t2) <= k) {
                        return true;
                    }
                }
            }
        }
        return false;
    }
};

int main() {
    Solution s;
    vector<int> vec = {1,2,3,1,2,3};
    cout << s.containsNearbyDuplicate(vec, 2);
}