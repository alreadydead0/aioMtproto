"""
RSA encryption and official Telegram public keys for MTProto handshake.
"""

from __future__ import annotations

import hashlib
import os
from typing import NamedTuple


class RSAKey(NamedTuple):
    fingerprint: int
    n: int
    e: int


# Official Telegram Production and Test Server RSA Public Keys
TELEGRAM_RSA_KEYS: list[RSAKey] = [
    RSAKey(
        fingerprint=-4725062493392723383,  # 0xbe256d0f6e919849 -> signed int64
        n=int(
            "c3b42b026ce86bf15d4323502f32c36647cf776739e46e63e52a1207ae3a61d4a9"
            "07590b4904d2a48b71f974dd80464a30284d64196747dcb8b0f58f9e0115d3024c"
            "68747aec34c8525b7e2440e0aded8b3c7820b399997ce7ab7656f40032e8b23f"
            "0468e3e2454f5a436f5e6394f12287e459818d525f4b97bf3d702923b77a019be"
            "ad961c620e1743248b61a463b497714995c8e2ab7000f2934d5463f50c79744e6"
            "c9b40d2bed4fe72f69fc9b506164d47700cee4fb2206824a79a4f23e716f0c9c0"
            "c07ddda302a8d3f6f506ae4b44a5f884e864b5a073c682f32c3200a8f7a92d71d"
            "a2f2e0f20a4239ec34f22cf454d4423543e2b90837466644d",
            16,
        ),
        e=65537,
    ),
    RSAKey(
        fingerprint=-1156828557342674483,  # 0xef99824249a852cd
        n=int(
            "9a2632b19b61dd1239506452f44173871438b91037749301507f3e5b853a5298a0"
            "fb3474fc15268324ceb9517ab937fdf8614a8d6e3a95970cb72d4761016296c7b"
            "a24cf29a73884313d4957e0fc270e7cb238b812acee3e743566580d9293007e34"
            "02d4f5507c72f506b6e1265a20f59cbbd7b0691728e9c337db70fb59e048b7768"
            "3164dd3dbd0f46a97c52cfeb21b0b651587b73f2c89084fa169b2356e0004908a"
            "14627b4d160f1507764e46b5a16f40fb8766e408a29ed6d653822f0703f5e81c2"
            "b14e37da45a7063b57ddd4d14d65036f136471b505a04b154fc76fb8979da1e99"
            "e9e4d5ab7939b28292455a75897d8b6964b1bb5072e49123",
            16,
        ),
        e=65537,
    ),
    RSAKey(
        fingerprint=-3732688755609340798,  # 0xcc3b0638708c3c82
        n=int(
            "bb82457f7fb6ec142b3b4eec3910c5119f394a0f1aeb7250acab7b0f8d2a156dabb"
            "713f770a9b4da530f012421a2764b426d4bce20e00877d547b511999402e6b975e"
            "7406a4613a0b08a97cf2a1e04c85fe0101e400a4a4e6eb4984f43711fa783a129f"
            "219a863b71f50919282224f7da2f1201fa74224d51862223d61d5f21803f2972908"
            "a0d019b5a6530bc857ca742610f9d8ec75a9b99d3d404d0f3f5ce2e077501f1b37d"
            "eb69464d99141334e6d158d54c4dd44a0e8bda10e04c2e2fe63555a9ec2f599b567"
            "f3550fb73036306136ec947f637fc73d7429700e6940a60bb47b01808291e702513"
            "643d82473c3e3d40a38ec23096425a9164821",
            16,
        ),
        e=65537,
    ),
    RSAKey(
        fingerprint=-5055006677943018446,  # 0xb9dc074e6f494432
        n=int(
            "cbea526f101f3a47da2231bd71861296cd70fb32499e04b80ebecd163eec86adb28"
            "04eed79a4c3c45496ec50e5303d8272604b14d00e128bceee82b497e0fc2943415"
            "ac1eb64324d312838a2e457f5af16f96e288202203fb2a604ec2d0e835e5d3e4a7"
            "6f27712518a8d07e66d4ba701e6a2bd5a8e042b26beec11d67b410d4c82e0ad7971"
            "7491f0007d3417f1f03446494f8416e34a50f142c3e35028d3e9b151e73068154216"
            "3a83b59e7ec923c4d4d960f64142d31249942a8182b2bb9914f3fb16007e334c05"
            "2866eb30a6ce9da459be59970a02c3074d0a5f07be06bd0b296fb0fa95f2e5a8394"
            "f493a52e52221b6abb73f7348166ac130001b",
            16,
        ),
        e=65537,
    ),
    RSAKey(
        fingerprint=-4344800451088585951,
        n=int(
            "C150023E2F70DB7985DED064759CFECF0AF328E69A41DAF4D6F01B538135A6F9"
            "1F8F8B2A0EC9BA9720CE352EFCF6C5680FFC424BD634864902DE0B4BD6D49F4E"
            "580230E3AE97D95C8B19442B3C0A10D8F5633FECEDD6926A7F6DAB0DDB7D457F"
            "9EA81B8465FCD6FFFEED114011DF91C059CAEDAF97625F6C96ECC74725556934"
            "EF781D866B34F011FCE4D835A090196E9A5F0E4449AF7EB697DDB9076494CA5F"
            "81104A305B6DD27665722C46B60E5DF680FB16B210607EF217652E60236C255F"
            "6A28315F4083A96791D7214BF64C1DF4FD0DB1944FB26A2A57031B32EEE64AD1"
            "5A8BA68885CDE74A5BFC920F6ABF59BA5C75506373E7130F9042DA922179251F",
            16,
        ),
        e=65537,
    ),
    RSAKey(
        fingerprint=847625836280919973,
        n=int(
            "AEEC36C8FFC109CB099624685B97815415657BD76D8C9C3E398103D7AD16C9BB"
            "A6F525ED0412D7AE2C2DE2B44E77D72CBF4B7438709A4E646A05C43427C7F184"
            "DEBF72947519680E651500890C6832796DD11F772C25FF8F576755AFE055B0A3"
            "752C696EB7D8DA0D8BE1FAF38C9BDD97CE0A77D3916230C4032167100EDD0F9E"
            "7A3A9B602D04367B689536AF0D64B613CCBA7962939D3B57682BEB6DAE5B6081"
            "30B2E52ACA78BA023CF6CE806B1DC49C72CF928A7199D22E3D7AC84E47BC9427"
            "D0236945D10DBD15177BAB413FBF0EDFDA09F014C7A7DA088DDE9759702CA760"
            "AF2B8E4E97CC055C617BD74C3D97008635B98DC4D621B4891DA9FB0473047927",
            16,
        ),
        e=65537,
    ),
    RSAKey(
        fingerprint=1562291298945373506,
        n=int(
            "BDF2C77D81F6AFD47BD30F29AC76E55ADFE70E487E5E48297E5A9055C9C07D2B"
            "93B4ED3994D3ECA5098BF18D978D54F8B7C713EB10247607E69AF9EF44F38E28"
            "F8B439F257A11572945CC0406FE3F37BB92B79112DB69EEDF2DC71584A661638"
            "EA5BECB9E23585074B80D57D9F5710DD30D2DA940E0ADA2F1B878397DC1A72B5"
            "CE2531B6F7DD158E09C828D03450CA0FF8A174DEACEBCAA22DDE84EF66AD370F"
            "259D18AF806638012DA0CA4A70BAA83D9C158F3552BC9158E69BF332A45809E1"
            "C36905A5CAA12348DD57941A482131BE7B2355A5F4635374F3BD3DDF5FF925BF"
            "4809EE27C1E67D9120C5FE08A9DE458B1B4A3C5D0A428437F2BECA81F4E2D5FF",
            16,
        ),
        e=65537,
    ),
    RSAKey(
        fingerprint=-5859577972006586033,
        n=int(
            "B3F762B739BE98F343EB1921CF0148CFA27FF7AF02B6471213FED9DAA0098976"
            "E667750324F1ABCEA4C31E43B7D11F1579133F2B3D9FE27474E462058884E5E1"
            "B123BE9CBBC6A443B2925C08520E7325E6F1A6D50E117EB61EA49D2534C8BB4D"
            "2AE4153FABE832B9EDF4C5755FDD8B19940B81D1D96CF433D19E6A22968A85DC"
            "80F0312F596BD2530C1CFB28B5FE019AC9BC25CD9C2A5D8A0F3A1C0C79BCCA52"
            "4D315B5E21B5C26B46BABE3D75D06D1CD33329EC782A0F22891ED1DB42A1D6C0"
            "DEA431428BC4D7AABDCF3E0EB6FDA4E23EB7733E7727E9A1915580796C55188D"
            "2596D2665AD1182BA7ABF15AAA5A8B779EA996317A20AE044B820BFF35B6E8A1",
            16,
        ),
        e=65537,
    ),
]


