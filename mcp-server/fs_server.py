from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import io
import base64
import matplotlib.pyplot as plt

from mcp.server.fastmcp import FastMCP

from utils.stocks_common_metrics import StocksCommonMetrics
from utils.news_report import News_Report
from utils.quant_analysis import QuantAnalysis
from utils.backtesting import pyBackTesting
from utils.tools import PythonREPL

stocks_common_metrics=StocksCommonMetrics()
news_report=News_Report()
quant_analysis=QuantAnalysis()
back_testing = pyBackTesting()
repl = PythonREPL()

# Initialize the MCP server
mcp = FastMCP()

# MCP Tool: 
@mcp.tool()
async def get_today_date(format: Optional[str]='YYYYMMDD') -> str:
    """
    Retrieve the current date.

    Args:
        format: The desired format of the date. Defaults to 'YYYYMMDD'. 
                - 'YYYYMMDD': Returns the date in 'YYYYMMDD' format.
                - Any other value: Returns the date in 'YYYY-MM-DD' format.

    Returns:
        The current date in the specified format.
    """

    # 获取当前日期时间
    today = datetime.today()
    
    if format == 'YYYYMMDD':
        # 转换为时间戳
        today_formatted = today.strftime("%Y%m%d")
    else:
        # 转换为日期时间字符串
        today_formatted = today.strftime("%Y-%m-%d")

    return today_formatted

# ----------------- 股票常用指标类。 ----------------- #
# MCP Tool: 
@mcp.tool()
async def get_stock_code(name: str)  -> List[Dict[str, Any]]:
    """
    Retrieve the stock codes of companies listed on China's A-share market.

    Args:
        name: Stock name.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, where each dictionary represents the stock name and stock code of a listed company. Each dictionary contains the following elements:
            | name          | str  | Stock name |
            | stock_code    | str  | Stock code |
    """

    return stocks_common_metrics.get_stock_code(name)


# 经营业务结构
@mcp.tool()
async def get_stock_business_structure(stock_code: str)  -> List[Dict[str, Any]]:
    """
    Retrieve the main business structure of Chinese A-share listed companies for analyzing the company's core business, products, services, and revenue distribution.

    Args:
        stock_code: Stock code, e.g., "000001".

    Returns:
        List[Dict[str, Any]]: Returns a list of dictionaries, where each dictionary represents the report content for a specific reporting period. Each dictionary contains the following elements:
            | reporting_period               | str  | Reporting period |
            | classification_direction       | str  | Classification direction |
            | classification                 | str  | Classification |
            | operating_revenue              | str  | Operating revenue (Note: Unit is in yuan) |
            | operating_revenue_yoy_growth   | str  | Year-on-year growth of operating revenue |
            | operating_revenue_pct_of_main  | str  | Percentage of operating revenue to main business revenue |
            | operating_cost                 | str  | Operating cost (Note: Unit is in yuan) |
            | operating_cost_yoy_growth      | str  | Year-on-year growth of operating cost |
            | operating_cost_pct_of_main     | str  | Percentage of operating cost to main business cost |
            | gross_profit_margin            | str  | Gross profit margin |
            | gross_profit_margin_yoy_growth | str  | Year-on-year growth of gross profit margin |
    """

    return stocks_common_metrics.get_stock_business_structure(stock_code)

# 历史价格数据
@mcp.tool()
async def get_historical_stockprice_data(stock_code: str ,
                                   start_date: str,
                                   end_date: str, 
                                   period: Optional[str] = 'daily', 
                                   adjust: Optional[str] = '') -> List[Dict[str, Any]]:
    """
    Retrieve historical price data of companies listed on China's A-share market.

    Args:
        stock_code: Stock code.
        start_date: The start date of the query, formatted as 'YYYYMMDD'.
        end_date: The end date of the query, formatted as 'YYYYMMDD'.
        period: Data frequency. Optional values: {'daily', 'weekly', 'monthly'}, representing daily, weekly, and monthly data respectively.
        adjust: Whether to adjust prices. Optional values: {'', 'qfq', 'hfq'}, representing no adjustment, forward adjustment, and backward adjustment respectively.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, where each dictionary represents the stock price for a specific period. Each dictionary contains the following elements:
            | date          | object  | Trading date              |
            | stock_code    | object  | Stock code (without market identifier) |
            | open          | float | Opening price             |
            | close         | float | Closing price             |
            | high          | float | Highest price             |
            | low           | float | Lowest price              |
            | volume        | int   | Trading volume (unit: lots)|
            | turnover      | float | Trading turnover (unit: yuan)|
            | amplitude     | float | Amplitude (unit: %)       |
            | change_rate   | float | Change rate (unit: %)     |
            | change_amount | float | Change amount (unit: yuan)|
            | turnover_rate | float | Turnover rate (unit: %)   |
    """

    return stocks_common_metrics.get_historical_stockprice_data(stock_code, start_date, end_date, period, adjust)

