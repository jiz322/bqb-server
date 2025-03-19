# bqb-server

> 一个用于检索表情包的服务器，基于 [zhaoolee/ChineseBQB](https://github.com/zhaoolee/ChineseBQB) 中的表情包数据，结合阿里巴巴 NLP 的 GME-Qwen2VL 系列多模态大模型（Qwen2-VL）进行文本与图像向量检索。

```bash
bqb-server/
├── data/
│   └── bqb-images/               # 表情包图片文件夹（来自 ChineseBQB）
├── embeddings/
│   └── bqb_embeddings.json       # 存储向量的文件或数据库
├── main.py                       # FastAPI 主入口
├── models/
│   └── qwen2_vl/                 # 下载或缓存的 Qwen2-VL 模型文件
├── prepare_embeddings.py         # 向量化脚本
├── requirements.txt
└── README.md
```

## 安装与运行

1. **创建并激活虚拟环境（可选）：**
```bash
# Windows PowerShell
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

2. **安装依赖：**
```bash
pip install -r requirements.txt
```

2. **启动服务端：**
```bash
python main.py
```

