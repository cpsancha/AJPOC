#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module groups the tests for the ´´logger_setup´´ module
"""

import ajpoc.logger_setup


def test_logger_level_mapper():
    """
    This function tests the ´´logger_level_mapper´´ function
    :return:
    """
    assert ajpoc.logger_setup.logger_level_mapper("NOTSET") == 0
    assert ajpoc.logger_setup.logger_level_mapper("DEBUG") == 10
    assert ajpoc.logger_setup.logger_level_mapper("INFO") == 20
    assert ajpoc.logger_setup.logger_level_mapper("WARNING") == 30
    assert ajpoc.logger_setup.logger_level_mapper("ERROR") == 40
    assert ajpoc.logger_setup.logger_level_mapper("CRITICAL") == 50
    assert ajpoc.logger_setup.logger_level_mapper("OTHERS") == 0
