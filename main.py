import sys
import os
import configparser
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QListWidget, QTableWidget, QTableWidgetItem, QLabel, QSplitter, 
                            QFileDialog, QPushButton, QGroupBox, QCheckBox, QMessageBox, 
                            QInputDialog, QMenu, QSizePolicy, QToolBar)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class WiiPluginManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wii插件配置管理器 By：bilibili:86年复古游戏厅")
        self.setGeometry(100, 100, 1200, 900)  # 增加窗口高度
        
        # 初始化日志
        import logging
        self.logging_enabled = False  # 默认禁用日志
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='wii_plugin_tool.log',
            filemode='w'
        )
        self.logger = logging.getLogger(__name__)
        self.setup_logging()  # 初始化日志配置
        
        # 初始化变量
        self.plugins_dir = ""
        self.roms_dir = ""
        self.images_dir = ""
        self.plugins = []
        self.current_plugin = None
        self.custom_titles = {}
        self.language = 'zh'  # 默认中文
        
        # 翻译字典
        self.translations = {
            'zh': {
                'window_title': "Wii插件配置管理器 By：bilibili:86年复古游戏厅",
                'pin_button': "📌 置顶",
                'pin_tooltip': "点击切换窗口置顶状态",
                'plugins_button': "� 插件目录",
                'plugins_tooltip': "选择插件配置文件所在目录",
                'images_button': "🖼️ 图片目录",
                'images_tooltip': "选择游戏图片所在目录",
                'titles_button': "📝 标题文件",
                'titles_tooltip': "选择自定义标题配置文件",
                'roms_button': "🎮 ROM目录",
                'roms_tooltip': "选择ROM文件所在目录",
                'scan_button': "🔄 扫描插件",
                'scan_tooltip': "扫描并加载插件配置文件",
                'subdir_check': "框体",
                'subdir_tooltip': "是否扫描子目录中的插件文件",
                'open_titles_button': "📋 打开自定义标题",
                'open_titles_tooltip': "打开自定义标题文件进行编辑",
                'log_button': "📝 日志",
                'log_tooltip_enabled': "点击切换日志记录功能 (当前: 启用)",
                'log_tooltip_disabled': "点击切换日志记录功能 (当前: 禁用)",
                'rom_list': "ROM列表",
                'image_management': "图片管理",
                'file_name': "文件名",
                'display_name': "显示名称",
                'resolution': "分辨率",
                'not_selected': "未选择",
                'image_list': "图片列表",
                'plugins_dir_label': "插件目录",
                'roms_dir_label': "ROM目录",
                'images_dir_label': "图片目录",
                'titles_file_label': "自定义标题文件"
            },
            'en': {
                'window_title': "Wii Plugin Manager By：bilibili:86年复古游戏厅",
                'pin_button': "📌 Pin",
                'pin_tooltip': "Toggle window always on top",
                'plugins_button': "� Plugins Dir",
                'plugins_tooltip': "Select plugin configuration directory",
                'images_button': "�️ Images Dir",
                'images_tooltip': "Select game images directory",
                'titles_button': "📝 Title Files",
                'titles_tooltip': "Select custom title configuration file",
                'roms_button': "🎮 ROMs Dir",
                'roms_tooltip': "Select ROM files directory",
                'scan_button': "🔄 Scan Plugins",
                'scan_tooltip': "Scan and load plugin configurations",
                'subdir_check': "Subdirs",
                'subdir_tooltip': "Whether to scan subdirectories for plugins",
                'open_titles_button': "� Open Titles",
                'open_titles_tooltip': "Open custom title file for editing",
                'log_button': "📝 Log",
                'log_tooltip_enabled': "Toggle logging (Current: Enabled)",
                'log_tooltip_disabled': "Toggle logging (Current: Disabled)",
                'switch_language': "Switch Language",
                'rom_list': "ROM List",
                'image_management': "Image Management",
                'select_plugin_dir': "Select Plugin Directory",
                'select_rom_dir': "Select ROM Directory",
                'select_image_dir': "Select Image Directory",
                'select_title_file': "Select Title File",
                'scan_plugins': "Scan Plugins",
                'scan_subdirs': "Scan Subdirectories",
                'open_title_editor': "Open Title Editor",
                'toggle_logging': "Toggle Logging",
                'toggle_pin': "Toggle Window Pin",
                'no_image_selected': "No image selected",
                'resize_image': "Resize Image",
                'enter_width': "Enter new width (px):",
                'enter_height': "Enter new height (px):",
                'success': "Success",
                'error': "Error",
                'warning': "Warning",
                'image_resized': "Image resized to {}×{} px",
                'permission_error': "Permission error",
                'file_locked': "File may be locked by another program",
                'file_not_found': "File not found"
            }
        }
     
        # 路径显示标签
        self.plugins_label = QLabel(f"{self.tr('plugins_dir_label')}: {self.tr('not_selected')}")
        self.roms_label = QLabel(f"{self.tr('roms_dir_label')}: {self.tr('not_selected')}")
        self.images_label = QLabel(f"{self.tr('images_dir_label')}: {self.tr('not_selected')}")
        self.custom_titles_label = QLabel(f"{self.tr('titles_file_label')}: {self.tr('not_selected')}")
        
        self.init_ui()
        
    def tr(self, key, *args):
        """获取翻译文本"""
        text = self.translations[self.language].get(key, key)
        if args:
            return text.format(*args)
        return text

