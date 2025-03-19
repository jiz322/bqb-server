# bqb-server

> 一个用于检索表情包的服务器，基于 [zhaoolee/ChineseBQB](https://github.com/zhaoolee/ChineseBQB) 中的表情包数据，结合阿里巴巴 NLP 的 GME-Qwen2VL 系列多模态大模型进行文本与图像向量检索。

```bash
bqb-server/
├── bqb/                             # 表情包图片文件夹（来自 ChineseBQB）  
│── bqb-preview/                     # resized bqb
├── embedding_dicts/                 # GME模型给出的向量 与bqb中文件一一对应
│   └── 2b_embeddings_dict.pt        
│   └── 2b_fused_embeddings_dict.pt  
│   └── 7b_embeddings_dict.pt        
│   └── 7b_fused_embeddings_dict.pt  
├── config.yaml  
├── demo_api.ipynb                       
├── demo_preview.ipynb               # 用于演示
├── gme_inference.py    
├── main.py                                              
└── README.md
├── requirements.txt
```

## 安装与运行

0. **下载模型文件：**
无需显卡，32B以上DRAM用7b，不然用2b
[7b](https://huggingface.co/Alibaba-NLP/gme-Qwen2-VL-7B-InstructB)
[2b](https://huggingface.co/Alibaba-NLP/gme-Qwen2-VL-2B-Instruct)

1. **克隆项目代码：**
```bash
git clone https://github.com/yourusername/bqb-server.git
cd bqb-server
```

2. **创建并激活虚拟环境（可选）：**
```bash
# Windows PowerShell
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **安装依赖：**
```bash
pip install -r requirements.txt
```

4. **检查config.yaml配置后，启动服务端：**
```bash
python main.py
```

