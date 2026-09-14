from vigenere import *


# Ciphertext 1 - Odd group numbers
CIPHERTEXT_1 = """
DAZFI SFSPA VQLSN PXYSZ WXALC DAFGQ UISMT PHZGA
MKTTF TCCFX
KFCRG GLPFE TZMMM ZOZDE ADWVZ WMWKV GQSOH QSVHP
WFKLS LEASE
PWHMJ EGKPU RVSXJ XVBWV POSDE TEQTX OBZIK WCXLW
NUOVJ MJCLL
OEOFA ZENVM JILOW ZEKAZ EJAQD ILSWW ESGUG KTZGQ
ZVRMN WTQSE
OTKTK PBSTA MQVER MJEGL JQRTL GFJYG SPTZP GTACM
OECBX SESCI
YGUFP KVILL TWDKS ZODFW FWEAA PQTFS TQIRG MPMEL
RYELH QSVWB
AWMOS DELHM UZGPG YEKZU KWTAM ZJMLS EVJQT GLAWV
OVVXH KWQIL
IEUYS ZWXAH HUSZO GMUZQ CIMVZ UVWIF JJHPW VXFSE
TZEDF
"""


# Ciphertext 2 - Even group numbers
CIPHERTEXT_2 = """
QRBAI UWYOK ILBRZ XTUWL EGXSN VDXWR XMHXY FCGMW
WWSME LSXUZ
MKMFS BNZIF YEIEG RFZRX WKUFA XQEDX DTTHY NTBRJ
LHTAI KOCZX
QHBND ZIGZG PXARJ EDYSJ NUMKI FLBTN HWISW NVLFM
EGXAI AAWSL
FMHXR SGRIG HEQTU MLGLV BRSIL AEZSG XCMHT OWHFM
LWMRK HPRFB
ELWGF RUGPB HNBEM KBNVW HHUEA KILBN BMLHK XUGML
YQKHP RFBEL
EJYNV WSIJB GAXGO TPMXR TXFKI WUALB RGWIE GHWHG
AMEWW LTAEL
NUMRE UWTBL SDPRL YVRET LEEDF ROBEQ UXTHX ZYOZB
XLKAC KSOHN
VWXKS MAEPH IYQMM FSECH RFYPB BSQTX TPIWH GPXQD
FWTAI KNNBX

SIYKE TXTLV BTMQA LAGHG OTPMX RTXTH XSFYG WMVKH
LOIVU ALMLD
LTSYV WYNVW MQVXP XRVYA BLXDL XSMLW SUIOI IMELI
SOYEB HPHNR
WTVUI AKEYG WIETG WWBVM VDUMA EPAUA KXWHK MAUPA
MUKHQ PWKCX
EFXGW WSDDE OMLWL NKMWD FWTAM FAFEA MFZBN WIHYA
LXRWK MAMIK
GNGHJ UAZHM HGUAL YSULA ELYHJ BZMSI LAILH WWYIK
EWAHN PMLBN
NBVPJ XLBEF WRWGX KWIRH XWWGQ HRRXW IOMFY CZHZL
VXNVI OYZCM
YDDEY IPWXT MMSHS VHHXZ YEWNV OAOEL SMLSW KXXFX
STRVI HZLEF
JXDAS FIE
"""


def get_key_length(ciphertext, candidates):

    # If Kasiski gives no candidates,
    # try key lengths from 2 to 20.
    if len(candidates) == 0:
        candidates = list(range(2, 21))

    best_length = candidates[0]
    best_ic = 0

    for length in candidates:

        if length > 20:
            continue

        groups = split_into_groups(ciphertext, length)

        total_ic = 0

        for group in groups:
            total_ic += calculate_ic(group)

        average_ic = total_ic / length

        if average_ic > best_ic:
            best_ic = average_ic
            best_length = length

    return best_length


def print_frequency_table(groups):

    for i in range(len(groups)):

        frequency = frequency_analysis(groups[i])

        print("\nGroup", i + 1)
        print("Letter : Frequency")

        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            print(letter, ":", frequency[letter], end="   ")

            if (ord(letter) - ord('A') + 1) % 6 == 0:
                print()


def main():

    print("VIGENERE CIPHER CRYPTANALYSIS")
    print("-----------------------------")

    group_number = int(
        input("Enter your group number: ")
    )

    # Select ciphertext
    if group_number % 2 == 1:
        ciphertext = CIPHERTEXT_1
        print("\nOdd group number -> Ciphertext 1 selected")
    else:
        ciphertext = CIPHERTEXT_2
        print("\nEven group number -> Ciphertext 2 selected")

    # Step 1: Clean ciphertext
    ciphertext = clean_ciphertext(ciphertext)

    print("\nCiphertext length:", len(ciphertext))

    # Step 2: Kasiski test
    candidates = kasiski_analysis(ciphertext)

    print("\nKasiski candidate key lengths:")

    if len(candidates) == 0:
        print("No candidates found")
    else:
        print(candidates[:10])

    # Step 3: Estimate key length
    key_length = get_key_length(
        ciphertext,
        candidates
    )

    print("\nEstimated key length:", key_length)

    # Step 4: Split ciphertext
    groups = split_into_groups(
        ciphertext,
        key_length
    )

    # Step 5: Frequency analysis
    print("\nFREQUENCY TABLES")
    print("----------------")

    print_frequency_table(groups)

    # Step 6: Find key
    key = find_key(groups)

    print("\nRecovered key:", key)

    # Step 7: Decrypt
    plaintext = vigenere_decrypt(
        ciphertext,
        key
    )

    print("\nRECOVERED PLAINTEXT")
    print("-------------------")
    print(plaintext)

    # Step 8: Re-encrypt
    encrypted = vigenere_encrypt(
        plaintext,
        key
    )

    # Step 9: Verify
    result = verify(
        ciphertext,
        encrypted
    )

    print("\nVERIFICATION")
    print("------------")

    if result:
        print("Re-encryption matches original ciphertext.")
        print("Verification successful!")
    else:
        print("Verification failed.")


if __name__ == "__main__":
    main()
