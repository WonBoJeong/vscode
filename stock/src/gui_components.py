#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI 컴포넌트 모듈
재사용 가능한 GUI 컴포넌트들
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class ModernComponents:
    def __init__(self):
        """현대적 GUI 컴포넌트 초기화"""
        self.colors = {
            'primary': '#667eea',
            'secondary': '#764ba2',
            'success': '#4facfe',
            'warning': '#fa709a',
            'background': '#f8fafc',
            'surface': '#ffffff',
            'text_primary': '#2d3748',
            'text_secondary': '#718096'
        }
        
    def create_card_frame(self, parent, title=None, padding=20):
        """카드 스타일 프레임 생성"""
        card_frame = ttk.Frame(parent, style='Card.TFrame')
        
        if title:
            title_frame = ttk.Frame(card_frame)
            title_frame.pack(fill=tk.X, padx=padding, pady=(padding, 10))
            
            title_label = ttk.Label(title_frame, text=title, style='Title.TLabel')
            title_label.pack(side=tk.LEFT)
            
            # 구분선
            separator = ttk.Separator(card_frame, orient='horizontal')
            separator.pack(fill=tk.X, padx=padding, pady=(0, 10))
            
        return card_frame
        
    def create_metric_card(self, parent, title, value, color='primary'):
        """메트릭 카드 생성"""
        card = ttk.Frame(parent, style='Card.TFrame')
        card.pack(fill=tk.X, padx=5, pady=5)
        
        # 제목
        title_label = ttk.Label(card, text=title, style='Subtitle.TLabel')
        title_label.pack(pady=(10, 0))
        
        # 값
        value_label = ttk.Label(card, text=str(value), 
                               font=('Segoe UI', 18, 'bold'))
        value_label.pack(pady=(5, 10))
        
        return card
        
    def create_progress_indicator(self, parent, value, max_value=100):
        """진행률 표시기 생성"""
        frame = ttk.Frame(parent)
        
        # 진행률 바
        progress = ttk.Progressbar(frame, length=200, mode='determinate')
        progress['value'] = (value / max_value) * 100
        progress.pack(pady=5)
        
        # 텍스트
        text_label = ttk.Label(frame, text=f"{value}/{max_value}")
        text_label.pack()
        
        return frame
        
    def create_status_indicator(self, parent, status, text=""):
        """상태 표시기 생성"""
        frame = ttk.Frame(parent)
        
        # 상태에 따른 색상
        status_colors = {
            'success': '🟢',
            'warning': '🟡', 
            'error': '🔴',
            'info': '🔵'
        }
        
        indicator = status_colors.get(status, '⚪')
        
        # 아이콘
        icon_label = ttk.Label(frame, text=indicator, font=('Segoe UI', 16))
        icon_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # 텍스트
        if text:
            text_label = ttk.Label(frame, text=text)
            text_label.pack(side=tk.LEFT)
            
        return frame
        
    def create_data_table(self, parent, columns, data=None):
        """데이터 테이블 생성"""
        frame = ttk.Frame(parent)
        
        # 트리뷰 생성
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=10)
        
        # 컬럼 헤더 설정
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor='center')
            
        # 스크롤바
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # 패킹
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 데이터 삽입
        if data:
            for row in data:
                tree.insert('', tk.END, values=row)
                
        return frame, tree
        
    def create_mini_chart(self, parent, data, chart_type='line'):
        """미니 차트 생성"""
        fig = Figure(figsize=(4, 2), facecolor=self.colors['background'])
        ax = fig.add_subplot(111)
        
        if chart_type == 'line':
            ax.plot(data, color=self.colors['primary'], linewidth=2)
        elif chart_type == 'bar':
            ax.bar(range(len(data)), data, color=self.colors['primary'])
            
        # 스타일링
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        
        # Canvas 생성
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        
        return canvas.get_tk_widget()
        
    def create_search_box(self, parent, placeholder="검색...", callback=None):
        """검색 박스 생성"""
        frame = ttk.Frame(parent)
        
        # 검색 아이콘
        icon_label = ttk.Label(frame, text="🔍", font=('Segoe UI', 12))
        icon_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # 입력 필드
        entry = ttk.Entry(frame, font=('Segoe UI', 11))
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # 플레이스홀더 효과
        entry.insert(0, placeholder)
        entry.config(foreground='gray')
        
        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(foreground='black')
                
        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.config(foreground='gray')
                
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)
        
        if callback:
            entry.bind('<Return>', callback)
            
        return frame, entry
        
    def create_button_group(self, parent, buttons, selected=0):
        """버튼 그룹 생성"""
        frame = ttk.Frame(parent)
        
        button_vars = []
        button_widgets = []
        
        for i, (text, command) in enumerate(buttons):
            var = tk.StringVar()
            button = ttk.Radiobutton(frame, text=text, variable=var, 
                                   value=text, command=command)
            button.pack(side=tk.LEFT, padx=2)
            
            if i == selected:
                button.invoke()
                
            button_vars.append(var)
            button_widgets.append(button)
            
        return frame, button_widgets
        
    def create_notification(self, parent, message, type='info', duration=3000):
        """알림 창 생성"""
        notification = tk.Toplevel(parent)
        notification.title("")
        notification.geometry("300x80")
        notification.resizable(False, False)
        
        # 화면 우상단에 배치
        notification.geometry("+{}+{}".format(
            parent.winfo_screenwidth() - 320,
            20
        ))
        
        # 프레임
        main_frame = ttk.Frame(notification, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 아이콘
        icons = {
            'info': 'ℹ️',
            'success': '✅',
            'warning': '⚠️',
            'error': '❌'
        }
        
        icon_label = ttk.Label(main_frame, text=icons.get(type, 'ℹ️'), 
                              font=('Segoe UI', 16))
        icon_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # 메시지
        message_label = ttk.Label(main_frame, text=message, wraplength=200)
        message_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 자동 닫기
        if duration > 0:
            notification.after(duration, notification.destroy)
            
        return notification
        
    def create_loading_spinner(self, parent, text="로딩 중..."):
        """로딩 스피너 생성"""
        frame = ttk.Frame(parent)
        
        # 스피너
        spinner = ttk.Progressbar(frame, mode='indeterminate', length=200)
        spinner.pack(pady=10)
        spinner.start(10)
        
        # 텍스트
        text_label = ttk.Label(frame, text=text)
        text_label.pack()
        
        return frame, spinner
        
    def create_collapsible_frame(self, parent, title, content_frame):
        """접을 수 있는 프레임 생성"""
        main_frame = ttk.Frame(parent)
        
        # 헤더
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X)
        
        # 토글 버튼
        is_expanded = tk.BooleanVar(value=True)
        
        def toggle():
            if is_expanded.get():
                content_frame.pack_forget()
                toggle_btn.config(text="▶")
                is_expanded.set(False)
            else:
                content_frame.pack(fill=tk.BOTH, expand=True)
                toggle_btn.config(text="▼")
                is_expanded.set(True)
                
        toggle_btn = ttk.Button(header_frame, text="▼", width=3, command=toggle)
        toggle_btn.pack(side=tk.LEFT)
        
        # 제목
        title_label = ttk.Label(header_frame, text=title, style='Title.TLabel')
        title_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # 콘텐츠 (기본적으로 표시)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        return main_frame
        
    def create_tabs_with_icons(self, parent, tabs):
        """아이콘이 있는 탭 생성"""
        notebook = ttk.Notebook(parent)
        
        for icon, text, frame in tabs:
            tab_text = f"{icon} {text}"
            notebook.add(frame, text=tab_text)
            
        return notebook
        
    def create_split_panel(self, parent, left_content, right_content, ratio=0.7):
        """분할 패널 생성"""
        paned_window = ttk.PanedWindow(parent, orient=tk.HORIZONTAL)
        
        # 왼쪽 패널
        left_frame = ttk.Frame(paned_window)
        paned_window.add(left_frame, weight=int(ratio * 100))
        left_content(left_frame)
        
        # 오른쪽 패널
        right_frame = ttk.Frame(paned_window)
        paned_window.add(right_frame, weight=int((1-ratio) * 100))
        right_content(right_frame)
        
        return paned_window
        
    def create_modern_listbox(self, parent, items=None, selection_callback=None):
        """현대적 스타일 리스트박스"""
        frame = ttk.Frame(parent)
        
        # 리스트박스와 스크롤바
        listbox = tk.Listbox(frame, font=('Segoe UI', 10), 
                           selectmode=tk.SINGLE, height=10)
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=listbox.yview)
        listbox.configure(yscrollcommand=scrollbar.set)
        
        # 패킹
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 아이템 추가
        if items:
            for item in items:
                listbox.insert(tk.END, item)
                
        # 선택 콜백
        if selection_callback:
            listbox.bind('<<ListboxSelect>>', selection_callback)
            
        return frame, listbox