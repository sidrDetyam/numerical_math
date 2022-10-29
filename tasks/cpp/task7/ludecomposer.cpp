//
// Created by argem on 21.10.2022.
//

#include <boost/asio/post.hpp>
#include "ludecomposer.h"

using namespace boost;
using namespace task7;

std::pair<BlasBasedMatrix, BlasBasedMatrix> LUDecomposer::decompose(const BlasBasedMatrix &a) {
    assert(a.size1() == a.size2());

    const size_t n = a.size1();
    BlasBasedMatrix u(a);
    BlasBasedMatrix l = BlasBasedMatrix::id(n);

    for (size_t i = 0; i < n; ++i) {
        for (size_t j = i + 1; j < n; ++j) {
            double c = -u(j, i) / u(i, i);
            u.daxpy(&u(i, 0), j, c);
            l(j, i) = -c;
        }
    }
    return std::make_pair(std::move(l), std::move(u));
}


static std::function<void()> fork_(boost::asio::thread_pool &pool, BlasBasedMatrix &u, BlasBasedMatrix &l,
                        std::vector<std::tuple<std::mutex, std::condition_variable, int>> &v, size_t i){
    using namespace std;

    return [i, &pool, &u, &l, &v](){
        for (size_t j = i + 1; j < u.size1(); ++j) {
            if(j == i+1) {
                lock_guard<mutex>(get<0>(v[i]));
            }
            std::unique_lock<mutex> lk(get<0>(v[j]));

            while(get<2>(v[j]) != i){
                get<1>((v[j])).wait(lk);
            }

            double c = -u(j, i) / u(i, i);
            u.daxpy(&u(i, 0), j, c);
            l(j, i) = -c;
            ++get<2>(v[j]);
            get<1>((v[j])).notify_all();

            if(get<2>(v[j]) == j){
                boost::asio::post(pool, fork_(pool, u, l, v, j));
            }

        }
    };
}


std::pair<BlasBasedMatrix, BlasBasedMatrix> ParallelLUDecomposer::decompose(const BlasBasedMatrix &a) {
    assert(a.size1() == a.size2());
    using namespace std;

    BlasBasedMatrix u(a);
    BlasBasedMatrix l = BlasBasedMatrix::id(a.size1());
    vector<tuple<mutex, std::condition_variable, int>> v(a.size1());

    mutex m;
    boost::asio::post(pool, fork_(pool, u, l, v, 0));
    pool.join();

    return std::make_pair(std::move(l), std::move(u));
}
