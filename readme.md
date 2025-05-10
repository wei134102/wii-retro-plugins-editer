# Wii Retro Game Plugins Editor
![en](https://github.com/user-attachments/assets/bb3eafd1-928e-40f3-9b71-41c0c65a36db)![zhcn](https://github.com/user-attachments/assets/e6825182-f510-4eab-a55b-7f24f9b38bea)

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

#### 插件管理
1. 扫描和加载插件配置文件(.ini)
2. 编辑插件配置（右键菜单）
3. 删除插件（移动到bak目录）
4. 支持子目录扫描

#### ROM管理
1. 显示ROM列表及其对应的显示名称
2. 重命名ROM文件（支持同时重命名对应图片）
3. 删除ROM文件
4. 双击ROM文件名复制到剪贴板
5. 右键菜单打开ROM所在文件夹

#### 图片管理
1. 显示与ROM对应的图片
2. 调整图片大小（保持或不保持比例）
3. 重命名图片文件
4. 打开图片所在文件夹
5. 选中ROM时自动显示对应图片
6. 图片状态指示（有/无图片）

#### 自定义标题
1. 加载和保存自定义标题配置
2. 编辑ROM的显示名称
3. 打开自定义标题文件进行编辑
4. 自动保存修改的标题

#### 界面功能
1. 中英文双语界面支持（点击"change language"按钮切换）
2. 窗口置顶功能（点击"📌 置顶"按钮）
3. 日志记录功能（可开启/关闭）
4. 状态栏提示信息
5. 可移动的工具栏

### 使用方法

#### 基本设置
1. 点击"插件目录"按钮选择插件配置文件所在目录
2. 点击"ROM目录"按钮选择ROM文件所在目录
3. 点击"图片目录"按钮选择游戏图片所在目录
4. 点击"标题文件"按钮选择自定义标题配置文件（可选）
5. 点击"扫描插件"按钮加载插件配置

#### ROM操作
1. 在左侧插件列表中选择一个插件，中间区域将显示对应的ROM列表
2. 右键点击ROM列表中的项目，可以：
   - 打开ROM所在文件夹
   - 重命名ROM文件（可选择是否同时重命名对应图片）
   - 删除ROM文件
3. 双击ROM文件名可复制文件名到剪贴板
4. 点击ROM列表中的项目，如果有对应图片，将在右侧预览区域显示

#### 图片操作
1. 右键点击图片列表中的项目，可以：
   - 打开图片所在文件夹
   - 调整图片大小
   - 重命名图片文件

#### 自定义标题
1. 在ROM列表中直接编辑"显示名称"列
2. 点击"打开自定义标题"按钮可以直接编辑标题配置文件

#### 其他功能
1. 点击"📌 置顶"按钮可以切换窗口置顶状态
2. 点击"change language"按钮可以切换中英文界面
3. 点击"日志"按钮可以开启/关闭日志记录功能

### 特色功能
- 可视化界面管理插件配置
- ROM与图片的自动关联
- 中英文双语界面支持
- 一键扫描并加载插件目录
- 实时预览配置更改效果
- 双击复制ROM文件名功能

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

#### Plugin Management
1. Scan and load plugin configuration files (.ini)
2. Edit plugin configurations (right-click menu)
3. Delete plugins (move to bak directory)
4. Support for subdirectory scanning

#### ROM Management
1. Display ROM list with custom display names
2. Rename ROM files (with option to rename corresponding images)
3. Delete ROM files
4. Copy ROM filename to clipboard with double-click
5. Open ROM folder from right-click menu

#### Image Management
1. Display images corresponding to ROMs
2. Resize images (with or without maintaining aspect ratio)
3. Rename image files
4. Open image folder
5. Automatically display corresponding image when ROM is selected
6. Image status indication (has/no image)

#### Custom Titles
1. Load and save custom title configurations
2. Edit ROM display names
3. Open custom title file for direct editing
4. Auto-save modified titles

#### Interface Features
1. Bilingual UI support (Chinese/English, toggle with "change language" button)
2. Window always-on-top function (click "📌 Pin" button)
3. Logging functionality (can be enabled/disabled)
4. Status bar notifications
5. Movable toolbar

### Usage Instructions

#### Basic Setup
1. Click "Plugins Dir" button to select plugin configuration directory
2. Click "ROMs Dir" button to select ROM files directory
3. Click "Images Dir" button to select game images directory
4. Click "Title Files" button to select custom title configuration file (optional)
5. Click "Scan Plugins" button to load plugin configurations

#### ROM Operations
1. Select a plugin from the left list, the middle area will display corresponding ROMs
2. Right-click on an item in the ROM list to:
   - Open ROM folder
   - Rename ROM file (with option to rename corresponding image)
   - Delete ROM file
3. Double-click on ROM filename to copy it to clipboard
4. Click on an item in the ROM list, if there's a corresponding image, it will be displayed in the preview area

#### Image Operations
1. Right-click on an item in the image list to:
   - Open image folder
   - Resize image
   - Rename image file

#### Custom Titles
1. Edit the "Display Name" column directly in the ROM list
2. Click "Open Titles" button to edit the title configuration file directly

#### Other Features
1. Click "📌 Pin" button to toggle window always-on-top state
2. Click "change language" button to switch between Chinese and English interface
3. Click "Log" button to enable/disable logging functionality

### Key Features
- Visual interface for plugin management
- Automatic association between ROMs and images
- Bilingual UI support (Chinese/English)
- One-click scan and load plugin directory
- Real-time preview of configuration changes
- Double-click to copy ROM filename feature
