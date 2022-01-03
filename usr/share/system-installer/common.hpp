/*
 * common.hpp
 *
 * Copyright 2022 Thomas Castleman <contact@draugeros.org>
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 * MA 02110-1301, USA.
 *
 *
 */
#define PY_SSIZE_T_CLEAN
#ifndef common_hpp__
#define common_hpp__
#define elif else if
#define string_list std::vector<std::string>
#define int_list std::vector<int>
#define float_list std::vector<float>
#define bool_list std::vector<bool>

#include <Python.h>

// We need to overload this method so it can take either a float or an int
extern unsigned real_number(float num);

extern unsigned real_number(int num);


#endif //common_hpp__
