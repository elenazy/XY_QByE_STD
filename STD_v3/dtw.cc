// dtw.cc

// Copyright 2017  ASLP (Author: jyhou@nwpu-aslp.org)

// See ../../COPYING for clarification regarding multiple authors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//  http://www.apache.org/licenses/LICENSE-2.0
//
// THIS CODE IS PROVIDED *AS IS* BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION ANY IMPLIED
// WARRANTIES OR CONDITIONS OF TITLE, FITNESS FOR A PARTICULAR PURPOSE,
// MERCHANTABLITY OR NON-INFRINGEMENT.
// See the Apache 2 License for the specific language governing permissions and
// limitations under the License.

#include "dtw.h"
#include "distance.h"
namespace aslp_std {
    
float DTW(const infra::matrix &dist) {
    unsigned long height = dist.height();
    unsigned long width = dist.width();
    infra::matrix cost(height+1, width+1);
    infra::matrix length(height+1, width+1);
    cost(0,0) = 0.0;
    length(0,0) = 1;
    for (int i=1; i < height+1; i++) {
        cost(i, 0) = BIG_FLT;
        length(i, 0) = 1;
    }
    for (int j=1; j < width+1; j++) {
        length(0, j) = 1;
        cost(0, j) = BIG_FLT;
    }
    for (int i=1; i < height+1; i++) {
        for (int j=1; j < width+1; j++) {
            if (cost(i-1, j) < cost(i, j-1) && cost(i-1, j) < cost(i-1, j-1)){
                length(i, j) = length(i-1, j) + 1;
            } else if (cost(i-1, j-1) <= cost(i, j-1) && cost(i-1, j-1) <= cost(i-1, j)) {
                length(i, j) = length(i-1, j-1) + LEN_PENALTY_DIAG;
            } else if (cost(i, j-1) <= cost(i-1, j) && cost(i, j-1) <= cost(i-1, j-1)) {
                length(i, j) = length(i, j-1) + 1;
            } else {
                std::cout << "WARNNING: we do not find the min value of DTW distance" << std::endl;
            }
            cost(i, j) = std::min(std::min(cost(i-1, j), cost(i, j-1)), cost(i-1, j-1)) + dist(i-1, j-1);
        }
    }
    return cost(height, width) / length(height, width);
}

float DTWWithPath(const infra::matrix &dist, infra::matrix &path) {
    unsigned long height = dist.height();
    unsigned long width = dist.width();
    infra::matrix cost(height+1, width+1);
    infra::matrix length(height+1, width+1);
    path.resize(height+1, width+1);

    cost(0,0) = 0.0;
    length(0,0) = 1;
    path(0, 0) = -1;
    for (int i=1; i < height+1; i++) {
        cost(i, 0) = BIG_FLT;
        length(i, 0) = 1;
        path(i, 0) = -1;
    }
    for (int j=1; j < width+1; j++) {
        cost(0, j) = BIG_FLT;
        length(0, j) = 1;
        path(0, j) = -1;
    }
    for (int i=1; i < height+1; i++) {
        for (int j=1; j < width+1; j++) {
            if (cost(i-1, j) <= cost(i, j-1) && cost(i-1, j) <= cost(i-1, j-1)){
                length(i, j) = length(i-1, j) + 1;
                path(i, j) = 1;
            } else if (cost(i-1, j-1) <= cost(i, j-1) && cost(i-1, j-1) <= cost(i-1, j)) {
                length(i, j) = length(i-1, j-1) + LEN_PENALTY_DIAG;
                path(i, j) = 2;
            } else if (cost(i, j-1) <= cost(i-1, j) && cost(i, j-1) <= cost(i-1, j-1)) {
                length(i, j) = length(i, j-1) + 1;
                path(i, j) = 3;
            } else {
                std::cout << "WARNNING: we do not find the min value of DTW distance" << std::endl;
            }
            cost(i, j) = std::min(std::min(cost(i-1, j), cost(i, j-1)), cost(i-1, j-1)) + dist(i-1, j-1);
        }
    }
    return cost(height, width)/length(height, width);
}

float SLN_DTW(const infra::matrix &dist, infra::vector& area) {
    unsigned long height = dist.height();
    unsigned long width = dist.width();
    infra::matrix avg_cost(height, width);
    infra::matrix cost(height, width);
    infra::matrix trace(height, width);
    infra::matrix length(height, width);

    // initialize
    // trace(i,j) = 0 denote the precedent point of (i,j) is (i-1,j)
    // trace(i,j) = 1                                        (i,j-1)
    // trace(i,j) = 2                                        (i-1,j-1)
    for( int i = 0; i < width; i++) {
        avg_cost(0, i) = dist(0, i);
        cost(0, i) = dist(0, i);
        trace(0, i) = i;
        length(0, i) = 1;
    }

    for( int i = 1; i < height; i++) {
        trace(i, 0) = 0;
        length(i, 0) = i + 1;
        cost(i, 0) = dist(i, 0) + cost(i-1, 0);
        avg_cost(i, 0)= cost(i, 0) / length(i, 0);
    }

    // fill the three matrices in a dynamic programming style.
    for (int i = 1; i < height; i++) {
        for (int j = 1; j < width; j++) {
            // compute the three possible costs
            double cost_0 = dist(i, j) + cost(i-1, j);
            double cost_1 = dist(i, j) + cost(i, j-1);
            double cost_2 = dist(i, j) + cost(i-1, j-1);
            double avg_cost_0 = cost_0 / (1 + length(i-1, j));
            double avg_cost_1 = cost_1 / (1 + length(i, j-1));
            double avg_cost_2 = cost_2 / (LEN_PENALTY_DIAG + length(i-1, j-1));

            // choose the one which lead to the minimum cost as the precedent point
            if(avg_cost_0 < avg_cost_1) {
                if(avg_cost_0 < avg_cost_2) {
                    avg_cost(i, j) = avg_cost_0;
                    cost(i, j) = cost_0;
                    length(i, j) = 1 + length(i-1, j);
                    trace(i, j) = trace(i-1, j);
                }
                else {
                    avg_cost(i, j) = avg_cost_2;
                    cost(i, j) = cost_2;
                    length(i, j) = LEN_PENALTY_DIAG + length(i-1, j-1);
                    trace(i, j) = trace(i-1, j-1);
                }
            } else if(avg_cost_1 < avg_cost_2) {
                avg_cost(i, j) = avg_cost_1;
                cost(i, j) = cost_1;
                length(i, j) = 1 + length(i, j-1);
                trace(i, j) = trace(i, j-1);
            } else {
                avg_cost(i, j) = avg_cost_2;
                cost(i, j) = cost_2;
                length(i, j) = LEN_PENALTY_DIAG + length(i-1, j-1);
                trace(i, j) = trace(i-1, j-1);
            }

        }
    }
    int end_point = avg_cost.row(height-1).argmin();
    float min_cost = avg_cost(height-1, end_point);
    int start_point = trace(height-1, end_point);
    area(0) = start_point;
    area(1) = end_point;
    return min_cost;
}

void Average(const infra::matrix &mat_a, const infra::matrix &mat_b, int i, int j, int num, infra::matrix &avg_mat) {
    unsigned long dim = mat_a.width(); 
    infra::vector vec_a(dim);
    vec_a.zeros();
    vec_a = mat_a.row(i-1);
    if (num == 1) {
        vec_a += mat_b.row(j-1);
        vec_a *= 0.5;
    } else {
        for (int index =0; index < num; index++) {
            vec_a += mat_b.row(j-index-1);
        }
        vec_a /= (num+1);
    }
    for (int index = 0; index < dim; index++) {
        avg_mat(i-1, index) = vec_a(index);
    }
}

int AverageTemplate(const infra::matrix &mat_a, const infra::matrix &mat_b, std::string distance_type, infra::matrix &avg_mat) {
    unsigned long height = mat_a.height();
    unsigned long width = mat_b.height();
    infra::matrix path(height + 1, width + 1);
    infra::matrix dist(height, width);  
    
    ComputeDist(mat_a, mat_b, dist, distance_type);
    DTWWithPath(dist, path);
    avg_mat.resize(height, mat_a.width());
    int i = mat_a.height();
    int j = mat_b.height();

    while(i > 0) {
        if (path(i,j) < 0.5) {
            std::cout << "ERROR: no such path " << std::endl;
        } else if (path(i, j) < 1.5 && path(i, j) > 0.5) {
            Average(mat_a, mat_b, i, j, 1, avg_mat);
            i--;
        } else if (path(i, j) < 2.5 && path(i, j) > 1.5) {
            Average(mat_a, mat_b, i, j, 1, avg_mat);
            i--;
            j--;
        } else if (path(i, j) < 3.5 && path(i, j) > 2.5) {
            int k = j;
            while (path(i, j) < 3.5 && path(i, j) > 2.5) {
                j--;
            }
            Average(mat_a, mat_b, i, k, k-j, avg_mat);
            i--;
            j--;
        } else {
            std::cout << "ERROR: no such path " << std::endl;
        }
    }
    return height;
}

} //namespace aslp_std
