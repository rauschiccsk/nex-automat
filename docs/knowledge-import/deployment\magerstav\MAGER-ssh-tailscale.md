# MAGER Server - SSH a Tailscale konfigurácia

## Prehľad

MAGER server (Windows 11) je nakonfigurovaný pre vzdialený SSH prístup cez Tailscale VPN.

## Prístupové údaje

| Parameter | Hodnota |
|-----------|---------|
| Tailscale IP | 100.67.77.58 |
| Tailscale názov | server |
| SSH port | 22 |
| SSH user | Magerstav |
| SSH alias | `ssh mager` |

## Konfigurácia na Dev PC

### SSH Config (~/.ssh/config)

```
Host mager
    HostName 100.67.77.58
    User Magerstav
```

### Použitie

```bash
# Pripojenie
ssh mager

# Kopírovanie súborov
scp file.txt mager:

# Synchronizácia
rsync -avz ./dir mager:path/
```

## Konfigurácia na MAGER serveri

### OpenSSH Server

- Služba: `sshd` (Automatic, Running)
- Port: 22
- Firewall pravidlo: "SSH via Tailscale" (100.64.0.0/10)

### Authorized Keys

Pre admin účty Windows OpenSSH používa:
```
C:\ProgramData\ssh\administrators_authorized_keys
```

Nie štandardný `~/.ssh/authorized_keys` (ignorovaný pre Administrators skupinu).

### Permissions pre authorized_keys

```powershell
icacls "C:\ProgramData\ssh\administrators_authorized_keys" /inheritance:r /grant:r "SYSTEM:F" /grant:r "Administrators:F"
```

## Tailscale

- Verzia: 1.94.1
- Účet: iccforai@gmail.com
- Služba: Tailscale (Automatic, Running)

## CC Fleet - SSH prístupy

| Inštancia | Tailscale IP | SSH alias | Stav |
|-----------|--------------|-----------|------|
| DEVELOPMENT | 100.67.176.24 | lokálny | ✅ |
| ANDROS Ubuntu | 100.107.134.104 | `ssh andros` | ❌ (chýba kľúč) |
| MAGER | 100.67.77.58 | `ssh mager` | ✅ |

## Troubleshooting

### SSH Permission denied

1. Over či kľúč je v `administrators_authorized_keys` (nie user authorized_keys)
2. Skontroluj permissions na súbore
3. Reštartuj sshd: `Restart-Service sshd`

### Tailscale ping timeout

1. Over či Tailscale služba beží na oboch stranách
2. Pridaj firewall pravidlo pre Tailscale subnet (100.64.0.0/10)

## Dátum konfigurácie

2026-01-29