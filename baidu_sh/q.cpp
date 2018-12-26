#include <iostream>
#include <stdio.h>
#include "q.h"
#include <vector>
using namespace std;


void myfunction (int* q) {  // function:
    cout << "print myfunction\b" << q <<endl;
}
class Box
{
   public:
       int length;   // 长度
       double breadth;  // 宽度
       double height;   // 高度
};
int test (){
    int *a;
    cout << &a << "test one" <<endl;
    Box Box1;
    Box1.length = 10.1;
    cout << Box1.length<< endl;
    return 0;
}

int main () {
    // 指针
    int a = 666;
    int *wal = &a;
    cout << "wal" << wal <<endl;
    cout << "*wal" << *wal <<endl;
    // 引用
    int b = 88888;
    int &q = b;
    cout << q << endl;
    myfunction(&a);


    int nArray[] = {0, 1, 2, 3, 4, 5};  
    std::vector<int> vecNum(nArray, nArray + 6);  
    //CString strText;  
    std::vector<int> c;
    // 第一种用法：最原始的语法(用下标)  
    for (size_t i = 0; i < vecNum.size(); ++i)  
    {  
        cout << nArray[i] << endl;
        c.push_back(nArray[i]);
    }; 
    cout << c.size()<<"size" <<endl;
    //// 第二种用法：最原始的语法(用迭代器)  
    //for (iterator it = vecNum.begin(); it != vecNum.end(); ++it)  
    //{  
    //    cout << *it << endl;
    //}  
    //vector<int> (10,1);
    //for(vector<int>::iterator iter=ivec.begin();iter!=ivec.end();++iter)
    //vector 循环
    for(vector<int>::iterator iter=c.begin();iter!=c.end();++iter)
    {
        //*iter=2; 
        cout << *iter << endl;
    };
    test();
    return 0;
}
