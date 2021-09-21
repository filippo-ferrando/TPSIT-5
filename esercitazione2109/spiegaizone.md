# Chat più articolata

### prima parte

(per ora udp)

- Identificazione utente con identificativo univoco

- server genera una tabella con identificativo - IP
1. Il client (appena conosce il nick) manda l'HELLO (per salvare nick e ip)

2. Il server risponde con un messaggio di OK

```python
HELLO = f"nickname: {nick}"
OK = "OK"
```


