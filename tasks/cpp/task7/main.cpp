//
// Created by argem on 21.10.2022.
//

#include <iostream>
#include "ludecomposer.h"

using namespace task7;
using namespace boost::numeric;
using namespace std;

int main(int argc, char** argv){

    int n = 3000;
    vector<vector<double>> vv(n);
    for(auto &i:vv){
        i = vector<double>(n);
        for(auto &j:i){
            j = rand() % 100;
        }
    }

    BlasBasedMatrix a(vv);//(vector<vector<double>>({{1., 2, 3}, {4., 5, 6}, {7., 9, 9}}));


    //LUDecomposer luDecomposer;
    ParallelLUDecomposer luDecomposer(4);
    auto lu = luDecomposer.decompose(a);
    //Base c =  prod(lu.first, lu.second);
    //cout << c << endl;
    //operator<<(cout, lu.first) << endl << lu.second << endl;

    return 0;
}