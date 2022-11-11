//
// Created by argem on 21.10.2022.
//

#include <iostream>
#include "ludecomposer.h"

using namespace task7;
using namespace boost::numeric;
using namespace std;


enum{
    COUNT_OF_THREADS = 4
};


int main(int argc, char** argv){

//    int n = atoi(argv[1]);
//    int is_parallel = atoi(argv[2]);
//    int count_of_threads = argc==4? atoi(argv[3]) : 1;
//
//    vector<vector<double>> vv(n);
//    for(auto &i:vv){
//        i = vector<double>(n);
//        for(auto &j:i){
//            j = rand() % 100;
//        }
//    }

    BlasBasedMatrix a(vector<vector<double>>({{4., -1, -1}, {-1., 4, -1}, {-1., -1, 4}}));
    std::vector<double> b{2, 2, 2};

    ParallelLUDecomposer parallel_lu_decomposer(COUNT_OF_THREADS);
    SeqLUDecomposer seq_lu_decomposer;

    LUDecomposer *lu_decomposer;
    lu_decomposer = &parallel_lu_decomposer;

//    if(is_parallel){
//        lu_decomposer = &parallel_lu_decomposer;
//    }
//    else{
//        lu_decomposer = &seq_lu_decomposer;
//    }

    auto lu = lu_decomposer->decompose(a);
    Base c =  prod(lu.first, lu.second);
    cout << c << endl;
    cout << lu.first << endl << lu.second << endl;

    auto x = task7::LUDecomposer::solve(lu.first, lu.second, b);
    for(double i : x){
        cout << i << ' ';
        cout << endl;
    }

    return 0;
}
