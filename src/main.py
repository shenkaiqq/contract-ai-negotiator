from orchestrator import MultiAgentOrchestrator

def main():
    # 示例合同文本(简化版)
    sample_contract = """
    软件开发合同

    第5条 知识产权
    原条款：本项目产生的所有知识产权归甲方所有。
    对方修改：本项目产生的知识产权由双方共有。
    
    第8条 责任限制
    原条款：乙方赔偿责任上限为合同总金额的3倍。
    对方修改：乙方赔偿责任上限为合同总金额。
    
    第12条 付款条款
    原条款：验收合格后30日内付款。
    对方修改：验收合格后90日内付款。
    """
    
    # 初始化编排器
    orchestrator = MultiAgentOrchestrator()
    
    # 执行分析
    report = orchestrator.analyze_contract(sample_contract)
    
    # 输出摘要
    print("\n" + "="*50)
    print("✅ 分析完成！关键建议：")
    print(f"风险等级: {report['风险等级']}")
    print(f"建议策略: {report['谈判策略']}")
    print(f"建议话术: {report['建议话术']}")

if __name__ == "__main__":
    main()
