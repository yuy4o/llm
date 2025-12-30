#pragma once
std::vector<std::vector<int>> generateMatrix(int n) {
    std::vector<std::vector<int>> res(n, std::vector<int>(n,0));//初始化可以不取名
    int loop = n/2; // 循环几圈
    int offset = 1; // 末尾截断
    int count = 1; // 计数
    int startx =0, starty = 0;
    int mid = n/2; // n为奇数的中心点
    int i, j;
    while (loop--){
        i = startx;
        j = starty;
        for(j = starty; j< n-offset; j++){
            res[startx][j] = count++;
        }
        for(i = startx; i < n-offset; i++){
            res[i][j] = count++;
        }
        for(;j>starty;j--){
            res[i][j] = count++;
        }
        for(;i>startx;i--){
            res[i][j] = count++;
        }
        offset++;
        startx++;
        starty++;
    }
    if (n%2){
        res[mid][mid] = count;
    }
    return res;
}
