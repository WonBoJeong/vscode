#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1Bo's Plan - Modules Package
모듈 패키지 초기화

Author: AI Assistant & User
Version: 1.0.0
"""

from .utils import Logger, ErrorHandler
from .data_manager import DataManager
from .korean_stock_manager import KoreanStockManager
from .chart_manager import ChartManager
from .analysis_engine import AnalysisEngine
from .investment_calculator import InvestmentCalculator
from .crash_analyzer import CrashAnalyzer

__all__ = [
    'Logger',
    'ErrorHandler', 
    'DataManager',
    'KoreanStockManager',
    'ChartManager',
    'AnalysisEngine',
    'InvestmentCalculator',
    'CrashAnalyzer'
]

__version__ = "1.0.0"
__author__ = "AI Assistant & User"