# 关键财报数据
@mcp.tool()
async def get_stock_financial_abstract(stock_code: str ,
                                 indicator: Optional[str] = '按报告期')  -> List[Dict[str, Any]]:
    """
    Retrieve the financial report summary data of companies listed on China's A-share market.

    Args:
        stock_code: Stock code.
        indicator: Type of indicator. Optional values: {'按报告期', '按年度', '按单季度'} (By reporting period, by year, or by single quarter).

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, where each dictionary represents a financial summary record.  Each dictionary contains the following elements:
            | reporting_period               | object   | Reporting period              |
            | net_profit                     | object   | Net profit                    |
            | net_profit_growth_rate         | object   | Net profit growth rate (YoY)  |
            | non_recurring_net_profit       | object   | Non-recurring net profit      |
            | non_recurring_net_profit_growth_rate | object | Non-recurring net profit growth rate (YoY) |
            | total_operating_revenue        | object   | Total operating revenue       |
            | total_operating_revenue_growth_rate | object | Total operating revenue growth rate (YoY) |
            | basic_earnings_per_share       | object   | Basic earnings per share      |
            | net_asset_per_share            | object   | Net assets per share          |
            | capital_reserve_fund_per_share | object   | Capital reserve fund per share|
            | undistributed_profit_per_share | object   | Undistributed profit per share|
            | operating_cash_flow_per_share  | object   | Operating cash flow per share |
            | net_profit_margin              | object   | Net profit margin             |
            | gross_profit_margin            | object   | Gross profit margin           |
            | return_on_equity_of_roe        | object   | Return on equity (ROE)        |
            | diluted_return_on_equity_of_roe| object   | Diluted return on equity (ROE)|
            | operating_cycle                | object   | Operating cycle               |
            | inventory_turnover_ratio       | object   | Inventory turnover ratio      |
            | days_inventory_outstanding     | object   | Days inventory outstanding    |
            | days_sales_outstanding         | object   | Days sales outstanding         |
            | current_ratio                  | object   | Current ratio                 |
            | quick_ratio                    | object   | Quick ratio                   |
            | conservative_quick_ratio       | object   | Conservative quick ratio      |
            | debt_to_equity_ratio           | object   | Debt to equity ratio          |
            | asset_to_liability_ratio       | object   | Asset to liability ratio      |
    """

    return stocks_common_metrics.get_stock_financial_abstract(stock_code, indicator)

# 融资融券明细数据。
@mcp.tool()
async def get_stock_margin_detail(stock_code: str, start_date: str, end_date: str, freq: str = "D") -> List[Dict[str, Any]]:
    """
    Retrieve the margin trading and short selling details of companies listed on China's A-share market.

    Args:
        stock_code: Stock code, e.g., "000001".
        start_date: Start date, formatted as YYYYMMDD.
        end_date: End date, formatted as YYYYMMDD.
        freq: Date interval type, default is "D" (daily). Optional values include:
                    - "D": Daily
                    - "W": Weekly
                    - "MS": First day of each month
                    - "ME": Last day of each month
                    - "Q": Quarterly
                    - "Y": Annually

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, where each dictionary represents a summary of margin trading and short selling for a trading day. Each dictionary contains the following elements:
            | trading_date           | str        | Trading date                       |
            | target_security_code   | str        | Target security code               |
            | target_security_name   | str        | Target security abbreviation       |
            | margin_balance         | int        | Margin balance (unit: yuan)        |
            | margin_buy_amount      | int        | Margin purchase amount (unit: yuan)|
            | margin_repayment       | int        | Margin repayment amount (unit: yuan)|
            | short_selling_balance  | int        | Short selling balance              |
            | short_selling_volume   | int        | Short selling volume               |
            | short_selling_repayment| int        | Short selling repayment volume     |
        """

    return stocks_common_metrics.get_stock_margin_detail(stock_code, start_date, end_date, freq)

