// 看const在*的前还是后
// const int *pt; == int const *pt  pt指针可以指向任何修改对象，但不能修改指向对象的值
// int *const pt; pt指针可以修改指向对象的值，但只能指向一个对象
// const int *const pt; pt指针只能指向一个对象，且不能修改指向对象的值

#include <iostream>

using namespace std;

int main()
{
  int n =10;
  int m = 100;
  // const int *pt = &n;
  int *const pt =&n; 

  cout << "1) n = "<<n << endl;
 // *pt = 20;
 // pt = &m;
  cout << "2) n = "<<n << endl;
  cout << "*pt = " <<*pt<<endl;
  cout << "m = " << m <<endl;
  return 0;
}













