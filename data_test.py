"""

TD-Ameritrade API
Example of API Data Retrieval Using Custom-Built Class Wrapper

"""

from account import user, password, consumer_key, localhost, exec_path
from tdapi import tdapi

session = tdapi(user, password, consumer_key, localhost, exec_path)
request = session.option_chain(ticker = 'DIS', cp = 'CALL', fromDate = '2019-07-28', toDate = '2019-08-31')
data = session.option_unpack(request, cpflag = 1)