# 分红送配详情数据
@mcp.tool()
async def get_stock_fhps_detail(stock_code: str) -> List[Dict[str, Any]]:
    """
    Retrieve the historical dividend and rights issue details of companies listed on China's A-share market.

    Args:
        stock_code: Stock code, e.g., "600000".

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, where each dictionary represents the details of a dividend or rights distribution.  Each dictionary contains the following elements:
            | reporting_period                     | Reporting period                        | object  |
            | earnings_disclosure_date             | Earnings disclosure date                | object  |
            | total_share_conversion_ratio         | Share conversion - Total conversion ratio | float |
            | bonus_share_ratio                    | Share conversion - Bonus share ratio     | float |
            | capitalization_ratio                 | Share conversion - Capitalization ratio  | float |
            | cash_dividend_payout_ratio           | Cash dividend - Payout ratio             | float |
            | cash_dividend_payout_ratio_description | Cash dividend - Payout ratio description | object  |
            | dividend_yield                       | Cash dividend - Dividend yield           | float |
            | earnings_per_share                   | Earnings per share                      | float |
            | net_asset_value_per_share            | Net asset value per share               | float |
            | surplus_reserve_fund_per_share       | Surplus reserve fund per share          | float |
            | undistributed_profit_per_share       | Undistributed profit per share          | float |
            | net_profit_growth_rate               | Net profit growth rate (YoY)            | float |
            | total_shares_outstanding             | Total shares outstanding                | int   |
            | preliminary_plan_announcement_date   | Preliminary plan announcement date      | object  |
            | record_date                          | Record date                             | object  |
            | ex_dividend_date                     | Ex-dividend and ex-rights date          | object  |
            | proposal_progress                    | Proposal progress                       | object  |
            | latest_announcement_date             | Latest announcement date                | object  |
    """

    return stocks_common_metrics.get_stock_fhps_detail(stock_code)

# ----------------- 新闻报告类。用于获取股票相关的新闻报道。 ----------------- #
@mcp.tool()
async def stock_news(stock_code: str, start_date: Optional[ str] = None, end_date: Optional[ str] = None) -> List[Dict[str, Any]]:
    """
    Fetch the latest news articles and information related to a specific stock within a specified date range.

    Args:
        stock_code: Stock code, e.g., "000001".
        start_date: The start date of the query, formatted as 'YYYY-MM-DD'. If not provided, it defaults to one week before the current date.
        end_date: The end date of the query, formatted as 'YYYY-MM-DD'. If not provided, it defaults to the current date.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, where each dictionary represents a news article record.
        Each dictionary contains the following elements:
            | keyword       | str  | Keywords |
            | title         | str  | News Title |
            | content       | str  | News Content |
            | publish_time  | str  | Publication Time (format: YYYY-MM-DD HH:MM:SS) |
            | source        | str  | Source of the Article |
            | url           | str  | URL Link to the News Article |
    """

    return news_report.stock_news(stock_code)

@mcp.tool()
def financial_news(start_date: Optional[ str] = None, end_date: Optional[ str] = None) -> List[Dict[str, Any]]:
    """
    Fetch the latest financial news and market trends.

    Args:
        start_date: The start date of the query, formatted as 'YYYY-MM-DD'. If not provided, it defaults to one week before the current date.
        end_date: The end date of the query, formatted as 'YYYY-MM-DD'. If not provided, it defaults to the current date.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, where each dictionary represents a news record.
        Each dictionary contains the following elements:
            | title         | str  | News Title |
            | content       | str  | News Content |
            | pub_time      | str  | Publication Time (format: YYYY-MM-DD HH:MM:SS) |
            | url           | str  | URL Link to the News Article |
    """

    return news_report.financial_news(start_date, end_date)

# ----------------- 量化分析 ----------------- #

