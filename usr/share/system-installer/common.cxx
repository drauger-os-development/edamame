/*
 * common.cxx
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
#include "common.hpp"

using namespace std;

// real_number()
// Take an int or float and return an int that is 0 or higher
//
// This DOES NOT return absolute value. Any negative numbers will return 0.
// Valid floats that are passed are truncated, not rounded.

unsigned real_number(int num)
{
	// This one is really easy. Just check to see if the argument is positive
	if (num > 0)
	{
		// now just static_cast the var so we know it's unsigned for sure
		return static_cast<unsigned>(num);
	}
	return 0;
}

unsigned real_number(float num)
{
	// First we need to static_cast the float to an int, to truncate it
	int new_num = static_cast<int>(num);
	// now, just use the other real_number()
	// no need to write code twice!
	return real_number(new_num);
}
