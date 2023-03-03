import requests 


for i in range(1000):
    r = requests.get('http://172.16.109.78:3000/api/get_package_json/j')
    r = requests.get('http://172.16.109.78:3000/api/get_package_json/j')
    r = requests.get('http://172.16.109.78:3000/api/get_package_json/j')
    print(r.status_code)