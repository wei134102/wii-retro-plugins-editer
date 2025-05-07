# Wii Retro Game Plugins Editor

## 安装与使用指南 (中文)

### 系统要求
- Python 3.8+
- PyQt5
- Pillow (图像处理库)

### 安装步骤
1. 创建虚拟环境：
   ```
   python -m venv venv
   ```
2. 激活虚拟环境：
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
3. 安装依赖：
   ```
   pip install PyQt5 pillow
   ```
4. 运行程序：
   ```
   python main.py
   ```

### 支持的插件类型
- wii flow plugins
- usbloader_gx plugins

### 主要功能
1. Wii复古游戏插件配置文件管理
2. 游戏封面图片批量处理
3. 自定义游戏标题编辑
4. 插件配置扫描与加载

### 插件配置
1. 将插件文件(.ini)放入plugins目录
2. 首次运行时选择插件目录
3. 使用"扫描插件"按钮加载配置
4. 右键点击插件进行编辑

### 特色功能
- 可视化界面管理插件配置
- 批量重命名和转换图片格式
- 中英文双语界面支持
- 一键扫描并加载插件目录
- 实时预览配置更改效果

---

## Installation & Usage (English)

### System Requirements
- Python 3.8+
- PyQt5
- Pillow (Image processing library)

### Installation Steps
1. Create virtual environment:
   ```
   python -m venv venv
   ```
2. Activate virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
3. Install dependencies:
   ```
   pip install PyQt5 pillow
   ```
4. Run the program:
   ```
   python main.py
   ```

### Supported Plugin Types
- wii flow plugins
- usbloader_gx plugins

### Main Features
1. Wii retro game plugins configuration management
2. Batch processing of game cover images
3. Custom game title editing
4. Plugin configuration scanning and loading

### Plugin Configuration
1. Place plugin files (.ini) in plugins directory
2. Select plugin directory on first run
3. Use "Scan Plugins" button to load configurations
4. Right-click plugins to edit

### Key Features
- Visual interface for plugin management
- Batch rename and convert image formats
- Bilingual UI support (Chinese/English)
- One-click scan and load plugin directory
- Real-time preview of configuration changes