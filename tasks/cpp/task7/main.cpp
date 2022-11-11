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


void bench(int argc, char** argv){
    int n = atoi(argv[1]);
    int is_parallel = atoi(argv[2]);
    int count_of_threads = argc==4? atoi(argv[3]) : 1;

    vector<vector<double>> vv(n);
    for(auto &i:vv){
        i = vector<double>(n);
        for(auto &j:i){
            j = rand() % 100;
        }
    }

    BlasBasedMatrix a(vv);
    LUDecomposer *lu_decomposer;
    ParallelLUDecomposer parallel_lu_decomposer(COUNT_OF_THREADS);
    SeqLUDecomposer seq_lu_decomposer;

    if(is_parallel){
        lu_decomposer = &parallel_lu_decomposer;
    }
    else{
        lu_decomposer = &seq_lu_decomposer;
    }
    lu_decomposer->decompose(a);

    exit(0);
}


int main(int argc, char** argv){

    bench(argc, argv);

    BlasBasedMatrix a(vector<vector<double>>({{1, 1, 1, 1}, {-1., 0, 1, 2}, {1, 0, 1, 4}, {-1, 0, 1, 8}}));
    std::vector<double> b{0, 0, 1, 0};

    ParallelLUDecomposer parallel_lu_decomposer(COUNT_OF_THREADS);

    auto lu = parallel_lu_decomposer.decompose(a);
    Base c =  lu.first * lu.second;
    cout << c << endl;
    cout << lu.first << endl << lu.second << endl;

    auto x = task7::LUDecomposer::solve(lu.first, lu.second, b);
    for(double i : x){
        cout << i << ' ';
        cout << endl;
    }

    return 0;
}
