import secrets
import string

def generate_key(length=16):
    """Gera uma chave segura no formato XXXX-XXXX-XXXX-XXXX"""
    alphabet = string.ascii_uppercase + string.digits
    raw_key = ''.join(secrets.choice(alphabet) for _ in range(length))
    
    # Formata em blocos de 4
    formatted_key = '-'.join(raw_key[i:i+4] for i in range(0, length, 4))
    return formatted_key

if __name__ == "__main__":
    print("=== Gerador de Chaves de Acesso ===")
    qtd = input("Quantas chaves deseja gerar? (Enter para 1): ")
    qtd = int(qtd) if qtd.isdigit() else 1
    
    new_keys = []
    print("\nChaves Geradas:")
    for _ in range(qtd):
        key = generate_key()
        print(f"🔑 {key}")
        new_keys.append(key)
        
    save = input("\nDeseja salvar essas chaves no arquivo 'access_keys.txt'? (S/N): ").upper()
    if save == 'S':
        with open("access_keys.txt", "a") as f:
            for k in new_keys:
                f.write(f"{k}\n")
        print("✅ Chaves salvas com sucesso!")
    
    input("\nPressione Enter para sair...")
