// const int *pt;
// int *const pt;
// const int *const pt;

#include <iostream>

using namespace std;

int main()
{
  int n =10;
  int m = 100;
  const int *pt = &n;

  cout << "1) n = "<<n << endl;
 // *pt = 20;
  pt = &m;
  cout << "2) n = "<<n << endl;
  cout << "*pt = " <<*pt<<endl;
  cout << "m = " << m <<endl;
  return 0;
}













