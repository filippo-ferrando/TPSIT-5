import requests

url = "http://localhost:5000/api/v1/resources/books/all"
http = requests.get(url)
print(http.content)