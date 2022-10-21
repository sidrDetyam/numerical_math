//
// Created by argem on 21.10.2022.
//

#ifndef TASK8_LUDECOMPOSER_H
#define TASK8_LUDECOMPOSER_H

#include <boost/numeric/ublas/vector.hpp>
#include <boost/numeric/ublas/matrix.hpp>

namespace task7 {

    using namespace boost::numeric;
    struct LU{
        ublas::matrix<double> u;

        explicit LU(ublas::matrix<double> &&u): u(u){
        }

        double& operator()(int i, int j){
            return u(i, j);
        }
    };

    class LU_decomposer {
    public:
        LU compute(const ublas::matrix<double> &a){
            ublas::matrix<double> u = a;
            unsigned long n = a.size1();

            ublas::vector<double> v;
            v.

            for(int i=0; i<n; ++i){
                for(int j=i+1; j<n; ++j){
                    for(int )
                }
            }
        }
    };

}

#endif //TASK8_LUDECOMPOSER_H
