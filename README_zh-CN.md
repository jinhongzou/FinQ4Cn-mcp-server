# FinQ4Cn MCP 服务器

### 简体中文 | [English](README.md)

FinQ4Cn-mcp-server 是一款专为量化分析设计的专用MCP服务器工具，旨在为大型模型提供便捷、免费且开源的金融数据访问。该项目基于 `akshare` 库构建，专注于中国A股市场，为用户提供全面的股票及相关金融产品数据支持。它特别适合从事量化分析的专业人士以及对中国国内股票市场感兴趣的用户，能够满足他们对于中国金融市场数据的需求。作为专为国内投资者定制的理想选择，FinQ4Cn-mcp-server 允许用户轻松获取多维数据，包括但不限于股票价格、财务指标和市场波动性，从而助力精准决策。

## 未来实现功能

### 时间线
- 丰富股票指标数据并完善数据分类  
- 提供技术分析能力  
- 支持基金、期货等更多品种  
- 支持回测模块

## 功能特性

### 股票风险提示
- 获取指定股票代码上市公司的波动详情  

### 股票常用指标
- 获取指定股票代码上市公司的主营业务构成  
- 获取指定时间段内股票的历史价格数据  
- 获取指定股票的财务概要数据  
- 获取指定时间段内指定股票的融资融券明细  
- 获取指定股票的历史分红与配股详情  

### 新闻资讯
- 获取指定日期范围内的最新财经新闻及市场趋势  
- 获取指定日期范围内与特定股票相关的最新新闻文章及信息  

### 回测功能
- 使用指定交易策略对历史股票数据进行回测以评估其表现。该策略如下：如果当前未持有该股票，则根据指定持仓比例（percent）买入股票，并设置止盈百分比（stop_profit_pct）。

## 项目结构

```
mcp-server/
├── utils    
├── |──modules.py # 数据校验模块
├── |──stocks_common_metrics.py # 常用指标数据
├── |──stocks_risk_alert.py     # 股票风险提示信息
├──fs_server.py # mcp server启动文件
```

## 依赖项

### 必需依赖
- FastMCP
- Pydantic
- akshare

安装依赖方法：
```bash
pip install -r requirements.txt
```

建议使用以下方式安装回测包：
```bash
pip install lib-pybroker -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/jinhongzou/FinQ4Cn-mcp-server.git
cd FinQ4Cn-mcp-server
```

2. 创建并激活虚拟环境：
```bash
python -m venv venv
source venv/bin/activate
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

如需跨 `Cherry Studio` 的详细MCP配置说明，请访问：
[Cherry Studio MCP 配置指南](https://docs.cherry-ai.com/advanced-basic/mcp)

### 与 `Cherry Studio` 集成
```json
{
  "mcpServers": {
    "FinQ4Cn-mcp-server": {
      "name": "FinQ4Cn",
      "command": "your_path/python.exe",
      "args": [
        "your_path/FinQ4Cn-mcp-server/mcp-server/fs_server.py"
      ]
    }
  }
}
```

![图片](demo_png/SetupCherry.png)

### 与 `MCP inspector` 集成

如需使用 `MCP inspector` 进行详细的MCP配置说明，请运行以下命令：
```bash
npx @modelcontextprotocol/inspector python ./mcp-server/fs_server.py
```
如果显示日志信息，表示服务已成功启动。在浏览器中打开地址 `http://127.0.0.1:6274` 即可开始调试MCP。
```text
Starting MCP inspector...
🔍 MCP Inspector is up and running at http://127.0.0.1:6274 🚀
⚙️ Proxy server listening on port 6277
```
![图片](demo_png/MCPinspector.png)
有关如何配置和使用此工具包进行深入股票数据分析的详细说明，请参考文档或示例代码。

## 可用工具

### stocks_common_metrics
- `get_stock_code`: 通过股票名称获取对应的股票代码。
- `get_stock_zygc_em`: 获取上市公司主营业务结构，用于分析公司核心业务、产品、服务和收入分布。
- `get_stock_financial_abstract`: 获取上市公司财务报告摘要数据。
- `get_stock_margin_detail`: 获取上市公司融资融券明细。
- `get_stock_fhps_detail`: 获取上市公司历史分红和配股详情。

![图片](demo_png/工具-分析综合股票财报.png)


### 新闻资讯
- `financial_news`: 获取指定日期范围内的最新财经新闻和市场趋势。
- `stock_news`: 获取指定日期范围内与特定股票相关的最新新闻文章和信息。

![图片](demo_png/工具-个股新闻.png)

### 回测功能
- `strategy_buy_with_stop_loss`: 使用指定交易策略对历史股票数据进行回测以评估其表现。该策略如下：如果当前未持有该股票，则根据指定持仓比例（percent）买入股票，并设置止盈百分比（stop_profit_pct）。

![图片](demo_png/BreaktestAnswer.gif)



### 示例用法：

```python
if __name__ == "__main__":

    # 创建 StocksCommonMetrics 实例
    stockutils = StocksCommonMetrics()
    # 获取股票名称及股票代码
    stock_codes = stockutils.get_stock_code(name="华泰证券")

    if stock_codes:
        stock_code = []
        for item in stock_codes:

            # 获取股票代码
            stock_code= item['stock_code']
            print(f"处理股票代码：{stock_code}")

            # 获取股价历史数据
            historical_stockprice_data = stockutils.get_historical_stockprice_data(stock_code=stock_code, start_date="20230101", end_date="20231001")
            print(historical_stockprice_data)
            
            # 获取财务概要数据
            stock_financial_abstract = stockutils.get_stock_financial_abstract(stock_code=stock_code, indicator='按报告期')
            print(stock_financial_abstract)

            # 获取融资融券明细数据
            stock_margin_detail = stockutils.get_stock_margin_detail(stock_code=stock_code, start_date="20230102", end_date="20230110")
            print(stock_margin_detail)
```

## 许可协议

本项目采用 MIT 许可协议 —— 请参阅 LICENSE 文件以获取详细信息。

## 致谢

- 使用 `FastMCP` 构建  
- 使用 `akshare` 获取全面的金融数据  
- 使用 `Pydantic` 进行数据验证
