//
// Created by argem on 21.10.2022.
//

#include <iostream>
#include "ludecomposer.h"

using namespace std;
using namespace task7;

int main(){

    LU a;
    ublas::matrix<double> b(4, 4);

    a.U = move(b);

    cout << "dsdds" << endl;

    return 0;
}