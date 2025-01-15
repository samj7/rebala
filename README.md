# rebala
Python rebalancing tool

Purpose:
I was tired of using google sheets to rebalance a small stock portfolio, so I built a somewhat automated one in python, using a yahoo finance api to fetch pricing data for stocks if possible. I want it to be easy to operate and effective enough for my own personal uses.

Potential upgrades:
- saving stock data in encrypted form, with user login
- accounting for dividends issued between logins with saved user data
- user error correction, so if you misinput a value you won't need to restart

Known issues:
- Currency conversion, some stocks are listed in USD vs CAD
