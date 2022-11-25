#include <iostream>
#include "../task7/BlasBasedMatrix.h"

using namespace task7;
using namespace boost::numeric;
using namespace std;

double norm(const ublas::vector<double>& v){
    double res = abs(v(0));
    for(auto i : v){
        res = max(res, abs(i));
    }
    return res;
}

const double err = 0.001;

ublas::vector<double> jacobi(const BlasBasedMatrix&a,
                             const ublas::vector<double>& b0,
                             const ublas::vector<double>& x0){

    assert(a.size1() == a.size2() && a.size1() == x0.size());
    BlasBasedMatrix d(a.size1(), a.size1());
    BlasBasedMatrix d1(a.size1(), a.size1());
    for(size_t i=0; i<d.size1(); ++i){
        for(size_t j=0; j<d.size1(); ++j){
            d(i, j) = i==j? a(i, j) : 0;
            assert(a(i, j));
            d1(i, j) = i==j? 1/a(i, j) : 0;
        }
    }

    BlasBasedMatrix b = d1 * (d - a);
    ublas::vector<double> g = d1 * b0;
    ublas::vector<double> x(x0), x_next;

    for(;;){
        x_next = b * x + g;
        double n = norm(x_next - x);
        x = x_next;

        for(double i : x){
            cout << i << ' ';
        }
        cout << endl;
        sleep(1);

        if(n < err){
            break;
        }
    }

    return x;
}


int main(){

    BlasBasedMatrix a(vector<vector<double>>({{1, 0.5, 0.333}, {0.5, 0.333, 0.25}, {0.333, 0.25, 0.2}}));
    ublas::vector<double> b(3);
    b(0) = 2; b(1) = 2; b(2) = 2;
    ublas::vector<double> x0(3);
    x0(0) = 6.0; x0(1) = -48; x0(2) = 60;

    auto x = jacobi(a, b, x0);
    for(int i=0; i<x.size(); ++i){
        cout << x(i) << " ";
    }

    auto check = a * x;
    for(double i:check){
        cout << i << " ";
    }
    cout << endl;

    return 0;
}