@mcp.tool()
async def get_stock_rsi_ma(stock_code: str ,
                     start_date: str,
                     end_date: str,
                     period: Optional[str] = 'daily',
                     adjust: Optional[str] = '',
                     min_window: Optional[int] = 50,
                     max_window: Optional[int] = 200) -> List[Dict[str, Any]]:
    """
    Fetch the moving average and RSI data for a stock, along with their buy/sell signals, to analyse the stock's strength and weakness.

    Args:
        stock_code: Stock code, e.g., "000001".
        start_date: Start date of the historical data (format: YYYYMMDD).
        end_date: End date of the historical data (format: YYYYMMDD).
        period: Time period of the data, e.g., "daily" (default: 'daily').
        adjust: Adjustment method for historical prices (default: '').
        min_window: Minimum window size for moving average calculation (default: 50).
        max_window: Maximum window size for moving average calculation (default: 200).

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, where each dictionary represents a trading day's stock volatility information.
        Each dictionary contains the following elements:
            | date         | str  | Trading Date (format: YYYY-MM-DD) |
            | close        | float| Closing Price |
            | MIN_MA       | float| Moving Average with a window size of min_window |
            | MAX_MA       | float| Moving Average with a window size of max_window |
            | MA_SIGNAL    | str  | Moving Average Signal ("Bullish" or "Bearish") |
            | RSI_SIGNAL   | str  | Relative Strength Index Signal ("Overbought", "Oversold", or "Neutral") |
    """

    return quant_analysis.get_stock_rsi_ma(stock_code, start_date, end_date, period, adjust, min_window, max_window)

# ----------------- 回测 ----------------- #
@mcp.tool()
async def strategy_buy_with_stop_loss(stock_code: str, start_date: str, end_date: str, percent: float, stop_profit_pct:float)->str:
    """
    Perform backtesting on historical stock data using the specified trading strategy to evaluate its performance. 
    The strategy is as follows: if the stock is not currently held, buy the stock based on the specified holding percentage (percent) and set a profit-taking percentage (stop_profit_pct).

    Args:
        stock_code: Stock code, e.g., "601688".
        start_date: Start date of the historical data (format: YYYYMMDD).
        end_date: End date of the historical data (format: YYYYMMDD).
        percent (float): A dynamic parameter representing the percentage for certain actions (e.g., buying proportion).
        stop_profit_pct (float): A dynamic parameter representing the profit-taking percentage.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, where each dictionary represents a backtesting result record.
            Each dictionary contains the following elements:
                | trade_count              | int    | Total number of trades executed during the backtesting period. |
                | initial_market_value     | float  | Initial market value (investment capital) at the start of the backtesting. |
                | end_market_value         | float  | Final market value (including unrealized PnL) at the end of the period. |
                | total_pnl                | float  | Total profit and loss (PnL) over the entire backtesting period. |
                | unrealized_pnl           | float  | Unrealized profit and loss at the end of the backtesting period. |
                | total_return_pct         | float  | Total return percentage over the backtesting period. |
                | annual_return_pct        | float  | Annualized return percentage. If not applicable, it will be null. |
                | total_profit             | float  | Total profit amount from all winning trades. |
                | total_loss               | float  | Total loss amount from all losing trades. |
                | total_fees               | float  | Total fees incurred during the backtesting period. |
                | max_drawdown             | float  | Maximum drawdown amount (peak-to-trough decline). |
                | max_drawdown_pct         | float  | Maximum drawdown percentage relative to the initial market value. |
                | win_rate                 | float  | Win rate as a percentage (number of winning trades divided by total trades). |
                | loss_rate                | float  | Loss rate as a percentage (number of losing trades divided by total trades). |
                | winning_trades           | int    | Total number of winning trades. |
                | losing_trades            | int    | Total number of losing trades. |
                | avg_pnl                  | float  | Average profit and loss per trade. |
                | avg_return_pct           | float  | Average return percentage per trade. |
                | avg_trade_bars           | float  | Average number of bars (time periods) per trade. |
                | avg_profit               | float  | Average profit amount per winning trade. |
                | avg_profit_pct           | float  | Average profit percentage per winning trade. |
                | avg_winning_trade_bars   | float  | Average number of bars per winning trade. |
                | avg_loss                 | float  | Average loss amount per losing trade. |
                | avg_loss_pct             | float  | Average loss percentage per losing trade. |
                | avg_losing_trade_bars    | float  | Average number of bars per losing trade. |
                | largest_win              | float  | Largest single trade profit amount. |
                | largest_win_pct          | float  | Largest single trade profit percentage. |
                | largest_win_bars         | int    | Number of bars for the largest winning trade. |
                | largest_loss             | float  | Largest single trade loss amount. |
                | largest_loss_pct         | float  | Largest single trade loss percentage. |
                | largest_loss_bars        | int    | Number of bars for the largest losing trade. |
                | max_wins                 | int    | Maximum consecutive winning trades. |
                | max_losses               | int    | Maximum consecutive losing trades. |
                | sharpe                   | float  | Sharpe ratio, measuring risk-adjusted returns. |
                | sortino                  | float  | Sortino ratio, focusing on downside risk-adjusted returns. |
                | calmar                   | float  | Calmar ratio, measuring returns relative to maximum drawdown. If not applicable, it will be null. |
                | profit_factor            | float  | Profit factor, calculated as total profit divided by total loss. |
                | ulcer_index              | float  | Ulcer index, measuring the depth and duration of drawdowns. |
                | upi                      | float  | UPI (Ulcer Performance Index), combining returns and ulcer index. |
                | equity_r2                | float  | R-squared value of the equity curve, indicating goodness of fit. |
                | std_error                | float  | Standard error of the equity curve, measuring volatility. |
                | annual_std_error         | float  | Annualized standard error. If not applicable, it will be null. |
                | annual_volatility_pct    | float  | Annualized volatility percentage. If not applicable, it will be null. |

    Example Usage:
        back_testing.Btesting(
            stock_code="601688",
            start_date="20221001",
            end_date="20231001",
            percent= 10,         # Dynamic parameter: Buying proportion
            stop_profit_pct=35   # Dynamic parameter: Profit-taking percentage

        )
    """
    strategy_parm = {
        'strategy_name': "strategy_buy_with_stop_loss",
        'percent': percent,         # Dynamic parameter: Buying proportion
        'stop_profit_pct': stop_profit_pct  # Dynamic parameter: Profit-taking percentage
    }
    return back_testing.Btesting(
        stock_code=stock_code,
        start_date=start_date,
        end_date=end_date,
        strategy_parm=strategy_parm
    )

