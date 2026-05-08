# contract-ai-negotiator
多Agent合同谈判系统
# 🤖 Contract Negotiation Multi-Agent System

一个基于多Agent架构的智能合同谈判模拟系统。通过让多个专业AI Agent协作（包括对方律师模拟Agent），实现合同风险分析、谈判策略推演和话术生成。

## ✨ 特性

- 🎭 **多角色Agent协作**: 解析Agent、防守方Agent、对手模拟Agent、仲裁Agent
- 🔄 **谈判博弈模拟**: Agent间多轮辩论，预测对方策略
- 🛡️ **熔断机制**: 防止Agent陷入死循环
- 📊 **置信度评估**: 量化分析结果可靠性
- 💾 **记忆系统**: 短期/长期/共享记忆，支持历史案例检索
- 🎯 **可操作建议**: 生成具体修改建议和谈判话术

## 🏗️ 架构
用户输入合同
↓
[解析Agent] → 提取条款
↓
[本方法务Agent] → 标注风险
↓
[辩论循环] ←→ [对手模拟Agent]
↓
[仲裁Agent] → 综合建议
↓
输出报告 (风险等级 + 谈判策略 + 话术)

text

## 🚀 快速开始

### 安装


# 克隆仓库
```
git clone https://github.com/yourusername/contract-negotiation-multi-agent.git
cd contract-negotiation-multi-agent
```
# 创建虚拟环境
```python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```
# 安装依赖
```pip install -e .
```

### 配置

# 复制环境变量模板
```
cp .env.example .env
```
# 编辑.env，填入你的OpenAI API密钥
# OPENAI_API_KEY=sk-your-key-here

### 运行
bash
# 使用示例合同
```
python src/main.py
```
# 或作为CLI工具
```
contract-agent --contract examples/sample_contracts/software_dev.txt
```
# Docker 运行
```
docker build -t contract-agent .
docker run -e OPENAI_API_KEY=your_key contract-agent
```

### 📖 使用示例
```
from src.orchestrator import MultiAgentOrchestrator
```
# 初始化系统
```
orchestrator = MultiAgentOrchestrator()
```
# 分析合同
```
contract = """
第5条 知识产权
原条款：项目知识产权归甲方。
修改为：双方共有。
"""

report = orchestrator.analyze_contract(contract)
```
# 输出:
# 风险等级: 高风险
# 建议策略: 坚持恢复原条款
# 建议话术: "考虑到本项目由我方全额出资..."
🎯 核心创新点
对抗性生成: 内建"对方律师模拟Agent"，实现双向博弈推演

熔断机制: 自动检测并中止无意义Agent辩论

人类仲裁接口: 低置信度决策自动升级给人类

结构化通信: Agent间使用JSON格式传递信息，防止信息污染

详见架构文档

🤝 贡献
欢迎贡献代码！请查看 CONTRIBUTING.md

🐛 报告Bug

💡 功能建议

🔧 Pull Request

⚠️ 免责声明
本系统仅作为辅助工具，不构成法律建议。重要合同决策请咨询专业律师。

📄 许可证
MIT License - 详见 LICENSE

🌟 致谢
OpenAI - GPT模型

ChromaDB - 向量数据库

Rich - 终端美化

如果这个项目对你有帮助，请给个⭐️ Star!
