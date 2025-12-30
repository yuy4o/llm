// 第二种方法完成6.cpp

# include <iostream>

using namespace std;

const int ArSize = 8;

int sum_arr(const int *begin, const int *end);

int main(void)
{
	int cookies[ArSize] = {1,2,4, 8,16,32,64,128};
  int sum = sum_arr(cookies, cookies+ArSize);
	cout << "Total cookies eaten: "<< sum << endl;
  int sum1 = sum_arr(cookies, cookies+3);
  cout << "The first three ate: " << sum1 << endl;
  int sum2 = sum_arr(cookies+4, cookies +8);
  cout << "The last four ate: " << sum2 <<endl;
  return 0;
}

int sum_arr(const int *begin, const int *end)
{
  int total = 0;
  const int *pt;
	for (pt=begin; pt != end; pt++)
		total += *pt;
	return total;
}
