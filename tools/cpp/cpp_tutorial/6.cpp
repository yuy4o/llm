# include <iostream>

using namespace std;

const int ArSize = 8;

int sum_arr(int arr[], int n);

int main(void)
{
	int cookies[ArSize] = {1,2,4, 8,16,32,64,128};
  cout << "cookies address is " << cookies << endl;
  cout << "size of cookies is "<< sizeof cookies <<endl;
  int sum = sum_arr(cookies, ArSize);
	cout << "Total cookies eaten: "<< sum << endl;
  int sum1 = sum_arr(cookies, 3);
  cout << "The first three ate: " << sum1 << endl;
  int sum2 = sum_arr(cookies+4, 4);
  cout << "The last four ate: " << sum2 <<endl;
  return 0;
}

int sum_arr(int arr[], int n)
{
	cout << "arr adress is " << arr <<endl;
  cout << "size of arr is "<< sizeof arr <<endl;
 
  int total = 0;
	for (int i = 0; i <  n; i++)
		total += arr[i];
	return total;
}
