import requests
cat = requests.get("https://api.chucknorris.io/jokes/categories").json()
if input("Categoria(c) o Parola(p)? --> ") == "c":
    print(f"Categorie: \n {cat}")
    resp = requests.get("https://api.chucknorris.io/jokes/random?category=" + input("Inserisci categoria: "))
    print(resp.json()["value"])
else:
    resp = requests.get("https://api.chucknorris.io/jokes/search?query=" + input("Inserisci parola: "))
    for i in resp.json()["result"]:
        print(i["value"])