def find_rsa_key(fingerprints: list[int]) -> RSAKey | None:
    """
    Find matching Telegram RSA key by given fingerprints list.
    """
    for fp in fingerprints:
        for key in TELEGRAM_RSA_KEYS:
            if key.fingerprint == fp:
                return key
    return None


def rsa_encrypt(data: bytes, key: RSAKey) -> bytes:
    """
    Encrypt data with Telegram RSA key using Telegram MTProto padding.

    Telegram MTProto RSA scheme (NOT standard PKCS#1 / OAEP):
        plaintext = SHA1(data) + data + random_padding  →  exactly 255 bytes
        ciphertext = pow(int_from_255_bytes, e, n)       →  256 bytes output

    The plaintext is 255 bytes (not 256) because Telegram pads to 255 so the
    resulting big integer is guaranteed to be smaller than the 2048-bit modulus.

    :param data: Data to encrypt (e.g. p_q_inner_data_dc serialised bytes).
    :param key: RSAKey instance with n and e.
    :return: 256-byte RSA ciphertext.
    """
    sha1_hash = hashlib.sha1(data).digest()  # 20 bytes
    data_with_hash = sha1_hash + data  # 20 + len(data) bytes
    # Pad to exactly 255 bytes so the integer is < n
    pad_len = 255 - len(data_with_hash)
    if pad_len < 0:
        msg = (
            f"Data too long for Telegram RSA: SHA1+data is {len(data_with_hash)} bytes "
            f"(max 255). Raw data length: {len(data)} bytes."
        )
        raise ValueError(msg)

    padded = data_with_hash + os.urandom(pad_len)  # exactly 255 bytes
    data_int = int.from_bytes(padded, "big")  # fits in < 2048 bits
    enc_int = pow(data_int, key.e, key.n)
    return enc_int.to_bytes(256, "big")  # 256-byte output
