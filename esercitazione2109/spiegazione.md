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

### seconda parte

1. client che compone i messaggi

```python
MSG = f"{nick_mittente}:{nick_dest}:{messaggio}"
```

2. server capisce dove inviare i messaggi

Inserisco il mittente nel client e il server attraverso il db capisce dove voglio inviare i messaggi

3. il server quando riceve "OK" entra in chat mod, bisogna inserire prima la lista di nick name "abilitati"
