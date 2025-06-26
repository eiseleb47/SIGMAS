#!/bin/python3
# -*- coding: utf-8 -*-

from sigmas.simulations.donut_sim import create_one_donut

ring1 = create_one_donut({"semi-maj": 560,
                          "semi-min": 400,
                          "ecc": 0.3,
                          "inc": 40,
                          "ring_ratio" : 0.96,
                          "width": 400,
                          "height": 400})