# ----------------- Python Tool----------------- #
@mcp.tool()
async def python_repl(code: str) -> str:
    """
    Execute Python code in a REPL (Read-Eval-Print Loop) environment.

    Args:
        code: The Python code to be executed.

    Returns:
        The output of the executed code or an error message if an exception occurs.
    """

    return repl.run(code)

@mcp.tool()
async def data_visualization(code: str) -> str:
    """
    Executes the provided Python code to generate a plot, saves the plot as a PNG image, 
    encodes it in Base64 format, and returns it as a data URL.

    This function is designed to execute user-provided Python code that generates a plot using libraries like Matplotlib. 
    The generated plot is saved as a PNG image, encoded into Base64 format, and returned as a data URL for easy embedding 
    in web pages or other applications.

    Args:
        code: The Python code to be executed. The code is expected to generate a plot using a plotting library such as Matplotlib.
            Ensure that the code does not contain any harmful or malicious operations, as it will be executed in the current environment.

    Returns:
        If successful, the function returns a Base64 encoded string representing the generated plot image in PNG format, 
        prefixed with "data:image/png;base64," for use as a data URL.
        If the provided code fails to execute or the image encoding process fails, an error message is returned instead.

    Example Usage:
        The following example demonstrates how to use this function to generate a simple line plot:

        ```python
        import matplotlib.pyplot as plt

        # Define the Python code to generate a plot
        code = '''
        import matplotlib.pyplot as plt
        plt.figure(figsize=(6, 4))
        plt.plot([1, 2, 3, 4], [10, 20, 25, 30], marker='o')
        plt.title("Sample Plot")
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        '''

        # Call the function
        result = data_visualization(code) #  a Base64-encoded data URL of the plot image

        ```

    Notes:
        - Ensure that the provided code generates a valid plot before calling this function.
        - The function uses `io.BytesIO` to handle binary image data, as plots are saved in binary format (PNG).
        - If the code execution fails (e.g., due to syntax errors or missing dependencies), an error message is returned.
        - Be cautious when executing untrusted code, as it may introduce security risks.

    Raises:
        Exception: Any exceptions raised during the execution of the provided code or the image encoding process are caught 
                   and returned as part of the error message.
    """

    return repl.data_visualization(code)

# Start the MCP server
if __name__ == "__main__":
    print(f"ASkare Stocks MCP Server starting...")
    mcp.run()
