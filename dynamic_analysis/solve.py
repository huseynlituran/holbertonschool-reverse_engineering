from z3 import *

solver = Solver()

# Holberton{ + 24 simvol + }
prefix = b"Holberton{"
suffix = b"}"

# 24 simvolluq daxili hissə (ASCII printable)
mid = [BitVec(f'm_{i}', 32) for i in range(24)]
for c in mid:
    solver.add(c >= 0x20, c <= 0x7e)

# Assembly dövr parametrləri (Dövr başlanğıcı: 0x12a3 - 0x12bf)
var_4c = BitVecVal(0, 32)
var_48 = BitVecVal(1, 32)
var_44 = BitVecVal(0, 32)
var_40 = BitVecVal(1, 32)

for i in range(24):
    c = mid[i]
    
    # 1) var_4c güncəllənməsi
    # (i + 1) * c * (i + 2)
    val1 = (i + 1) * c * (i + 2)
    # cdq; shr edx, 0x18; add eax, edx; movzx eax, al; sub eax, edx
    # Bu əməliyyat x86 assembly-də sign extension və modulo 256 təsirini emulyasiya edir
    val1_b = (val1 & 0xff)
    var_4c = var_4c + val1_b

    # 2) var_48 güncəllənməsi
    # edx = i; eax = (edx << 3) - edx => 7 * i
    # eax = c + 7 * i; edx = eax + 0x1f
    edx = c + 7 * i + 0x1f
    # imul 0x214d0215 / division emulyasiyası (edx % 123)
    mod_val = edx % 123
    var_48 = var_48 * mod_val

    # 3) var_44 güncəllənməsi
    # (i + 1) * c + i*i
    val3 = (i + 1) * c + i * i
    var_44 = var_44 + (val3 & 0x1ff)

    # 4) var_40 güncəllənməsi
    # (i + 3) * c + 0x11
    val4 = (i + 3) * c + 0x11
    var_40 = var_40 ^ (val4 & 0x3ff)

# Dövr sonu hesablamalar (0x1399 - 0x13b4)
term1 = var_4c * var_48
var_38 = ((term1 + var_44 - var_40) ^ 0xdeadbeef) & 0xffffff

# Yekun yoxlama tənliyi (0x13b7 - 0x13f9)
edx_final = (term1 + var_38) - (var_44 * var_40)
eax_diff = edx_final - 0x35014542

rcx_val = LShR(eax_diff, 1)
# 0x87e53f15 sabit multipilakasiyası 987654 (0xf1206) ilə modulo/division əməliyyatıdır
eax_mod = eax_diff % 987654

# Yekun nəticə 0xae44-ə bərabər olmalıdır
solver.add(eax_mod == 0xae44)

print("[*] Z3 SMT Solver işə salındı... Şərtlər həll edilir...")

if solver.check() == sat:
    m = solver.model()
    flag_mid = "".join([chr(m[mid[i]].as_long()) for i in range(24)])
    full_flag = prefix.decode() + flag_mid + suffix.decode()
    
    print(f"\n[+] TAPILDI! Flag: {full_flag}")
    
    with open("0-flag.txt", "w") as f:
        f.write(full_flag + "\n")
    print("[+] Flag '0-flag.txt' faylına yazıldı.")
else:
    print("[-] UNSAT: Şərtlərə uyğun cavab tapılmadı. Tənliklər dəqiqləşdirilməlidir.")
