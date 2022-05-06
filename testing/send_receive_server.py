import select
from socket import *




s = socket(AF_INET,SOCK_STREAM)
s.bind(("localhost",0))
print(s.getsockname()[1])