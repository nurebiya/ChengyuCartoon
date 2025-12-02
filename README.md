# 成语连环画生成器

基于AI的成语故事连环画自动生成工具。输入一个成语，系统会自动生成故事、分镜脚本，并创作出精美的连环画。

## ✨ 功能特点

- 📖 **智能故事生成**：基于成语自动生成生动有趣的故事
- 🎬 **自动分镜脚本**：将故事智能拆分为4-10个分镜
- 🎨 **多种漫画风格**：支持国风插画、卡通彩绘、水墨丹青等多种风格
- ✏️ **用户可编辑**：支持编辑分镜脚本和重新生成图片
- 🔄 **工作流编排**：使用LangGraph实现流畅的生成流程

## 🚀 快速开始

### 环境要求

- Python 3.8+
- 阿里云通义千问API密钥（用于文本生成和图像生成）

### 安装步骤

1. **克隆项目**
```bash
git clone <your-repo-url>
cd demo
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置环境变量**
```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的API密钥：
```env
BASE_API_KEY=your_base_api_key_here
BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
BASE_MODEL=qwen-plus
IMG_API_KEY=your_img_api_key_here
IMG_URL=https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
IMG_MODEL=qwen-image-plus
```

### 运行应用

```bash
streamlit run src/main.py
```

应用会在浏览器中自动打开，默认地址：`http://localhost:8501`

## 📖 使用说明

1. **输入成语**：在首页输入一个成语（系统会验证成语是否存在）
2. **查看故事**：系统自动生成基于该成语的故事
3. **编辑分镜**：查看并编辑自动生成的分镜脚本（4-10个分镜）
4. **选择风格**：选择你喜欢的漫画风格
5. **生成漫画**：系统根据分镜和风格生成连环画，可以逐帧查看和重新生成

## 🏗️ 项目结构

```
demo/
├── src/
│   ├── main.py              # 应用入口
│   ├── flow.py              # LangGraph工作流定义
│   ├── nodes/               # 工作流节点
│   │   ├── storyteller.py   # 故事生成节点
│   │   ├── screenwriter.py  # 分镜脚本生成节点
│   │   └── cartoonist.py    # 漫画生成节点
│   ├── llms/                # LLM封装
│   │   ├── base.py          # 基础文本生成LLM
│   │   └── img.py           # 图像生成LLM
│   ├── front/               # Streamlit前端
│   │   ├── pages/           # 页面组件
│   │   ├── components.py    # 通用组件
│   │   └── config.py        # 配置和初始化
│   ├── state/               # 状态管理
│   ├── prompts/             # Prompt模板
│   └── tools/                # 工具函数
│       ├── chengyulist.py   # 成语列表
│       ├── encyclo_reader.py # 百科读取器
│       └── image_merger.py  # 图片合并工具
├── logs/                    # 日志文件
├── .env.example             # 环境变量示例
├── requirements.txt         # 依赖列表
└── README.md               # 项目说明
```

## 🔧 环境变量说明

| 变量名 | 说明 | 示例 | 是否必需 |
|--------|------|------|---------|
| `BASE_API_KEY` | 基础LLM的API密钥（用于生成故事和分镜） | `sk-xxx...` | ✅ 必需 |
| `BASE_URL` | 基础LLM的API地址 | `https://dashscope.aliyuncs.com/compatible-mode/v1` | ⚠️ 可选（代码中未使用） |
| `BASE_MODEL` | 基础LLM模型名称 | `qwen-plus` | ✅ 必需 |
| `IMG_API_KEY` | 图像生成LLM的API密钥 | `sk-xxx...` | ✅ 必需 |
| `IMG_URL` | 图像生成API地址 | `https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation` | ✅ 必需 |
| `IMG_MODEL` | 图像生成模型名称 | `qwen-image-plus` | ✅ 必需 |

**注意**：`BASE_URL` 和 `IMG_URL` 目前在代码中未使用（使用 dashscope SDK 时会自动处理），但可以保留在配置文件中以备将来使用。

## 🎨 支持的漫画风格

- 国风插画 (Chinese Traditional)
- 卡通彩绘 (Cartoon Color)
- 水墨丹青 (Ink Wash)
- 黑白线描 (Black & White Line Art)
- 简笔趣画 (Minimalist Doodle)
- 奇幻唯美 (Fantasy Art)

## 🛠️ 技术栈

- **前端框架**：Streamlit
- **工作流编排**：LangGraph
- **AI模型**：阿里云通义千问（文本生成 + 图像生成）
- **图像处理**：Pillow

## 📝 开发说明

### 工作流流程

```
输入成语 → storyteller（生成故事） → screenwriter（生成分镜） → cartoonist（生成图片）
```

### 日志

日志文件保存在 `logs/` 目录下，按模块和日期分类：
- `app_YYYY-MM-DD.log` - 应用主日志
- `storyteller_YYYY-MM-DD.log` - 故事生成日志
- `screenwriter_YYYY-MM-DD.log` - 分镜生成日志
- `cartoonist_YYYY-MM-DD.log` - 漫画生成日志
- `imgllm_YYYY-MM-DD.log` - 图像生成日志

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- 成语列表数据参考自"成语大全"（https://chengyu.5000yan.com/）
- 使用阿里云通义千问API进行文本和图像生成

