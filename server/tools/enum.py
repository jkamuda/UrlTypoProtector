#!/usr/bin/env python

def enum(**named_values):
  return type('Enum', (), named_values)