# 添加语言切换方法
    def toggle_language(self):
        """切换语言"""
        self.language = 'en' if self.language == 'zh' else 'zh'
        self.update_ui_language()
        
    def update_ui_language(self):
        """更新UI语言"""
        self.setWindowTitle(self.tr('window_title'))
        self.topmost_btn.setText(self.tr('pin_button'))
        self.plugins_btn.setText(self.tr('plugins_button'))
        self.images_btn.setText(self.tr('images_button'))
        self.custom_titles_btn.setText(self.tr('titles_button'))
        self.roms_btn.setText(self.tr('roms_button'))
        self.scan_btn.setText(self.tr('scan_button'))
        self.subdir_check.setText(self.tr('subdir_check'))
        self.titles_btn.setText(self.tr('open_titles_button'))
        self.logging_btn.setText(self.tr('log_button'))
        
        # 更新路径标签
        if hasattr(self, 'plugins_dir') and self.plugins_dir:
            self.plugins_label.setText(f"{self.tr('plugins_button')}: {self.plugins_dir}")
        else:
            self.plugins_label.setText(f"{self.tr('plugins_button')}: {self.tr('not_selected')}")
            
        if hasattr(self, 'roms_dir') and self.roms_dir:
            self.roms_label.setText(f"{self.tr('roms_button')}: {self.roms_dir}")
        else:
            self.roms_label.setText(f"{self.tr('roms_button')}: {self.tr('not_selected')}")
            
        if hasattr(self, 'images_dir') and self.images_dir:
            self.images_label.setText(f"{self.tr('images_button')}: {self.images_dir}")
        else:
            self.images_label.setText(f"{self.tr('images_button')}: {self.tr('not_selected')}")
            
        if hasattr(self, 'custom_titles_file') and self.custom_titles_file:
            self.custom_titles_label.setText(f"{self.tr('titles_button')}: {self.custom_titles_file}")
        else:
            self.custom_titles_label.setText(f"{self.tr('titles_button')}: {self.tr('not_selected')}")
        
        # 更新表格标题
        self.rom_table.setHorizontalHeaderLabels([self.tr('file_name'), self.tr('display_name')])
        self.image_table.setHorizontalHeaderLabels([self.tr('file_name'), self.tr('resolution')])
        
        # 更新分组框标题
        self.rom_group.setTitle(self.tr('rom_list'))
        self.image_group.setTitle(self.tr('image_management'))
        
        # 更新计数标签前缀
        rom_count = self.rom_table.rowCount()
        image_count = self.image_table.rowCount()
        self.rom_count_label.setText(f"({rom_count})")
        self.image_count_label.setText(f"({image_count})")
        
        # 更新图片列表标签
        if hasattr(self, 'image_header'):
            for i in range(self.image_header.count()):
                widget = self.image_header.itemAt(i).widget()
                if isinstance(widget, QLabel) and widget.text() == "图片列表":
                    widget.setText(self.tr('image_list'))

    def init_ui(self):
        # 设置全局样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QListWidget, QTableWidget {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 2px;
            }
            QListWidget::item, QTableWidget::item {
                color: #333333;
                padding: 4px;
            }
            QListWidget::item:selected, QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            QListWidget::item:hover, QTableWidget::item:hover {
                background-color: #f5f5f5;
            }
            QLabel {
                color: #333333;
                font-size: 12px;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                margin-top: 12px;
                padding-top: 12px;
            }
            QGroupBox::title {
                color: #1976d2;
                subcontrol-origin: margin;
                left: 10px;
            }
            QCheckBox {
                color: #333333;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #757575;
                border-radius: 3px;
                background-color: #ffffff;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #4CAF50;
                border-radius: 3px;
                background-color: #4CAF50;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 12px;
                min-width: 80px;
                min-height: 25px;
            }
            QPushButton:hover {
                background-color: #66BB6A;
            }
            QPushButton:pressed {
                background-color: #43A047;
            }
            QPushButton:disabled {
                background-color: #BDBDBD;
            }
            QTableWidget::horizontalHeader {
                background-color: #f5f5f5;
                font-weight: bold;
            }
            QTableWidget::item {
                border-bottom: 1px solid #e0e0e0;
            }
        """)
        
        # 主布局
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        
        # 创建可移动的工具栏
        toolbar = QToolBar("主工具栏")
        toolbar.setMovable(True)  # 允许移动
        toolbar.setFloatable(True)  # 允许浮动
        toolbar.setAllowedAreas(Qt.AllToolBarAreas)  # 允许停靠在所有区域
        
        # 添加置顶按钮 (红色)
        self.always_on_top = False
        self.topmost_btn = QPushButton("📌 置顶")
        self.topmost_btn.setCheckable(True)
        self.topmost_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF5252;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton:checked {
                background-color: #D32F2F;
            }
            QPushButton:hover {
                background-color: #FF867C;
            }
            QPushButton:checked:hover {
                background-color: #D32F2F;
            }
        """)
        self.topmost_btn.setToolTip(self.tr('pin_tooltip'))
        self.topmost_btn.clicked.connect(self.toggle_topmost)
        toolbar.addWidget(self.topmost_btn)

        # 添加插件目录按钮 (橙色)
        self.plugins_btn = QPushButton("� 插件目录")
        self.plugins_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #FFB74D;
            }
            QPushButton:pressed {
                background-color: #F57C00;
            }
        """)
        self.plugins_btn.setToolTip(self.tr('plugins_tooltip'))
        self.plugins_btn.clicked.connect(self.select_plugins_dir)
        toolbar.addWidget(self.plugins_btn)
        
        # 添加图片目录按钮 (黄色)
        self.images_btn = QPushButton("🖼️ 图片目录")
        self.images_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFEB3B;
                color: #333333;
                border: none;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #FFF176;
            }
            QPushButton:pressed {
                background-color: #FDD835;
            }
        """)
        self.images_btn.setToolTip(self.tr('images_tooltip'))
        self.images_btn.clicked.connect(self.select_images_dir)
        toolbar.addWidget(self.images_btn)
        
        # 添加标题文件按钮 (绿色)
        self.custom_titles_btn = QPushButton("📝 标题文件")
        self.custom_titles_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #66BB6A;
            }
            QPushButton:pressed {
                background-color: #388E3C;
            }
        """)
        self.custom_titles_btn.setToolTip(self.tr('titles_tooltip'))
        self.custom_titles_btn.clicked.connect(self.select_custom_titles_file)
        toolbar.addWidget(self.custom_titles_btn)
        
        # 添加ROM目录按钮 (蓝色)
        self.roms_btn = QPushButton("🎮 ROM目录")
        self.roms_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #42A5F5;
            }
            QPushButton:pressed {
                background-color: #1976D2;
            }
        """)
        self.roms_btn.setToolTip(self.tr('roms_tooltip'))
        self.roms_btn.clicked.connect(self.select_roms_dir)
        toolbar.addWidget(self.roms_btn)
        
        # 添加分隔符
        toolbar.addSeparator()
        
        # 添加扫描插件按钮 (靛色)
        self.scan_btn = QPushButton("🔄 扫描插件")
        self.scan_btn.setStyleSheet("""
            QPushButton {
                background-color: #3F51B5;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #5C6BC0;
            }
            QPushButton:pressed {
                background-color: #303F9F;
            }
        """)
        self.scan_btn.setToolTip(self.tr('scan_tooltip'))
        self.scan_btn.clicked.connect(self.scan_plugins)
        toolbar.addWidget(self.scan_btn)
        
        # 添加扫描子目录复选框 (靛色框体)
        self.subdir_check = QCheckBox("扫描子目录")
        self.subdir_check.setChecked(True)
        self.subdir_check.setStyleSheet("""
            QCheckBox {
                color: #3F51B5;
                font-weight: bold;
                spacing: 8px;
                padding: 4px;
                border: 2px solid #5C6BC0;
                border-radius: 4px;
                background-color: #E8EAF6;
            }
            QCheckBox:hover {
                background-color: #C5CAE9;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                background-color: #E8EAF6;
                border: 2px solid #5C6BC0;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                background-color: #3F51B5;
                border: 2px solid #3F51B5;
            }
            QCheckBox::indicator:hover {
                border: 2px solid #3949AB;
            }
        """)
        self.subdir_check.setToolTip("是否扫描子目录中的插件文件")
        toolbar.addWidget(self.subdir_check)
        
        # 添加打开自定义标题按钮 (紫色)
        self.titles_btn = QPushButton("📋 打开自定义标题")
        self.titles_btn.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #BA68C8;
            }
            QPushButton:pressed {
                background-color: #7B1FA2;
            }
        """)
        self.titles_btn.setToolTip(self.tr('open_titles_tooltip'))
        self.titles_btn.clicked.connect(self.open_custom_titles_file)
        toolbar.addWidget(self.titles_btn)
        
        # 添加语言切换按钮
        self.lang_btn = QPushButton("🌐change language")
        self.lang_btn.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px;
                min-width: 30px;
            }
            QPushButton:hover {
                background-color: #BA68C8;
            }
            QPushButton:pressed {
                background-color: #7B1FA2;
            }
        """)
        self.lang_btn.setToolTip(self.tr('switch_language'))
        self.lang_btn.clicked.connect(self.toggle_language)
        toolbar.addWidget(self.lang_btn)

        # 添加日志按钮 (默认禁用)
        self.logging_btn = QPushButton(self.tr('log_button'))
        self.logging_btn.setCheckable(True)
        self.logging_btn.setChecked(False)
        self.logging_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton:checked {
                background-color: #F44336;
            }
            QPushButton:hover {
                background-color: #66BB6A;
            }
            QPushButton:checked:hover {
                background-color: #EF5350;
            }
        """)
        self.logging_btn.setToolTip("点击切换日志记录功能 (当前: 禁用)")
        self.logging_btn.clicked.connect(self.toggle_logging)
        toolbar.addWidget(self.logging_btn)
        
        # 将工具栏添加到主窗口
        self.addToolBar(toolbar)
        
        # 三栏分割
        splitter = QSplitter(Qt.Horizontal)
        
        # 左侧 - 插件列表
        self.plugin_list_widget = QListWidget()
        self.plugin_list_widget.itemClicked.connect(self.on_plugin_selected)
        self.plugin_list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.plugin_list_widget.customContextMenuRequested.connect(self.show_plugin_context_menu)
        splitter.addWidget(self.plugin_list_widget)
        
        # 中间 - ROM列表
        self.rom_group = QGroupBox(self.tr("rom_list"))
        rom_layout = QVBoxLayout()
        
        # ROM计数标签
        rom_header = QHBoxLayout()
        rom_header.addWidget(QLabel(self.tr("rom_list")))
        self.rom_count_label = QLabel("(0)")
        rom_header.addWidget(self.rom_count_label)
        rom_header.addStretch()
        rom_layout.addLayout(rom_header)
        
        self.rom_table = QTableWidget()
        self.rom_table.setColumnCount(2)
        self.rom_table.setHorizontalHeaderLabels(["文件名", "显示名称"])
        self.rom_table.setSortingEnabled(True)
        self.rom_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.rom_table.customContextMenuRequested.connect(self.show_rom_context_menu)
        rom_layout.addWidget(self.rom_table)
        self.rom_group.setLayout(rom_layout)
        splitter.addWidget(self.rom_group)
        
        # 右侧 - 图片管理
        self.image_group = QGroupBox(self.tr("image_management"))
        self.image_layout = QVBoxLayout()
        
        # 图片计数标签
        image_header = QHBoxLayout()
        image_header.addWidget(QLabel("图片列表"))
        self.image_count_label = QLabel("(0)")
        image_header.addWidget(self.image_count_label)
        image_header.addStretch()
        self.image_layout.addLayout(image_header)
        
        # 创建垂直分割器
        self.image_splitter = QSplitter(Qt.Vertical)
        
        # 图片列表
        self.image_table = QTableWidget()
        self.image_table.setColumnCount(2)
        self.image_table.setHorizontalHeaderLabels(["文件名", "分辨率"])
        self.image_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.image_table.setSortingEnabled(True)
        self.image_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.image_table.customContextMenuRequested.connect(self.show_image_context_menu)
        self.image_table.itemClicked.connect(self.on_image_selected)
        self.image_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_table.horizontalHeader().setStretchLastSection(True)
        self.image_splitter.addWidget(self.image_table)
        
        # 图片预览
        self.image_preview = QLabel()
        self.image_preview.setAlignment(Qt.AlignCenter)
        self.image_preview.setMinimumSize(300, 200)
        self.image_preview.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.image_splitter.addWidget(self.image_preview)
        
        # 设置图片列表和预览框的比例
        # 使图片列表高度与ROM列表一致，预览框占据剩余空间
        self.image_splitter.setSizes([400, 300])  # 图片列表400，预览框300
        
        # 设置分割器的大小策略
        self.image_splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.image_layout.addWidget(self.image_splitter)
        
        # 图片操作按钮已移至右键菜单
        
        self.image_group.setLayout(self.image_layout)
        splitter.addWidget(self.image_group)
        
        # 设置分割器比例
        splitter.setSizes([300, 400, 500])
        main_layout.addWidget(splitter)
        
        # 底部控制面板 - 简化布局
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)
        control_layout.setContentsMargins(5, 5, 5, 5)
        
        # 直接添加路径标签
        control_layout.addWidget(self.plugins_label)
        control_layout.addWidget(self.roms_label)
        control_layout.addWidget(self.images_label)
        control_layout.addWidget(self.custom_titles_label)
        
        # 主布局 - 调整比例
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(splitter, stretch=1)  # 主内容区域占据所有可用空间
        layout.addWidget(control_panel, stretch=0)  # 控制面板固定高度
        
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
    
    def select_plugins_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, self.tr('select_plugin_dir'))
        if dir_path:
            self.plugins_dir = dir_path
            self.plugins_label.setText(f"插件目录: {dir_path}")
            self.logger.info(f"设置插件目录: {dir_path}")
    
    def select_roms_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "选择ROM目录")
        if dir_path:
            self.roms_dir = dir_path
            self.roms_label.setText(f"ROM目录: {dir_path}")
            self.logger.info(f"设置ROM目录: {dir_path}")
    
    def select_images_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "选择图片目录")
        if dir_path:
            self.images_dir = dir_path
            self.images_label.setText(f"图片目录: {dir_path}")
            self.logger.info(f"设置图片目录: {dir_path}")

    def select_custom_titles_file(self):
        """选择自定义标题文件"""
        file_path, _ = QFileDialog.getOpenFileName(self, "选择自定义标题文件", "", "INI Files (*.ini)")
        if file_path:
            self.custom_titles_file = file_path
            self.custom_titles_label.setText(f"自定义标题文件: {file_path}")
            self.logger.info(f"设置自定义标题文件: {file_path}")
            
    def scan_plugins(self):
        """扫描插件目录，解析INI文件"""
        if not self.plugins_dir:
            return
            
        self.plugins = []
        self.plugin_list_widget.clear()
        
        # 扫描目录
        plugin_files = []
        if self.subdir_check.isChecked():
            # 扫描子目录
            for root, dirs, files in os.walk(self.plugins_dir):
                for file in files:
                    if file.lower().endswith('.ini'):
                        plugin_files.append(os.path.join(root, file))
        else:
            # 只扫描当前目录
            for file in os.listdir(self.plugins_dir):
                if file.lower().endswith('.ini'):
                    plugin_files.append(os.path.join(self.plugins_dir, file))
        
        # 解析插件
        for plugin_file in plugin_files:
            plugin = self.parse_plugin(plugin_file)
            if plugin:
                self.plugins.append(plugin)
        
        # 按displayname排序
        self.plugins.sort(key=lambda x: x.get('displayname', ''))
        
        # 显示插件列表
        for plugin in self.plugins:
            self.plugin_list_widget.addItem(plugin.get('displayname', '未知插件'))
    
    def parse_plugin(self, file_path):
        """解析插件INI文件"""
        config = configparser.ConfigParser()
        try:
            config.read(file_path, encoding='utf-8')
            if 'PLUGIN' in config:
                plugin = dict(config['PLUGIN'])
                plugin['filepath'] = file_path
                
                # 确保有必要的字段
                if 'displayname' not in plugin:
                    plugin['displayname'] = os.path.splitext(os.path.basename(file_path))[0]
                if 'filetypes' not in plugin:
                    plugin['filetypes'] = ''
                if 'romdir' not in plugin:
                    plugin['romdir'] = ''
                if 'coverfolder' not in plugin:
                    plugin['coverfolder'] = ''
                if 'magic' not in plugin:
                    plugin['magic'] = ''
                    
                return plugin
        except Exception as e:
            print(f"解析插件错误: {e}")
        return None
    
    def on_plugin_selected(self, item):
        """插件选择事件"""
        index = self.plugin_list_widget.row(item)
        if 0 <= index < len(self.plugins):
            self.current_plugin = self.plugins[index]
            self.load_roms()
            self.load_images()
    
    def load_roms(self):
        """加载当前插件的ROM列表(支持自定义标题)"""
        from PyQt5.QtGui import QColor
        
        self.rom_table.setRowCount(0)
        if not self.current_plugin or not self.roms_dir:
            self.logger.warning("无法加载ROM: 插件或ROM目录未设置")
            return
            
        # 加载自定义标题
        self.load_custom_titles()
        self.logger.info(f"加载自定义标题: {len(self.custom_titles)}条记录")
        
        # 获取并规范化ROM目录路径
        rom_dir = os.path.normpath(os.path.join(self.roms_dir, self.current_plugin.get('romdir', '')))
        if not os.path.exists(rom_dir):
            self.logger.error(f"ROM目录不存在: {rom_dir}")
            QMessageBox.warning(self, "错误", f"ROM目录不存在:\n{rom_dir}\n请检查路径配置")
            return
            
        # 获取图片目录路径
        cover_folder = self.current_plugin.get('coverfolder', 'NES')
        image_dir = os.path.normpath(os.path.join(self.images_dir, cover_folder))
        
        # 处理文件类型
        file_types = [ext.lower().strip() for ext in self.current_plugin.get('filetypes', '').split('|') if ext]
        if not file_types:
            self.logger.error("插件未配置有效的文件类型")
            QMessageBox.warning(self, "错误", "插件未配置有效的文件类型")
            return
            
        self.logger.info(f"扫描ROM目录: {rom_dir} (文件类型: {file_types})")
            
        # 扫描ROM文件(包括隐藏文件和目录)
        rom_files = []
        for entry in os.scandir(rom_dir):
            # 跳过.和..目录
            if entry.name in ('.', '..'):
                continue
                
            # 检查是否是文件(包括隐藏文件)
            if entry.is_file():
                file_lower = entry.name.lower()
                if any(file_lower.endswith(ext) for ext in file_types):
                    filename = os.path.basename(entry.name)
                    display_name = self.get_display_name(filename)
                    rom_files.append((filename, display_name))
                    self.logger.debug(f"找到ROM文件: {entry.name} (显示为: {display_name})")
                    # 调试输出自定义标题查找结果
                    self.logger.debug(f"自定义标题查找结果: {filename} -> {display_name}")
            
            # 如果是目录(包括隐藏目录)，递归扫描
            elif entry.is_dir():
                sub_dir = os.path.join(rom_dir, entry.name)
                for sub_entry in os.scandir(sub_dir):
                    if sub_entry.is_file():
                        file_lower = sub_entry.name.lower()
                        if any(file_lower.endswith(ext) for ext in file_types):
                            filename = os.path.basename(sub_entry.name)
                            display_name = self.get_display_name(filename)
                            rom_files.append((filename, display_name))
                            self.logger.debug(f"找到ROM文件: {entry.name}/{sub_entry.name} (显示为: {display_name})")
        
        # 按显示名称排序后添加到表格
        self.rom_table.setRowCount(len(rom_files))
        for i, (filename, display_name) in enumerate(sorted(rom_files, key=lambda x: x[1])):
            # 检查是否有对应图片
            base_name = os.path.splitext(filename)[0]
            has_image = False
            if os.path.exists(image_dir):
                for ext in ['.png', '.jpg', '.jpeg', '.bmp', '.gif']:
                    if os.path.exists(os.path.join(image_dir, base_name + ext)):
                        has_image = True
                        break
            
            # 创建表格项并确保显示名称正确
            filename_item = QTableWidgetItem(filename)
            display_name_item = QTableWidgetItem(display_name)
            
            # 强制设置显示名称
            display_name_item.setText(display_name)
            self.logger.debug(f"设置表格项: 文件名={filename}, 显示名称={display_name}")
            
            # 如果没有图片，设置红色背景
            if not has_image:
                filename_item.setBackground(QColor(255, 200, 200))  # 浅红色
                display_name_item.setBackground(QColor(255, 200, 200))
                self.logger.debug(f"ROM {filename} 没有对应的图片")
            
            # 立即设置表格项并刷新
            self.rom_table.setItem(i, 0, filename_item)
            self.rom_table.setItem(i, 1, display_name_item)
            self.rom_table.viewport().update()
        
        # 启用编辑功能
        self.rom_table.cellChanged.connect(self.on_rom_name_changed)
        self.logger.info(f"加载完成: {len(rom_files)}个ROM(来自{rom_dir})")
        self.rom_count_label.setText(f"({len(rom_files)})")
        
    def on_rom_name_changed(self, row, column):
        """ROM名称编辑事件"""
        if column != 1:  # 只处理显示名称列的修改
            return
            
        filename_item = self.rom_table.item(row, 0)
        display_name_item = self.rom_table.item(row, 1)
        
        if not filename_item or not display_name_item:
            return
            
        filename = filename_item.text()
        display_name = display_name_item.text()
        
        # 更新自定义标题
        base_name = os.path.splitext(filename)[0]
        self.custom_titles[base_name] = display_name
        
        # 标记需要保存
        self.custom_titles_modified = True
        
    def save_custom_titles(self):
        """保存自定义标题到文件"""
        if not hasattr(self, 'custom_titles_file') or not self.custom_titles_file:
            # 使用默认位置
            self.custom_titles_file = os.path.join(os.path.dirname(self.plugins_dir), 'custom_titles.ini')
            self.logger.info(f"使用默认自定义标题文件路径: {self.custom_titles_file}")
            
        config = configparser.ConfigParser()
        
        # 保留其他插件的自定义标题
        if os.path.exists(self.custom_titles_file):
            try:
                config.read(self.custom_titles_file, encoding='utf-8')
                self.logger.debug(f"读取现有自定义标题文件: {self.custom_titles_file}")
            except Exception as e:
                self.logger.error(f"读取自定义标题文件错误: {e}")
                return False
        
        # 更新当前插件的自定义标题
        magic = self.current_plugin.get('magic', '')
        if not magic:
            self.logger.warning("无法保存: 当前插件没有magic值")
            return False
            
        if magic not in config:
            config[magic] = {}
            self.logger.debug(f"为magic值 '{magic}' 创建新节")
            
        config[magic].update(self.custom_titles)
        self.logger.info(f"准备保存 {len(self.custom_titles)} 条自定义标题到 {magic} 节")
            
        # 写入文件
        try:
            with open(self.custom_titles_file, 'w', encoding='utf-8') as f:
                config.write(f)
            self.custom_titles_modified = False
            self.logger.info(f"成功保存自定义标题到 {self.custom_titles_file}")
            return True
        except Exception as e:
            self.logger.error(f"保存自定义标题错误: {e}")
            return False
    
    def load_custom_titles(self):
        """安全加载自定义标题文件"""
        try:
            # 使用深拷贝避免数据污染
            from copy import deepcopy
            import configparser
            
            # 初始化新的字典
            new_titles = deepcopy(self.custom_titles) if hasattr(self, 'custom_titles') else {}
            
            # 获取文件路径
            custom_file = getattr(self, 'custom_titles_file', None)
            if not custom_file:
                custom_file = os.path.join(os.path.dirname(self.plugins_dir), 'custom_titles.ini')
            
            if os.path.exists(custom_file):
                config = configparser.ConfigParser()
                try:
                    # 保留注释和大小写
                    config.optionxform = str  
                    # 使用严格模式解析
                    config.read(custom_file, encoding='utf-8')
                    
                    # 验证并加载所有节
                    for section in config.sections():
                        section_data = new_titles.get(section, {})
                        for key, value in config.items(section):
                            try:
                                # 严格验证键值格式
                                if not isinstance(key, str) or not isinstance(value, str):
                                    raise ValueError(f"无效的键值类型: key={type(key)}, value={type(value)}")
                                
                                clean_key = key.strip()
                                clean_value = value.strip()
                                if not clean_key or '%' in clean_value:  # 过滤含特殊字符的值
                                    continue
                                    
                                section_data[clean_key] = clean_value
                                self.logger.debug(f"加载自定义标题: [{section}] '{clean_key}' = '{clean_value}'")
                            except Exception as e:
                                self.logger.error(f"处理自定义标题条目错误: {e}")
                                continue
                        
                        if section_data:  # 只添加非空节
                            new_titles[section] = section_data
                    
                    # 原子性更新
                    self.custom_titles = deepcopy(new_titles)
                    
                    # 记录加载状态
                    magic = self.current_plugin.get('magic', '')
                    if magic in self.custom_titles:
                        count = len(self.custom_titles[magic])
                        self.logger.info(f"成功加载自定义标题: Magic节 '{magic}' 包含 {count} 条记录")
                    else:
                        self.logger.warning(f"未找到匹配的magic节 '{magic}'")
                    
                    # 调试信息
                    self.logger.debug(f"当前加载的magic节: {list(self.custom_titles.keys())}")
                    return True
                    
                except Exception as e:
                    self.logger.error(f"解析自定义标题文件错误: {e}")
                    QMessageBox.warning(self, "错误", "自定义标题文件格式错误")
            else:
                self.logger.warning(f"自定义标题文件不存在: {custom_file}")
                
        except Exception as e:
            self.logger.error(f"加载自定义标题严重错误: {e}")
            QMessageBox.critical(self, "错误", "无法加载自定义标题")
            
        return False
    
    def get_display_name(self, filename):
        """获取ROM的显示名称（使用不含扩展名的文件名作为键）"""
        base_name = os.path.splitext(filename)[0]  # 去掉扩展名
        magic = self.current_plugin.get('magic', '')
        
        self.logger.debug(f"查找自定义标题: 文件名={filename}, 查找键={base_name}, magic={magic}")
        
        if magic and magic in self.custom_titles:
            try:
                magic_section = self.custom_titles[magic]
                if isinstance(magic_section, dict) and base_name in magic_section:
                    title = magic_section[base_name]
                    self.logger.debug(f"找到匹配的自定义标题: {title}")
                    return str(title).strip()
            except Exception as e:
                self.logger.error(f"获取自定义标题错误: {e}")
        
        self.logger.debug(f"未找到自定义标题，使用文件名: {base_name}")
        return base_name
   
    def load_images(self):
        """加载当前插件的图片(根据ROM文件名查找.png图片)"""
        from PyQt5.QtGui import QColor
        
        if not self.current_plugin or not self.images_dir:
            self.logger.warning("无法加载图片: 插件或图片目录未设置")
            return
            
        # 获取图片目录
        cover_folder = self.current_plugin.get('coverfolder', 'NES')
        image_dir = os.path.normpath(os.path.join(self.images_dir, cover_folder))
        
        # 检查图片目录是否存在
        if not os.path.exists(image_dir):
            self.logger.warning(f"图片目录不存在: {image_dir}")
            QMessageBox.warning(self, "警告", f"图片目录不存在:\n{image_dir}")
            return
            
        # 清空图片列表
        self.image_table.setRowCount(0)
        found_images = []
            
        # 遍历ROM表格中的每一项
        for row in range(self.rom_table.rowCount()):
            filename_item = self.rom_table.item(row, 0)
            display_name_item = self.rom_table.item(row, 1)
            
            if filename_item and display_name_item:
                # 获取ROM文件名信息
                rom_fullname = filename_item.text()  # 包含扩展名
                rom_name, rom_ext = os.path.splitext(rom_fullname)
                
                # 严格按ROM文件名(带扩展名)+.png格式查找图片
                image_path = os.path.join(image_dir, rom_name + rom_ext + ".png")
                self.logger.debug(f"查找图片: {image_path}")
                
                if os.path.exists(image_path):
                    # 图片存在，清除任何标记
                    filename_item.setBackground(QColor(255, 255, 255))  # 白色
                    display_name_item.setBackground(QColor(255, 255, 255))
                    self.logger.debug(f"找到图片: {rom_name}.png")
                    
                    # 获取图片分辨率
                    try:
                        from PIL import Image
                        with Image.open(image_path) as img:
                            resolution = f"{img.width}×{img.height}"
                    except Exception as e:
                        self.logger.warning(f"获取图片分辨率失败: {e}")
                        resolution = "未知"
                    
                    found_images.append((os.path.basename(image_path), resolution))
                else:
                    # 图片不存在，标记为红色
                    filename_item.setBackground(QColor(255, 200, 200))  # 浅红色
                    display_name_item.setBackground(QColor(255, 200, 200))
                    self.logger.debug(f"未找到图片: {rom_name}.png")
                    
        # 更新图片表格
        self.image_table.setRowCount(len(found_images))
        for i, (image, resolution) in enumerate(sorted(found_images)):
            self.image_table.setItem(i, 0, QTableWidgetItem(image))
            self.image_table.setItem(i, 1, QTableWidgetItem(resolution))
            
        # 更新图片计数
        self.image_count_label.setText(f"({len(found_images)})")
        self.logger.info(f"图片检查完成: {self.rom_table.rowCount()}个ROM检查完毕, 找到{len(found_images)}张图片")
    def is_rom_exists(self, rom_name):
        """检查是否存在对应的ROM文件"""
        if not self.current_plugin or not self.roms_dir:
            self.logger.debug(f"ROM检查失败: 插件或ROM目录未设置")
            return False
            
        # 规范化路径处理
        rom_dir = os.path.normpath(os.path.join(self.roms_dir, self.current_plugin.get('romdir', '')))
        if not os.path.exists(rom_dir):
            self.logger.warning(f"ROM目录不存在: {rom_dir}")
            return False
            
        file_types = [ext.lower().strip() for ext in self.current_plugin.get('filetypes', '').split('|') if ext]
        if not file_types:
            self.logger.warning(f"无有效的文件类型配置: {self.current_plugin.get('filetypes', '')}")
            return False
        
        # 检查是否有ROM文件名匹配图片名
        for ext in file_types:
            rom_path = os.path.normpath(os.path.join(rom_dir, rom_name))
            if os.path.exists(rom_path):
                self.logger.debug(f"找到匹配ROM: {rom_path}")
                return True
                
        self.logger.debug(f"未找到匹配ROM: {rom_name} (在目录: {rom_dir}),扩展名: {ext}")
        return False
    
    def on_image_selected(self, item):
        """图片选择事件"""
        if not self.current_plugin or not self.images_dir:
            return
            
        # 获取选中行的图片文件名(第一列)
        row = item.row()
        image_item = self.image_table.item(row, 0)
        if not image_item:
            return
            
        image_dir = os.path.join(self.images_dir, self.current_plugin.get('coverfolder', ''))
        image_path = os.path.join(image_dir, image_item.text())
        
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            self.image_preview.setPixmap(pixmap.scaled(
                self.image_preview.width(), 
                self.image_preview.height(),
                Qt.KeepAspectRatio
            ))
            
    def resize_image(self):
        """调整图片大小"""
        selected_items = self.image_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, self.tr('warning'), self.tr('no_image_selected'))
            return
            
        # 获取选中行的图片文件名(第一列)
        row = selected_items[0].row()
        image_item = self.image_table.item(row, 0)
        if not image_item:
            return
            
        image_dir = os.path.join(self.images_dir, self.current_plugin.get('coverfolder', ''))
        image_path = os.path.join(image_dir, image_item.text())
        
        # 关闭预览释放文件锁
        self.image_preview.setPixmap(QPixmap())
        
        # 获取当前尺寸作为默认值
        try:
            from PIL import Image
            with Image.open(image_path) as img:
                current_width, current_height = img.size
        except Exception as e:
            QMessageBox.warning(self, "错误", f"获取图片尺寸失败: {e}")
            return
            
        # 获取新尺寸
        width, ok = QInputDialog.getInt(self, "调整大小", "输入新宽度(像素):", 
                                      current_width, 50, 4000, 1)
        if not ok:
            return
            
        height, ok = QInputDialog.getInt(self, "调整大小", "输入新高度(像素):", 
                                       current_height, 50, 4000, 1)
        if not ok:
            return
            
        # 方法1: 使用QPixmap直接调整(适用于简单缩放)
        try:
            # 加载原图
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                raise Exception("无法加载图片")
                
            # 缩放图片
            scaled_pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            # 保存到临时文件(同目录)
            temp_path = os.path.join(image_dir, f"temp_resize_{os.path.basename(image_path)}")
            if not scaled_pixmap.save(temp_path):
                raise Exception("保存临时文件失败")
                
            # 备份原文件
            backup_path = image_path + ".bak"
            if os.path.exists(backup_path):
                os.remove(backup_path)
            os.rename(image_path, backup_path)
            
            # 替换文件
            os.rename(temp_path, image_path)
            os.remove(backup_path)
            
            # 更新表格中的分辨率显示
            self.image_table.item(row, 1).setText(f"{width}×{height}")
            
            # 刷新预览
            self.on_image_selected(selected_items[0])
            
            QMessageBox.information(self, "成功", f"图片已调整为 {width}×{height} 像素")
            return
        except Exception as e:
            self.logger.error(f"QPixmap调整大小失败: {e}")
            
        # 方法2: 使用PIL作为备选方案
        try:
            from PIL import Image
            
            # 在同目录创建临时文件
            temp_path = os.path.join(image_dir, f"temp_resize_{os.path.basename(image_path)}")
            
            # 调整大小并保存
            with Image.open(image_path) as img:
                img = img.resize((width, height), Image.LANCZOS)
                img.save(temp_path, quality=95)
            
            # 备份并替换原文件
            backup_path = image_path + ".bak"
            if os.path.exists(backup_path):
                os.remove(backup_path)
            os.replace(image_path, backup_path)
            os.replace(temp_path, image_path)
            os.remove(backup_path)
            
            # 更新表格中的分辨率显示
            self.image_table.item(row, 1).setText(f"{width}×{height}")
            
            # 刷新预览
            self.on_image_selected(selected_items[0])
            
            QMessageBox.information(self, "成功", f"图片已调整为 {width}×{height} 像素")
        except PermissionError as e:
            QMessageBox.warning(self, "权限错误", 
                f"无法修改图片，请确保:\n1. 文件未被其他程序占用\n2. 有写入权限\n3. 磁盘空间充足\n错误详情: {e}")
        except Exception as e:
            QMessageBox.warning(self, "错误", 
                f"调整图片大小失败:\n{str(e)}\n请尝试关闭其他可能占用此文件的程序后重试")
            
    def convert_image_format(self):
        """转换图片格式"""
        selected_items = self.image_list_widget.selectedItems()
        if not selected_items:
            return
            
        from PyQt5.QtWidgets import QInputDialog, QMessageBox
        from PIL import Image
        
        item = selected_items[0]
        image_dir = os.path.join(self.images_dir, self.current_plugin.get('coverfolder', ''))
        image_path = os.path.join(image_dir, item.text())
        
        # 获取新格式
        formats = ["PNG", "JPEG", "BMP", "GIF"]
        format, ok = QInputDialog.getItem(self, "转换格式", "选择新格式:", formats, 0, False)
        if not ok:
            return
            
        # 转换格式
        try:
            img = Image.open(image_path)
            new_path = os.path.splitext(image_path)[0] + f".{format.lower()}"
            img.save(new_path, format)
            
            # 删除旧文件
            if new_path != image_path:
                os.remove(image_path)
                self.image_list_widget.takeItem(self.image_list_widget.row(item))
                self.image_list_widget.addItem(os.path.basename(new_path))
        except Exception as e:
            QMessageBox.warning(self, "错误", f"转换格式失败: {e}")
            
    def rename_image(self):
        """重命名图片"""
        selected_items = self.image_table.selectedItems()
        if not selected_items:
            return
            
        from PyQt5.QtWidgets import QInputDialog, QMessageBox
        
        item = selected_items[0]
        image_dir = os.path.join(self.images_dir, self.current_plugin.get('coverfolder', ''))
        image_path = os.path.join(image_dir, item.text())
        
        # 获取新名称
        new_name, ok = QInputDialog.getText(self, "重命名", "输入新名称:", text=item.text())
        if not ok or not new_name:
            return
            
        # 重命名文件
        try:
            new_path = os.path.join(image_dir, new_name)
            os.rename(image_path, new_path)
            item.setText(new_name)
        except Exception as e:
            QMessageBox.warning(self, "错误", f"重命名失败: {e}")

    def setup_logging(self):
        """初始化或重新配置日志"""
        import logging
        
        # 移除所有已存在的处理器
        root = logging.getLogger()
        for handler in root.handlers[:]:
            root.removeHandler(handler)
            
        if self.logging_enabled:
            # 启用日志
            logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s - %(levelname)s - %(message)s',
                filename='wii_plugin_tool.log',
                filemode='a'  # 改为追加模式，避免每次开关日志都清空文件
            )
            self.logger = logging.getLogger(__name__)
            
            # 禁用PIL的DEBUG日志
            logging.getLogger('PIL').setLevel(logging.INFO)
            
            self.logger.info("日志功能已启用")
        else:
            # 完全禁用所有日志
            logging.basicConfig(handlers=[logging.NullHandler()])
            
            # 设置根日志记录器级别为CRITICAL+1，确保不记录任何日志
            root.setLevel(logging.CRITICAL + 1)
            
            # 确保所有已知的日志记录器都被禁用
            for name in logging.root.manager.loggerDict:
                logger = logging.getLogger(name)
                logger.handlers = []
                logger.propagate = False
                logger.setLevel(logging.CRITICAL + 1)
            
            # 设置当前实例的日志记录器
            self.logger = logging.getLogger(__name__)
            self.logger.addHandler(logging.NullHandler())
            self.logger.propagate = False
            self.logger.setLevel(logging.CRITICAL + 1)

    def toggle_logging(self):
        """切换日志功能状态"""
        self.logging_enabled = not self.logging_enabled
        self.setup_logging()
        
        if self.logging_enabled:
            self.logging_btn.setText("📝 日志")
            self.logging_btn.setToolTip("点击切换日志记录功能 (当前: 启用)")
            self.statusBar().showMessage("日志记录已启用", 3000)
            self.logger.info("日志功能已启用")
        else:
            self.logging_btn.setText("📝 日志")
            self.logging_btn.setToolTip("点击切换日志记录功能 (当前: 禁用)")
            self.statusBar().showMessage("日志记录已禁用", 3000)
            
        self.logging_btn.setChecked(self.logging_enabled)

    def open_custom_titles_file(self):
        """打开自定义标题文件"""
        if not hasattr(self, 'custom_titles_file') or not self.custom_titles_file:
            # 使用默认位置
            self.custom_titles_file = os.path.join(os.path.dirname(self.plugins_dir), 'custom_titles.ini')
            
        if not os.path.exists(self.custom_titles_file):
            # 如果文件不存在，创建一个空文件
            try:
                with open(self.custom_titles_file, 'w', encoding='utf-8') as f:
                    f.write("; 自定义标题配置文件\n")
                    f.write("; 格式: [magic]\n")
                    f.write("; ROM文件名=显示名称\n")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"创建自定义标题文件失败: {e}")
                return
                
        try:
            import subprocess
            subprocess.Popen(f'notepad "{self.custom_titles_file}"')
            self.logger.info(f"打开自定义标题文件: {self.custom_titles_file}")
        except Exception as e:
            QMessageBox.warning(self, "错误", f"打开文件失败: {e}")
            self.logger.error(f"打开自定义标题文件失败: {e}")

    def toggle_topmost(self):
        """切换窗口置顶状态"""
        self.always_on_top = not self.always_on_top
        if self.always_on_top:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            self.topmost_btn.setText("📌 取消")
            if hasattr(self, 'logger'):
                self.logger.info("窗口设置为置顶模式")
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
            self.topmost_btn.setText("📌 置顶")
            if hasattr(self, 'logger'):
                self.logger.info("取消窗口置顶模式")
        
        # 需要重新显示窗口使设置生效
        self.show()
        self.topmost_btn.setChecked(self.always_on_top)

    # def save_plugin_config(self):
    #     """保存当前插件配置到INI文件"""
    #     if not self.current_plugin:
    #         from PyQt5.QtWidgets import QMessageBox
    #         QMessageBox.warning(self, "警告", "没有选中的插件")
    #         return
            
    #     file_path = self.current_plugin.get('filepath', '')
    #     if not file_path:
    #         return
            
    #     try:
    #         config = configparser.ConfigParser()
    #         config.read(file_path, encoding='utf-8')
            
    #         # 更新PLUGIN节
    #         if 'PLUGIN' not in config:
    #             config['PLUGIN'] = {}
                
    #         # 保留所有原始配置项
    #         for key, value in self.current_plugin.items():
    #             if key != 'filepath':  # 跳过内部使用的filepath
    #                 config['PLUGIN'][key] = value
            
    #         # 写入文件
    #         with open(file_path, 'w', encoding='utf-8') as f:
    #             config.write(f)
                
    #         from PyQt5.QtWidgets import QMessageBox
    #         QMessageBox.information(self, "成功", "插件配置已保存")
            
    #     except Exception as e:
    #         from PyQt5.QtWidgets import QMessageBox
    #         QMessageBox.critical(self, "错误", f"保存配置失败: {e}")

    def show_rom_context_menu(self, pos):
        """显示ROM表格的右键菜单"""
        menu = QMenu()
        
        # 添加打开文件夹选项
        open_folder_action = menu.addAction(self.tr("open_rom_folder"))
        open_folder_action.triggered.connect(self.open_rom_folder)
        
        # 只在有选中行时显示菜单
        if self.rom_table.selectedItems():
            menu.exec_(self.rom_table.viewport().mapToGlobal(pos))
            
    def open_rom_folder(self):
        """打开选中ROM所在的文件夹"""
        selected_items = self.rom_table.selectedItems()
        if not selected_items:
            return
            
        row = selected_items[0].row()
        filename_item = self.rom_table.item(row, 0)
        if not filename_item:
            return
            
        try:
            rom_dir = os.path.normpath(os.path.join(self.roms_dir, self.current_plugin.get('romdir', '')))
            rom_path = os.path.join(rom_dir, filename_item.text())
            folder_path = os.path.dirname(rom_path)
            
            if os.path.exists(folder_path):
                import subprocess
                subprocess.Popen(f'explorer "{folder_path}"')
            else:
                QMessageBox.warning(self, "错误", "文件夹不存在")
        except Exception as e:
            QMessageBox.warning(self, "错误", f"打开文件夹失败: {e}")
            
    def show_image_context_menu(self, pos):
        """显示图片表格的右键菜单"""
        menu = QMenu()
        
        # 添加打开文件夹选项
        open_folder_action = menu.addAction(self.tr("open_images_folder"))
        open_folder_action.triggered.connect(self.open_image_folder)
        
        # 添加操作选项
        resize_action = menu.addAction(self.tr("resize_image"))
        resize_action.triggered.connect(self.resize_image)
        
        convert_action = menu.addAction(self.tr("convert_format"))
        convert_action.triggered.connect(self.convert_image_format)
        
        rename_action = menu.addAction(self.tr("rename_image"))
        rename_action.triggered.connect(self.rename_image)
        
        # 只在有选中行时显示菜单
        if self.image_table.selectedItems():
            menu.exec_(self.image_table.viewport().mapToGlobal(pos))
            
    def show_plugin_context_menu(self, pos):
        """显示插件列表的右键菜单"""
        menu = QMenu()
        
        # 添加编辑选项
        edit_action = menu.addAction("编辑插件(edit plugin ini file)")
        edit_action.triggered.connect(self.edit_selected_plugin)
        
        # 添加删除选项
        delete_action = menu.addAction("删除插件move plugin ini file to bak")
        delete_action.triggered.connect(self.delete_selected_plugin)
        
        # 只在有选中项时显示菜单
        if self.plugin_list_widget.selectedItems():
            menu.exec_(self.plugin_list_widget.viewport().mapToGlobal(pos))
            
    def edit_selected_plugin(self):
        """编辑选中的插件INI文件"""
        selected_items = self.plugin_list_widget.selectedItems()
        if not selected_items:
            return
            
        index = self.plugin_list_widget.row(selected_items[0])
        if 0 <= index < len(self.plugins):
            plugin = self.plugins[index]
            file_path = plugin.get('filepath', '')
            
            if file_path and os.path.exists(file_path):
                try:
                    import subprocess
                    subprocess.Popen(f'notepad "{file_path}"')
                    # 编辑后重新加载插件列表
                    self.scan_plugins()
                except Exception as e:
                    QMessageBox.warning(self, "错误", f"打开文件失败: {e}")
            else:
                QMessageBox.warning(self, "错误", "插件文件不存在")
                
    def delete_selected_plugin(self):
        """删除选中的插件(移动到bak目录)"""
        selected_items = self.plugin_list_widget.selectedItems()
        if not selected_items:
            return
            
        index = self.plugin_list_widget.row(selected_items[0])
        if 0 <= index < len(self.plugins):
            plugin = self.plugins[index]
            file_path = plugin.get('filepath', '')
            
            if file_path and os.path.exists(file_path):
                # 确认删除
                reply = QMessageBox.question(
                    self, '确认删除', 
                    f'确定要删除插件 "{plugin.get("displayname", "")}" 吗?\n文件将移动到bak目录。',
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                )
                
                if reply == QMessageBox.Yes:
                    try:
                        # 创建bak目录(如果不存在)
                        bak_dir = os.path.join(os.path.dirname(file_path), 'bak')
                        os.makedirs(bak_dir, exist_ok=True)
                        
                        # 移动文件到bak目录
                        import shutil
                        bak_path = os.path.join(bak_dir, os.path.basename(file_path))
                        shutil.move(file_path, bak_path)
                        
                        # 重新加载插件列表
                        self.scan_plugins()
                        QMessageBox.information(self, "成功", "插件已移动到bak目录")
                    except Exception as e:
                        QMessageBox.warning(self, "错误", f"删除插件失败: {e}")
            else:
                QMessageBox.warning(self, "错误", "插件文件不存在")
            
    def open_image_folder(self):
        """打开选中图片所在的文件夹"""
        selected_items = self.image_table.selectedItems()
        if not selected_items:
            return
            
        row = selected_items[0].row()
        image_item = self.image_table.item(row, 0)
        if not image_item:
            return
            
        try:
            image_dir = os.path.normpath(os.path.join(self.images_dir, self.current_plugin.get('coverfolder', '')))
            image_path = os.path.join(image_dir, image_item.text())
            folder_path = os.path.dirname(image_path)
            
            if os.path.exists(folder_path):
                import subprocess
                subprocess.Popen(f'explorer "{folder_path}"')
            else:
                QMessageBox.warning(self, "错误", "文件夹不存在")
        except Exception as e:
            QMessageBox.warning(self, "错误", f"打开文件夹失败: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WiiPluginManager()
    window.show()
    sys.exit(app.exec_())