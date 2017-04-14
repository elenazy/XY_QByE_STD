// dtw.h

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

#include <math.h>
#include <string>

#include "infra.h"

#ifndef ASLP_KWS_DTW_H_
#define ASLP_KWS_DTW_H_

namespace aslp_std {

#define LEN_PENALTY_DIAG 2
#define BIG_FLT 99999999

float DTW(const infra::matrix &dist);

float DTWWithPath(const infra::matrix &dist, infra::matrix &path);

float SLN_DTW(const infra::matrix &dist, infra::vector& area); 

void Average(const infra::matrix &mat_a, const infra::matrix &mat_b, int i, int j, int num, infra::matrix &avg_mat);

int AverageTemplate(const infra::matrix &mat_a, const infra::matrix &mat_b, const std::string distance_type, infra::matrix &avg_mat);

} //namespace aslp_std

#endif // ASLP_KWS_DTW_H_