
def leitura_arquivo ():
    with open ("darkweb2017-top100.txt", "r") as arquivo:
        for i in range (0,10):
            linha = arquivo.readline()
            print(f"senha : {linha}")

leitura_arquivo()
