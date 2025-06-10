#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1Bo's Plan - Utilities Module
로깅, 에러 처리, 공통 유틸리티 함수들

Author: AI Assistant & User
Version: 1.0.0
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import traceback
import logging
from datetime import datetime
from pathlib import Path
import json
import sys
import os

# 설정 import
sys.path.append(str(Path(__file__).parent.parent))
from config import LOG_CONFIG, ERROR_CONFIG, LOG_DIR, APP_NAME, APP_VERSION

class Logger:
    """로깅 클래스"""
    
    def __init__(self, name=None):
        self.name = name or APP_NAME
        self.messages = []
        self.setup_logging()
    
    def setup_logging(self):
        """로깅 설정"""
        try:
            # 로그 파일명
            log_file = LOG_DIR / f"{self.name}_{datetime.now().strftime('%Y%m%d')}.log"
            
            # 로거 설정
            self.logger = logging.getLogger(self.name)
            self.logger.setLevel(getattr(logging, LOG_CONFIG['level']))
            
            # 핸들러가 이미 있으면 제거
            for handler in self.logger.handlers[:]:
                self.logger.removeHandler(handler)
            
            # 파일 핸들러
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_formatter = logging.Formatter(
                LOG_CONFIG['format'], 
                datefmt=LOG_CONFIG['date_format']
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
            
            # 콘솔 핸들러
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(file_formatter)
            self.logger.addHandler(console_handler)
            
        except Exception as e:
            print(f"Logging setup failed: {e}")
    
    def info(self, message):
        """정보 로그"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_message = f"[{timestamp}] INFO: {message}"
        self.messages.append(log_message)
        
        if hasattr(self, 'logger'):
            self.logger.info(message)
        else:
            print(log_message)
    
    def error(self, message):
        """에러 로그"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_message = f"[{timestamp}] ERROR: {message}"
        self.messages.append(log_message)
        
        if hasattr(self, 'logger'):
            self.logger.error(message)
        else:
            print(log_message)
    
    def warning(self, message):
        """경고 로그"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_message = f"[{timestamp}] WARNING: {message}"
        self.messages.append(log_message)
        
        if hasattr(self, 'logger'):
            self.logger.warning(message)
        else:
            print(log_message)
    
    def debug(self, message):
        """디버그 로그"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_message = f"[{timestamp}] DEBUG: {message}"
        self.messages.append(log_message)
        
        if hasattr(self, 'logger'):
            self.logger.debug(message)
        else:
            print(log_message)
    
    def get_messages(self):
        """로그 메시지 목록 반환"""
        return self.messages.copy()
    
    def clear_messages(self):
        """로그 메시지 목록 클리어"""
        self.messages.clear()

class ErrorHandler:
    """에러 처리 클래스"""
    
    def __init__(self, parent_window=None):
        self.parent_window = parent_window
        self.logger = Logger("ErrorHandler")
    
    def handle_exception(self, exception, show_dialog=True, context=""):
        """예외 처리"""
        error_info = {
            'type': type(exception).__name__,
            'message': str(exception),
            'context': context,
            'traceback': traceback.format_exc(),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'version': APP_VERSION
        }
        
        # 로깅
        if ERROR_CONFIG['enable_error_logging']:
            self.logger.error(f"{error_info['type']}: {error_info['message']}")
            self.logger.debug(f"Context: {context}")
            self.logger.debug(f"Traceback:\n{error_info['traceback']}")
        
        # 다이얼로그 표시
        if show_dialog and ERROR_CONFIG['show_detailed_errors']:
            self.show_error_dialog(error_info)
        elif show_dialog:
            messagebox.showerror("Error", f"An error occurred: {error_info['message']}")
        
        return error_info
    
    def show_error_dialog(self, error_info):
        """복사 가능한 에러 다이얼로그 표시"""
        try:
            if not self.parent_window:
                return
            
            error_window = tk.Toplevel(self.parent_window)
            error_window.title("🚨 Error Details")
            error_window.geometry("900x700")
            error_window.transient(self.parent_window)
            error_window.grab_set()
            
            # 에러 텍스트 생성
            error_text = f"""🚨 {APP_NAME} v{APP_VERSION} Error Report

Time: {error_info['timestamp']}
Type: {error_info['type']}
Context: {error_info['context']}

Message:
{error_info['message']}

Traceback:
{error_info['traceback']}

Version: {APP_VERSION}
System: {sys.platform}
Python: {sys.version}
"""
            
            # UI 구성
            main_frame = ttk.Frame(error_window, padding="15")
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            ttk.Label(main_frame, text="❌ An error occurred! Please copy this information:", 
                     font=('Segoe UI', 14, 'bold'), foreground='red').pack(anchor=tk.W, pady=(0, 15))
            
            # 텍스트 영역
            text_widget = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, 
                                                  font=('Consolas', 10))
            text_widget.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
            text_widget.insert('1.0', error_text)
            text_widget.config(state=tk.DISABLED)
            
            # 버튼 프레임
            button_frame = ttk.Frame(main_frame)
            button_frame.pack(fill=tk.X)
            
            def copy_to_clipboard():
                try:
                    self.parent_window.clipboard_clear()
                    self.parent_window.clipboard_append(error_text)
                    messagebox.showinfo("✅", "Error details copied to clipboard!")
                except Exception as e:
                    messagebox.showerror("❌", f"Copy failed: {e}")
            
            ttk.Button(button_frame, text="📋 Copy to Clipboard", 
                      command=copy_to_clipboard).pack(side=tk.LEFT, padx=(0, 15))
            ttk.Button(button_frame, text="❌ Close", 
                      command=error_window.destroy).pack(side=tk.RIGHT)
            
        except Exception as e:
            messagebox.showerror("Critical Error", 
                               f"Error dialog failed: {e}\n\nOriginal error: {error_info['message']}")
    
    def safe_execute(self, func, *args, **kwargs):
        """안전한 함수 실행"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            context = f"Function: {func.__name__ if hasattr(func, '__name__') else str(func)}"
            self.handle_exception(e, True, context)
            return None

class FileManager:
    """파일 관리 유틸리티"""
    
    def __init__(self):
        self.logger = Logger("FileManager")
    
    def ensure_dir(self, path):
        """디렉토리 존재 확인 및 생성"""
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            self.logger.error(f"Directory creation failed: {path} - {e}")
            return False
    
    def get_file_size(self, filepath):
        """파일 크기 반환 (KB)"""
        try:
            return Path(filepath).stat().st_size // 1024
        except:
            return 0
    
    def get_file_modified_time(self, filepath):
        """파일 수정 시간 반환"""
        try:
            timestamp = Path(filepath).stat().st_mtime
            return datetime.fromtimestamp(timestamp)
        except:
            return None
    
    def move_to_out_folder(self, filepath, out_dir):
        """파일을 out 폴더로 이동"""
        try:
            source = Path(filepath)
            if not source.exists():
                return False
            
            self.ensure_dir(out_dir)
            destination = Path(out_dir) / source.name
            
            # 중복 파일명 처리
            counter = 1
            while destination.exists():
                stem = source.stem
                suffix = source.suffix
                destination = Path(out_dir) / f"{stem}_{counter}{suffix}"
                counter += 1
            
            source.rename(destination)
            self.logger.info(f"File moved: {source.name} -> out/{destination.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"File move failed: {e}")
            return False
    
    def cleanup_old_files(self, directory, max_age_days=30):
        """오래된 파일 정리"""
        try:
            from datetime import timedelta
            
            directory = Path(directory)
            if not directory.exists():
                return []
            
            cutoff_date = datetime.now() - timedelta(days=max_age_days)
            old_files = []
            
            for file in directory.glob("*.csv"):
                modified_time = self.get_file_modified_time(file)
                if modified_time and modified_time < cutoff_date:
                    old_files.append(file)
            
            return old_files
            
        except Exception as e:
            self.logger.error(f"Cleanup scan failed: {e}")
            return []

class DataValidator:
    """데이터 검증 유틸리티"""
    
    @staticmethod
    def is_valid_stock_symbol(symbol):
        """유효한 주식 심볼인지 확인"""
        if not symbol or len(symbol.strip()) == 0:
            return False
        
        symbol = symbol.strip().upper()
        
        # 한국 주식 (숫자로만 구성, 1-6자리)
        if symbol.isdigit() and 1 <= len(symbol) <= 6:
            return True
        
        # 미국 주식 (알파벳 1-5자리)
        if symbol.isalpha() and 1 <= len(symbol) <= 5:
            return True
        
        return False
    
    @staticmethod
    def is_korean_stock(symbol):
        """한국 주식인지 확인"""
        if not symbol:
            return False
        
        # 6자리로 맞춘 후 확인
        if symbol.isdigit():
            formatted_symbol = symbol.zfill(6)
            return len(formatted_symbol) == 6 and formatted_symbol.isdigit()
        
        return False
    
    @staticmethod
    def format_korean_stock_code(symbol):
        """한국 주식 코드를 6자리로 포맷"""
        if symbol and symbol.isdigit():
            return symbol.zfill(6)
        return symbol
    
    @staticmethod
    def validate_price(price_str):
        """가격 검증"""
        try:
            price = float(price_str)
            return price > 0
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_positive_integer(value_str):
        """양의 정수 검증"""
        try:
            value = int(value_str)
            return value > 0
        except (ValueError, TypeError):
            return False

class ConfigManager:
    """설정 관리 유틸리티"""
    
    def __init__(self, config_file="settings.json"):
        self.config_file = Path(config_file)
        self.logger = Logger("ConfigManager")
        self.settings = self.load_settings()
    
    def load_settings(self):
        """설정 로드"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {}
        except Exception as e:
            self.logger.error(f"Settings load failed: {e}")
            return {}
    
    def save_settings(self):
        """설정 저장"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            self.logger.error(f"Settings save failed: {e}")
            return False
    
    def get(self, key, default=None):
        """설정값 가져오기"""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """설정값 설정"""
        self.settings[key] = value
        self.save_settings()
    
    def get_nested(self, keys, default=None):
        """중첩된 설정값 가져오기"""
        try:
            value = self.settings
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set_nested(self, keys, value):
        """중첩된 설정값 설정"""
        try:
            target = self.settings
            for key in keys[:-1]:
                if key not in target:
                    target[key] = {}
                target = target[key]
            target[keys[-1]] = value
            self.save_settings()
            return True
        except Exception as e:
            self.logger.error(f"Nested setting failed: {e}")
            return False

# 공통 유틸리티 함수들
def format_number(value, decimal_places=2):
    """숫자 포맷팅"""
    try:
        if isinstance(value, (int, float)):
            return f"{value:,.{decimal_places}f}"
        return str(value)
    except:
        return str(value)

def format_percentage(value, decimal_places=2):
    """퍼센트 포맷팅"""
    try:
        return f"{value:.{decimal_places}f}%"
    except:
        return str(value)

def format_currency(value, symbol="$", decimal_places=2, is_korean=False):
    """통화 포맷팅 - 한국/미국 구분"""
    try:
        if is_korean:
            # 한국 주식: 원화, 소수점 없음
            return f"₩{value:,.0f}"
        else:
            # 미국 주식: 달러, 소수점 있음
            return f"${value:,.{decimal_places}f}"
    except:
        return str(value)

def format_currency_auto(value, symbol, decimal_places=2):
    """자동 통화 포맷팅 - 심볼로 한국/미국 구분"""
    try:
        # 심볼이 숫자로만 구성되어 있고 6자리면 한국 주식
        if symbol and symbol.isdigit() and len(symbol.zfill(6)) == 6:
            return format_currency(value, is_korean=True)
        else:
            return format_currency(value, is_korean=False, decimal_places=decimal_places)
    except:
        return str(value)

def truncate_text(text, max_length=50):
    """텍스트 자르기"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def get_color_by_change(change_value):
    """변동에 따른 색상 반환"""
    if change_value > 0:
        return "green"
    elif change_value < 0:
        return "red"
    else:
        return "black"

def safe_divide(numerator, denominator, default=0):
    """안전한 나눗셈"""
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except:
        return default

def calculate_percentage_change(old_value, new_value):
    """퍼센트 변화율 계산"""
    try:
        if old_value == 0:
            return 0
        return ((new_value - old_value) / old_value) * 100
    except:
        return 0