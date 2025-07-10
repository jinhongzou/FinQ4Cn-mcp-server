# FinQ4Cn MCP Server

### English| [简体中文](README_zh-CN.md) 

A dedicated MCP server tool designed for quantitative analysis, FinQ4Cn-mcp-server aims to provide large models with convenient, free, and open-source access to financial data. Built on the `akshare` library, the project focuses on China's A-share market, offering users comprehensive data support for stocks and related financial products. It is particularly well-suited for professionals engaged in quantitative analysis as well as users interested in China's domestic stock market, meeting their needs for data from China's financial markets. As an ideal choice tailored to domestic investors, FinQ4Cn-mcp-server allows users to effortlessly access multi-dimensional data, including but not limited to stock prices, financial indicators, and market volatility, empowering precise decision-making.

## Future Implementation

### Timeline
- Enrich stock metrics data and improve data categorization  
- Provide technical analysis capabilities  
- Support funds, futures, and more  
- Support backtesting modules

## Features

### Stocks Risk Alert
- Retrieve the volatility details of the specified stock code's listed company.

### Stocks Common Metrics
- Retrieve the main business composition of the listed company with the specified stock code  
- Obtain historical price data for the stock within the specified time period  
- Retrieve the financial summary data of the specified stock  
- Obtain the margin trading and short selling details of the specified stock within the specified time range  
- Retrieve the historical dividend and rights issue details of the specified stock

### News Report
- Fetch the latest financial news and market trends within a specified date range.
- Fetch the latest news articles and information related to a specific stock within a specified date range.

### Back Testing
- Perform backtesting on historical stock data using the specified trading strategy to evaluate its performance. 
    The strategy is as follows: if the stock is not currently held, buy the stock based on the specified holding percentage (percent) and set a profit-taking percentage (stop_profit_pct).

## Project Structure

```
mcp-server/
├── utils    
├── |──modules.py # 数据校验模块
├── |──stocks_common_metrics.py # 常用指标数据
├── |──stocks_risk_alert.py     # 股票风险提示信息
├──fs_server.py # mcp server启动文件
```

## Dependencies

### Required Dependencies
- FastMCP
- Pydantic
- akshare

To install dependencies:
```bash
pip install -r requirements.txt
```

It is recommended to install the backtesting package using the following method:
```bash
pip install lib-pybroker -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## Setup

1. Clone the repository:
```bash
git clone https://github.com/jinhongzou/FinQ4Cn-mcp-server.git
cd FinQ4Cn-mcp-server
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

For detailed MCP configuration instructions across `Cherry Studio`, visit:
[Cherry Studio MCP Configuration Guide](https://docs.cherry-ai.com/advanced-basic/mcp)

### Integration with `Cherry Studio`
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

![image](demo_png/SetupCherry.png)

### Integration with `MCP inspector`

For detailed MCP configuration instructions using `MCP inspector`, run the following command:
```bash
npx @modelcontextprotocol/inspector python ./mcp-server/fs_server.py
```
If the log messages are displayed, it means the service has started successfully. Open the address `http://127.0.0.1:6274` in your browser to begin debugging MCP.
```text
Starting MCP inspector...
🔍 MCP Inspector is up and running at http://127.0.0.1:6274 🚀
⚙️ Proxy server listening on port 6277
```
![image](demo_png/MCPinspector.png)
For detailed instructions on how to configure and use this toolkit for in-depth stock data analysis, please refer to the documentation or example code.

## Available Tools

### stocks_common_metrics
- `get_stock_code`: Obtain the stock codes of companies by a stock names.
- `get_stock_zygc_em`: Retrieve the main business structure of companies listed, used to analyze the company's core business, products, services, and revenue distribution.
- `get_stock_financial_abstract`: Obtain the financial report summary data of companies listed.
- `get_stock_margin_detail`: Obtain the margin trading and short selling details of companies listed .
- `get_stock_fhps_detail`: Obtain the historical dividend and rights issue details of companies listed .

![image](demo_png/工具-分析综合股票财报.png)


### news report
- `financial_news`:Fetch the latest financial news and market trends within a specified date range.
- `stock_news`:Fetch the latest news articles and information related to a specific stock within a specified date range.

![image](demo_png/工具-个股新闻.png)

### BackTesting
- `strategy_buy_with_stop_loss`: Perform backtesting on historical stock data using the specified trading strategy to evaluate its performance. The strategy is as follows: if the stock is not currently held, buy the stock based on the specified holding percentage (percent) and set a profit-taking percentage (stop_profit_pct).

![image](demo_png/BreaktestAnswer.gif)



### Example usage:

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

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with `FastMCP`
- Built with `akshare` for comprehensive financial data access
- Uses `Pydantic` for data validation
