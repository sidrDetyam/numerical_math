//
// Created by argem on 11.11.2022.
//
#include <iostream>
#include "BlasBasedMatrix.h"

using namespace task7;
using namespace boost::numeric;
using namespace std;

const double err = 0.00001;

std::vector<double> dig3mat(const BlasBasedMatrix&a,
                              const std::vector<double>& b){

    size_t n = b.size();
    std::vector<double> v(n), u(n), x(n);

    v[0] = - a(0 , 1) / a(0, 0);
    u[0] = b[0] / a(0, 0);
    v[n-1] = 0;
    u[n-1] = (a(n-1, n-2) * u[n-2] - b[n-1]) /
            (-a(n-1, n-1) - a(n-1, n-2)*v[n-2]);

    for(size_t i=1; i<n-1; ++i){
        v[i] = a(i, i+1) / (-a(i, i) - a(i, i-1)*v[i-1]);
        u[i] = (a(i, i-1)*u[i-1] -  b[i]) / (-a(i, i) - a(i, i-1)*v[i-1]);
    }

    x[n-1] = u[n-1];
    for(int64_t i=n-2; i>-1; --i){
        x[i] = v[i]*x[i+1] + u[i];
    }

    return x;
}


int main(){

    BlasBasedMatrix a(vector<vector<double>>({{2, -1, 0}, {-1, 2, -1}, {0, -1, 2}}));
    std::vector<double> b{2, 2, 2};

    auto x = dig3mat(a, b);
    for(double i : x){
        cout << i << " ";
    }
    cout << endl;

    return 0;
}
