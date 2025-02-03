def est_valide_ipv4(adresse):
  # Ici on découpe l'addresse en parties par le point
  parties = adresse.split(".")

  # On verifie que l'adresse contient 4 parties
  if len(parties) != 4:
    return False
  
  # On verifie que chaque partie est un nombre entre 0 et 255
  for partie in parties:
    try:
      nombre = int(partie)
      if nombre < 0 or nombre > 255:
        return False
    except:
      return False
  
  return True

def est_valide_ipv6(adresse):
    parties = adresse.split(":")
    
    # Vérifie que l'adresse contient 8 parties
    if len(parties) != 8:
        return False
    
    for partie in parties:
        # Vérifie que chaque partie a entre 1 et 4 caractères
        if len(partie) == 0 or len(partie) > 4:
            return False
            
        # Vérifie que chaque caractère est un chiffre hexa valide
        for caractere in partie:
            if caractere not in "0123456789abcdefABCDEF":
                return False
                
    return True

def detecter_version_ip(adresse):
    # Si c'est un dictionnaire, on traite chaque paire host/IP
    if isinstance(adresse, dict):
        resultats = {}
        for host, addr in adresse.items():
            if est_valide_ipv4(addr):
                resultats[host] = (addr, 4)
            elif est_valide_ipv6(addr):
                resultats[host] = (addr, 6)
            else:
                resultats[host] = (addr, None)
        return resultats
    
    # Si c'est une liste, on traite chaque adresse
    if isinstance(adresse, list):
        resultats = []
        for addr in adresse:
            if est_valide_ipv4(addr):
                resultats.append((addr, 4))
            elif est_valide_ipv6(addr):
                resultats.append((addr, 6))
        return resultats
    
    # Si c'est une seule adresse
    if est_valide_ipv4(adresse):
        return 4
    elif est_valide_ipv6(adresse):
        return 6
    return None