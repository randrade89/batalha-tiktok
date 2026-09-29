with open(r"C:\Users\Rogerio\.gemini\antigravity\scratch\tiktok-live-batalha\public\overlay.html", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace("/images/camisa_vermelha.png", "/images/lula_cutout.png")
text = text.replace("/images/camisa_amarela.png", "/images/flavio_cutout.png")

with open(r"C:\Users\Rogerio\.gemini\antigravity\scratch\tiktok-live-batalha\public\overlay.html", "w", encoding="utf-8") as f:
    f.write(text)
print("Updated overlay.html with cutout caricatures!")