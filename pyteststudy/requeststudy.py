import requests

url='https://www.runoob.com/wp-content/themes/runoob/option/alisearch/v330/hot_hint.php'
query_data={
    "hint":"html教程",
    "pv":"342541",

}
my_header={
"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
}

r=requests.get(url,params=query_data,headers=my_header)
print(r.status_code)
print(r.request.headers)
print(r.json()[1]['hot'])
print(r.text)
assert 