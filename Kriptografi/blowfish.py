import base64
import html
import pandas as pd
from textwrap import dedent

# BLOWFISH CONSTANTS
_PI_HEX = """243f6a8885a308d313198a2e03707344a4093822299f31d0082efa98ec4e6c89452821e638d01377be5466cf34e90c6cc0ac29b7c97c50dd3f84d5b5b54709179216d5d98979fb1bd1310ba698dfb5ac2ffd72dbd01adfb7b8e1afed6a267e96ba7c9045f12c7f9924a19947b3916cf70801f2e2858efc16636920d871574e69a458fea3f4933d7e0d95748f728eb658718bcd5882154aee7b54a41dc25a59b59c30d5392af26013c5d1b023286085f0ca417918b8db38ef8e79dcb0603a180e6c9e0e8bb01e8a3ed71577c1bd314b2778af2fda55605c60e65525f3aa55ab945748986263e8144055ca396a2aab10b6b4cc5c341141e8cea15486af7c72e993b3ee1411636fbc2a2ba9c55d741831f6ce5c3e169b87931eafd6ba336c24cf5c7a325381289586773b8f48986b4bb9afc4bfe81b6628219361d809ccfb21a991487cac605dec8032ef845d5de98575b1dc262302eb651b8823893e81d396acc50f6d6ff383f442392e0b4482a484200469c8f04a9e1f9b5e21c66842f6e96c9a670c9c61abd388f06a51a0d2d8542f68960fa728ab5133a36eef0b6c137a3be4ba3bf0507efb2a98a1f1651d39af017666ca593e82430e888cee8619456f9fb47d84a5c33b8b5ebee06f75d885c12073401a449f56c16aa64ed3aa62363f77061bfedf72429b023d37d0d724d00a1248db0fead349f1c09b075372c980991b7b25d479d8f6e8def7e3fe501ab6794c3b976ce0bd04c006bac1a94fb6409f60c45e5c9ec2196a246368fb6faf3e6c53b51339b2eb3b52ec6f6dfc511f9b30952ccc814544af5ebd09bee3d004de334afd660f2807192e4bb3c0cba85745c8740fd20b5f39b9d3fbdb5579c0bd1a60320ad6a100c6402c7279679f25fefb1fa3cc8ea5e9f8db3222f83c7516dffd616b152f501ec8ad0552ab323db5fafd23876053317b483e00df829e5c57bbca6f8ca01a87562edf1769dbd542a8f6287effc3ac6732c68c4f5573695b27b0bbca58c8e1ffa35db8f011a010fa3d98fd2183b84afcb56c2dd1d35b9a53e479b6f84565d28e49bc4bfb9790e1ddf2daa4cb7e3362fb1341cee4c6e8ef20cada36774c01d07e9efe2bf11fb495dbda4dae909198eaad8e716b93d5a0d08ed1d0afc725e08e3c5b2f8e7594b78ff6e2fbf2122b648888b812900df01c4fad5ea0688fc31cd1cff191b3a8c1ad2f2f2218be0e1777ea752dfe8b021fa1e5a0cc0fb56f74e818acf3d6ce89e299b4a84fe0fd13e0b77cc43b81d2ada8d9165fa2668095770593cc7314211a1477e6ad206577b5fa86c75442f5fb9d35cfebcdaf0c7b3e89a0d6411bd3ae1e7e4900250e2d2071b35e226800bb57b8e0af2464369bf009b91e5563911d59dfa6aa78c14389d95a537f207d5ba202e5b9c5832603766295cfa911c819684e734a41b3472dca7b14a94a1b5100529a532915d60f573fbc9bc6e42b60a47681e6740008ba6fb5571be91ff296ec6b2a0dd915b6636521e7b9f9b6ff34052ec585566453b02d5da99f8fa108ba47996e85076a4b7a70e9b5b32944db75092ec4192623ad6ea6b049a7df7d9cee60b88fedb266ecaa8c71699a17ff5664526cc2b19ee1193602a575094c29a0591340e4183a3e3f54989a5b429d656b8fe4d699f73fd6a1d29c07efe830f54d2d38e6f0255dc14cdd20868470eb266382e9c6021ecc5e09686b3f3ebaefc93c9718146b6a70a1687f358452a0e286b79c5305aa5007373e07841c7fdeae5c8e7d44ec5716f2b8b03ada37f0500c0df01c1f040200b3ffae0cf51a3cb574b225837a58dc0921bdd19113f97ca92ff69432477322f547013ae5e58137c2dadcc8b576349af3dda7a94461460fd0030eecc8c73ea4751e41e238cd993bea0e2f3280bba1183eb3314e548b384f6db9086f420d03f60a04bf2cb8129024977c795679b072bcaf89afde9a771fd9930810b38bae12dccf3f2e5512721f2e6b7124501adde69f84cd877a5847187408da17bc9f9abce94b7d8cec7aec3adb851dfa63094366c464c3d2ef1c18473215d908dd433b3724c2ba1612a14d432a65c45150940002133ae4dd71dff89e10314e5581ac77d65f11199b043556f1d7a3c76b3c11183b5924a509f28fe6ed97f1fbfa9ebabf2c1e153c6e86e34570eae96fb1860e5e0a5a3e2ab3771fe71c4e3d06fa2965dcb999e71d0f803e89d65266c8252e4cc9789c10b36ac6150eba94e2ea78a5fc3c531e0a2df4f2f74ea7361d2b3d1939260f19c279605223a708f71312b6ebadfe6eeac31f66e3bc4595a67bc883b17f37d1018cff28c332ddefbe6c5aa56558218568ab9802eecea50fdb2f953b2aef7dad5b6e2f841521b62829076170ecdd4775619f151013cca830eb61bd960334fe1eaa0363cfb5735c904c70a239d59e9e0bcbaade14eecc86bc60622ca79cab5cabb2f3846e648b1eaf19bdf0caa02369b9655abb5040685a323c2ab4b3319ee9d5c021b8f79b540b19875fa09995f7997e623d7da8f837889a97e32d7711ed935f166812810e358829c7e61fd696dedfa17858ba9957f584a51b2272639b83c3ff1ac24696cdb30aeb532e30548fd948e46dbc312858ebf2ef34c6ffeafe28ed61ee7c3c735d4a14d9e864b7e342105d14203e13e045eee2b6a3aaabeadb6c4f15facb4fd0c742f442ef6abbb5654f3b1d41cd2105d81e799e86854dc7e44b476a3d816250cf62a1f25b8d2646fc8883a0c1c7b6a37f1524c369cb749247848a0b5692b285095bbf00ad19489d1462b17423820e0058428d2a0c55f5ea1dadf43e233f70613372f0928d937e41d65fecf16c223bdb7cde3759cbee74604085f2a7ce77326ea607808419f8509ee8efd85561d99735a969a7aac50c06c25a04abfc800bcadc9e447a2ec3453484fdd567050e1e9ec9db73dbd3105588cd675fda79e3674340c5c43465713e38d83d28f89ef16dff20153e21e78fb03d4ae6e39f2bdb83adf7e93d5a68948140f7f64c261c94692934411520f77602d4f7bcf46b2ed4a20068d40824713320f46a43b7d4b7500061af1e39f62e9724454614214f74bf8b88404d95fc1d96b591af70f4ddd366a02f45bfbc09ec03bd97857fac6dd031cb850496eb27b355fd3941da2547e6abca0a9a28507825530429f40a2c86dae9b66dfb68dc1462d7486900680ec0a427a18dee4f3ffea2e887ad8cb58ce0067af4d6b6aace1e7cd3375fecce78a399406b2a4220fe9e35d9f385b9ee39d7ab3b124e8b1dc9faf74b6d185626a36631eae397b23a6efa74dd5b43326841e7f7ca7820fbfb0af54ed8feb397454056acba48952755533a3a20838d87fe6ba9b7d096954b55a867bca1159a58cca9296399e1db33a62a4a563f3125f95ef47e1c9029317cfdf8e80204272f7080bb155c05282ce395c11548e4c66d2248c1133fc70f86dc07f9c9ee41041f0f404779a45d886e17325f51ebd59bc0d1f2bcc18f41113564257b7834602a9c60dff8e8a31f636c1b0e12b4c202e1329eaf664fd1cad181156b2395e0333e92e13b240b62eebeb92285b2a20ee6ba0d99de720c8c2da2f728d012784595b794fd647d0862e7ccf5f05449a36f877d48fac39dfd27f33e8d1e0a476341992eff743a6f6eabf4f8fd37a812dc60a1ebddf8991be14cdb6e6b0dc67b55106d672c372765d43bdcd0e804f1290dc7cc00ffa3b5390f92690fed0b667b9ffbcedb7d9ca091cf0bd9155ea3bb132f88515bad247b9479bf763bd6eb37392eb3cc1159798026e297f42e312d6842ada7c66a2b3b12754ccc782ef11c6a124237b79251e706a1bbe64bfb63501a6b101811caedfa3d25bdd8e2e1c3c9444216590a121386d90cec6ed5abea2a64af674eda86a85fbebfe98864e4c3fe9dbc8057f0f7c08660787bf86003604dd1fd8346f6381fb07745ae04d736fccc83426b33f01eab71b08041873c005e5f77a057bebde8ae2455464299bf582e614e58f48ff2ddfda2f474ef388789bdc25366f9c3c8b38e74b475f25546fcd9b97aeb26618b1ddf84846a0e79915f95e2466e598e20b457708cd55591c902de4cb90bace1bb8205d011a862487574a99eb77f19b6e0a9dc09662d09a1c4324633e85a1f0209f0be8c4a99a0251d6efe101ab93d1d0ba5a4dfa186f20f2868f169dcb7da83573906fea1e2ce9b4fcd7f5250115e01a70683faa002b5c40de6d0279af88c27773f8641c3604c0661a806b5f0177a28c0f586e0006058aa30dc7d6211e69ed72338ea6353c2dd94c2c21634bbcbee5690bcb6deebfc7da1ce591d766f05e4094b7c018839720a3d7c927c2486e3725f724d9db91ac15bb4d39eb8fced54557808fca5b5d83d7cd34dad0fc41e50ef5eb161e6f8a28514d96c51133c6fd5c7e756e14ec4362abfceddc6c837d79a323492638212670efa8e406000e03a39ce37d3faf5cfabc277375ac52d1b5cb0679e4fa33742d382274099bc9bbed5118e9dbf0f7315d62d1c7ec700c47bb78c1b6b21a19045b26eb1be6a366eb45748ab2fbc946e79c6a376d26549c2c8530ff8ee468dde7dd5730a1d4cd04dc62939bbdba9ba4650ac9526e8be5ee304a1fad5f06a2d519a63ef8ce29a86ee22c089c2b843242ef6a51e03aa9cf2d0a483c061ba9be96a4d8fe51550ba645bd62826a2f9a73a3ae14ba99586ef5562e9c72fefd3f752f7da3f046f6977fa0a5980e4a91587b086019b09e6ad3b3ee593e990fd5a9e34d7972cf0b7d9022b8b5196d5ac3a017da67dd1cf3ed67c7d2d281f9f25cfadf2b89b5ad6b4725a88f54ce029ac71e019a5e647b0acfded93fa9be8d3c48d283b57ccf8d5662979132e28785f0191ed756055f7960e44e3d35e8c15056dd488f46dba03a161250564f0bdc3eb9e153c9057a297271aeca93a072a1b3f6d9b1e6321f5f59c66fb26dcf3197533d928b155fdf5035634828aba3cbb28517711c20ad9f8abcc5167ccad925f4de817513830dc8e379d58629320f991ea7a90c2fb3e7bce5121ce64774fbe32a8b6e37ec3293d4648de53696413e680a2ae0810dd6db22469852dfd09072166b39a460a6445c0dd586cdecf1c20c8ae5bbef7dd1b588d40ccd2017f6bb4e3bbdda26a7e3a59ff453e350a44bcb4cdd572eacea8fa6484bb8d6612aebf3c6f47d29be463542f5d9eaec2771bf64e6370740e0d8de75b1357f8721671af537d5d4040cb084eb4e2cc34d2466a0115af84e1b0042895983a1d06b89fb4ce6ea0486f3f3b823520ab82011a1d4b277227f8611560b1e7933fdcbb3a792b344525bda08839e151ce794b2f32c9b7a01fbac9e01cc87ebcc7d1f6cf0111c3a1e8aac71a908749d44fbd9ad0dadecbd50ada380339c32ac69136678df9317ce0b12b4ff79e59b743f5bb3af2d519ff27d9459cbf97222c15e6fc2a0f91fc719b941525fae59361ceb69cebc2a8645912baa8d1b6c1075ee3056a0c10d25065cb03a442e0ec6e0e1698db3b4c98a0be3278e9649f1f9532e0d392dfd3a0342b8971f21e1b0a74414ba3348cc5be7120c37632d8df359f8d9b992f2ee60b6f470fe3f11de54cda541edad891ce6279cfcd3e7e6f1618b166fd2c1d05848fd2c5f6fb2299f523f357a632762393a8353156cccd02acf081625a75ebb56e16369788d273ccde96629281b949d04c50901b71c65614e6c6c7bd327a140a45e1d006c3f27b9ac9aa53fd62a80f00bb25bfe235bdd2f671126905b2040222b6cbcf7ccd769c2b53113ec01640e3d338abbd602547adf0ba38209cf746ce7677afa1c52075606085cbfe4e8ae88dd87aaaf9b04cf9aa7e1948c25c02fb8a8c01c36ae4d6ebe1f990d4f869a65cdea03f09252dc208e69fb74e6132ce77e25b578fdfe33ac372e6"""

_PI_WORDS = [int(_PI_HEX[i : i + 8], 16) for i in range(0, len(_PI_HEX), 8)]
INIT_P = _PI_WORDS[:18]
INIT_S = [_PI_WORDS[18 + i * 256 : 18 + (i + 1) * 256] for i in range(4)]

MASK32 = 0xFFFFFFFF

# HELPER
def _u32(value):
    return value & MASK32

def _f(x, sboxes):
    """F-function Blowfish."""
    a = (x >> 24) & 0xFF
    b = (x >> 16) & 0xFF
    c = (x >> 8) & 0xFF
    d = x & 0xFF

    return _u32(((_u32(sboxes[0][a] + sboxes[1][b]) ^ sboxes[2][c]) + sboxes[3][d]))

def _encrypt_block(block, p, sboxes, collect=False):
    """Enkripsi satu blok 64-bit."""
    left = int.from_bytes(block[:4], "big")
    right = int.from_bytes(block[4:], "big")

    rounds = []

    for i in range(16):
        left ^= p[i]
        f_value = _f(left, sboxes)
        right ^= f_value

        if collect:
            rounds.append(
                {
                    "Round": i + 1,
                    "P": p[i],
                    "L setelah XOR P": left,
                    "F(L)": f_value,
                    "R setelah XOR F": right,
                    "L/R sebelum Swap": f"{left:08X} / {right:08X}",
                }
            )

        left, right = right, left

    # Undo swap terakhir
    left, right = right, left

    # Final whitening
    right ^= p[16]
    left ^= p[17]

    return (left.to_bytes(4, "big") + right.to_bytes(4, "big"), rounds)

def _decrypt_block(block, p, sboxes, collect=False):
    """
    Dekripsi satu blok Blowfish 64-bit.

    Proses dekripsi menggunakan P-Array dalam urutan terbalik:
    P18 → P17 → ... → P3

    Kemudian dilakukan final whitening:
    P2 dan P1
    """

    left = int.from_bytes(block[:4], "big")
    right = int.from_bytes(block[4:], "big")
    rounds = []

    # 16 REVERSE FEISTEL ROUND
    for i in range(17, 1, -1):

        # XOR Left dengan P-Array
        left_before = left
        left ^= p[i]

        # Hitung F(L)
        f_value = _f(left, sboxes)

        # XOR Right dengan F(L)
        right ^= f_value

        if collect:
            rounds.append(
                {
                    "Reverse Round": 18 - i,
                    "P Index": i + 1,
                    "P": p[i],
                    "L Sebelum XOR": left_before,
                    "L Setelah XOR P": left,
                    "F(L)": f_value,
                    "R Setelah XOR F": right,
                }
            )

        # Swap
        left, right = right, left

    # UNDO SWAP TERAKHIR
    left, right = right, left

    # FINAL WHITENING
    right_before = right
    left_before = left

    right ^= p[1]
    left ^= p[0]

    if collect:
        rounds.append(
            {
                "Reverse Round": "Final Whitening",
                "P Index": "P2/P1",
                "P": None,
                "L Sebelum XOR": left_before,
                "L Setelah XOR P": left,
                "F(L)": None,
                "R Setelah XOR F": right,
            }
        )

    plaintext_block = left.to_bytes(4, "big") + right.to_bytes(4, "big")

    if collect:
        return plaintext_block, rounds

    return plaintext_block

# KEY EXPANSION
def _key_expand(key_bytes):
    p = INIT_P.copy()
    s = [box.copy() for box in INIT_S]

    # XOR key terhadap P-array
    key_index = 0
    xor_rows = []

    for i in range(18):
        key_word = 0

        for _ in range(4):
            key_word = (key_word << 8) | key_bytes[key_index]
            key_index = (key_index + 1) % len(key_bytes)

        p[i] ^= key_word

        xor_rows.append(
            {
                "Subkey": f"P{i + 1}",
                "P Awal": f"0x{INIT_P[i]:08X}",
                "Key Word": f"0x{key_word:08X}",
                "P Setelah XOR": f"0x{p[i]:08X}",
            }
        )

    # Enkripsi blok nol secara berulang untuk mengisi P-array
    block = b"\x00" * 8
    p_expand_rows = []

    for i in range(0, 18, 2):
        block, _ = _encrypt_block(block, p, s)

        p[i] = int.from_bytes(block[:4], "big")
        p[i + 1] = int.from_bytes(block[4:], "big")

        p_expand_rows.append(
            {
                "Pasangan": f"P{i + 1}, P{i + 2}",
                "P Baru 1": f"0x{p[i]:08X}",
                "P Baru 2": f"0x{p[i + 1]:08X}",
            }
        )

    # Enkripsi berulang untuk seluruh S-box
    s_summary = []

    for box_index in range(4):
        for i in range(0, 256, 2):
            block, _ = _encrypt_block(block, p, s)

            s[box_index][i] = int.from_bytes(block[:4], "big")
            s[box_index][i + 1] = int.from_bytes(block[4:], "big")

        s_summary.append(
            {
                "S-Box": f"S{box_index + 1}",
                "Jumlah Entry": 256,
                "Entry Pertama": f"0x{s[box_index][0]:08X}",
                "Entry Terakhir": f"0x{s[box_index][255]:08X}",
            }
        )

    return p, s, xor_rows, p_expand_rows, s_summary

# PADDING
def pad_pkcs7(data, block_size=8):
    padding_len = block_size - (len(data) % block_size)
    return (data + bytes([padding_len]) * padding_len, padding_len)

def unpad_pkcs7(data, block_size=8):
    if not data:
        raise ValueError("Data kosong.")

    padding_len = data[-1]

    if not 1 <= padding_len <= block_size:
        raise ValueError("Padding PKCS7 tidak valid.")

    if data[-padding_len:] != bytes([padding_len]) * padding_len:
        raise ValueError("Padding PKCS7 rusak.")

    return data[:-padding_len], padding_len

# VISUAL HTML
def _table(df):
    if df is None or df.empty:
        return ""

    return df.to_html(index=False, escape=False, border=0, classes="bf-table")

def _details(title, description="", content="", df=None, open_by_default=False):
    open_attr = " open" if open_by_default else ""

    title = dedent(str(title)).strip()
    description = dedent(str(description)).strip() if description else ""
    content = dedent(str(content)).strip() if content else ""

    body_parts = []

    if description:
        body_parts.append(f'<div class="bf-desc">{description}</div>')

    if content:
        body_parts.append(f'<div class="bf-content">{content}</div>')

    if df is not None:
        body_parts.append('<div class="bf-table-wrap">' + _table(df) + "</div>")

    body = "".join(body_parts)

    return (
        f'<details class="bf-step"{open_attr}>'
        f"<summary>{title}</summary>"
        f'<div class="bf-body">{body}</div>'
        f"</details>"
    )

def _css():
    return """
<style>
.bf-step {
    background: var(--surface, #202722);
    border: 1px solid var(--line, #3a463e);
    border-radius: 5px;
    margin: 10px 0;
    overflow: hidden;
}

.bf-step summary {
    cursor: pointer;
    padding: 14px 16px;
    font-weight: 700;
    color: var(--text, #e9efeb);
    background: var(--surface-raised, #29322c);
    user-select: none;
}

.bf-step summary:hover {
    background: #313b34;
}

.bf-body {
    padding: 14px 16px 18px 16px;
    color: var(--text, #e9efeb);
}

.bf-desc {
    color: var(--muted, #a5b0a8);
    margin-bottom: 12px;
    line-height: 1.6;
}

.bf-content {
    line-height: 1.8;
    margin: 8px 0;
}

.bf-table-wrap {
    overflow-x: auto;
    margin-top: 12px;
}

.bf-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}

.bf-table th {
    background: var(--surface-raised, #29322c);
    color: var(--text, #e9efeb);
    padding: 8px;
    border: 1px solid var(--line, #3a463e);
    text-align: left;
    white-space: nowrap;
}

.bf-table td {
    padding: 8px;
    border: 1px solid var(--line, #3a463e);
    white-space: nowrap;
}

.bf-formula {
    background: var(--app-bg, #151a17);
    border-left: 3px solid var(--accent, #47a879);
    padding: 10px 12px;
    margin: 10px 0;
    font-family: monospace;
    line-height: 1.7;
}

.bf-result {
    background: var(--app-bg, #151a17);
    border: 1px solid var(--line, #3a463e);
    border-radius: 4px;
    padding: 12px;
    margin-top: 10px;
}

.bf-note {
    color: var(--muted, #a5b0a8);
    font-size: 0.9em;
}
</style>
"""

# PROCESS
def process(text: str, key: str, mode: str):
    key_bytes = key.encode("utf-8")

    if not 4 <= len(key_bytes) <= 56:
        error = (
            "**Kunci Blowfish tidak valid.** "
            "Panjang kunci harus 4–56 byte "
            "(32–448 bit)."
        )

        return "Error: Kunci Tidak Valid!", [
            _css(),
            _details(
                "Validasi kunci",
                "Blowfish menerima kunci 4 sampai 56 byte.",
                f"<b>Kunci saat ini:</b> {html.escape(key)}",
            ),
        ]

    try:
        p, s, xor_rows, p_expand_rows, s_summary = _key_expand(key_bytes)
    except Exception as e:
        return "Gagal!", [
            _css(),
            _details("Ekspansi kunci gagal", content=html.escape(str(e))),
        ]

    # ENKRIPSI
    if mode == "Enkripsi":
        try:
            plain_bytes = text.encode("utf-8")
            padded, pad_len = pad_pkcs7(plain_bytes, 8)

            # STEP 1
            block_rows = []

            for i in range(0, len(padded), 8):
                block = padded[i : i + 8]

                block_rows.append(
                    {
                        "Blok": f"Blok {i // 8 + 1}",
                        "Data Hex": block.hex().upper(),
                        "L0": f"0x{block[:4].hex().upper()}",
                        "R0": f"0x{block[4:].hex().upper()}",
                    }
                )

            # STEP 2
            xor_df = pd.DataFrame(xor_rows)

            # STEP 3
            p_expand_df = pd.DataFrame(p_expand_rows)
            s_df = pd.DataFrame(s_summary)

            # STEP 4 - proses round untuk setiap block
            encrypted_blocks = []
            round_tables = []

            for block_index in range(0, len(padded), 8):
                block = padded[block_index : block_index + 8]

                encrypted_block, round_data = _encrypt_block(block, p, s, collect=True)

                encrypted_blocks.append(encrypted_block)

                rows = []

                for row in round_data:
                    rows.append(
                        {
                            "Round": row["Round"],
                            "P": f"0x{row['P']:08X}",
                            "L": f"0x{row['L setelah XOR P']:08X}",
                            "F(L)": f"0x{row['F(L)']:08X}",
                            "R": f"0x{row['R setelah XOR F']:08X}",
                        }
                    )

                round_tables.append(pd.DataFrame(rows))

            ciphertext = b"".join(encrypted_blocks)

            result_base64 = base64.b64encode(ciphertext).decode("ascii")

            # LOGS / EXPANDERS
            logs = [_css()]

            logs.append(
                _details(
                    "Informasi input",
                    "Data yang akan diproses oleh Blowfish.",
                    f"""
                    <b>Plaintext:</b> <code>{html.escape(text)}</code><br>
                    <b>Kunci:</b> <code>{html.escape(key)}</code><br>
                    <b>Panjang kunci:</b> {len(key_bytes)} byte<br>
                    <b>Block size:</b> 64-bit (8 byte)<br>
                    <b>Mode:</b> ECB
                    """,
                    open_by_default=True,
                )
            )

            logs.append(
                _details(
                    "Langkah 1 — Plaintext ke byte ke blok 64-bit",
                    (
                        f"Plaintext diubah menjadi UTF-8, kemudian "
                        f"ditambahkan PKCS7 padding sebanyak "
                        f"<b>{pad_len} byte</b>. Setelah itu data "
                        f"dibagi menjadi blok 64-bit."
                    ),
                    f"""
                    <b>Plaintext Hex:</b>
                    <code>{plain_bytes.hex().upper()}</code><br>
                    <b>Padding:</b>
                    <code>{pad_len}</code> byte<br>
                    <b>Setelah Padding:</b>
                    <code>{padded.hex().upper()}</code>
                    """,
                    pd.DataFrame(block_rows),
                    open_by_default=True,
                )
            )

            logs.append(
                _details(
                    "Langkah 2 — XOR kunci dengan P-Array awal",
                    (
                        "Setiap word 32-bit pada P-Array di-XOR "
                        "dengan potongan key secara berulang."
                    ),
                    """
                    <div class="bf-formula">
                    P[i] = P[i] XOR KeyWord
                    </div>
                    """,
                    xor_df,
                )
            )

            logs.append(
                _details(
                    "Langkah 3 — Ekspansi kunci P-Array dan S-Box",
                    (
                        "Blowfish mengenkripsi blok nol secara berulang "
                        "untuk membentuk P-Array final dan kemudian "
                        "seluruh S-Box. Tahap ini membuat subkey "
                        "bergantung pada key."
                    ),
                    """
                    <div class="bf-formula">
                    18 P-Array + 4 S-Box × 256 entry
                    </div>
                    <div class="bf-note">
                    Tabel P-Array dan ringkasan S-Box ditampilkan agar
                    proses tetap mudah dibaca tanpa memenuhi layar
                    dengan 1024 nilai S-Box.
                    </div>
                    """,
                    None,
                )
            )

            # Nested-ish: karena <details> tidak aman untuk nested
            # dalam beberapa renderer, tampilkan tabel P/S dalam content.
            logs.append(
                _details(
                    "   └─ STEP 3A — P-Array Setelah Key Expansion",
                    "Nilai final P1 sampai P18.",
                    "",
                    pd.DataFrame(
                        [
                            {"Subkey": f"P{i + 1}", "Nilai Final": f"0x{p[i]:08X}"}
                            for i in range(18)
                        ]
                    ),
                )
            )

            logs.append(
                _details(
                    "   └─ STEP 3B — Ringkasan S-Box",
                    "Masing-masing S-Box memiliki 256 entry 32-bit.",
                    "",
                    s_df,
                )
            )

            for block_no, round_df in enumerate(round_tables, 1):
                logs.append(
                    _details(
                        f"🔄 STEP 4 — Feistel Network: Blok {block_no}",
                        (
                            "Blok diproses melalui 16 putaran. "
                            "Pada setiap putaran: L XOR P[i], "
                            "hitung F(L), kemudian R XOR F(L), "
                            "lalu swap L dan R."
                        ),
                        """
                        <div class="bf-formula">
                        L = L XOR P[i]<br>
                        R = R XOR F(L)<br>
                        SWAP(L, R)
                        </div>
                        """,
                        round_df,
                    )
                )

            logs.append(
                _details(
                    "Langkah 5 — Final whitening dan ciphertext",
                    (
                        "Setelah Round 16, dilakukan pembalikan swap "
                        "terakhir dan XOR dengan P17 serta P18."
                    ),
                    f"""
                    <b>Ciphertext Hex:</b>
                    <code>{ciphertext.hex().upper()}</code><br>
                    <div class="bf-result">
                    <b>Final Ciphertext (Base64):</b><br>
                    <code>{result_base64}</code>
                    </div>
                    """,
                )
            )

            return result_base64, logs

        except Exception as e:
            return "Gagal Enkripsi!", [
                _css(),
                _details("Enkripsi gagal", content=html.escape(str(e))),
            ]

    # MODE DEKRIPSI
    else:
        try:
            ciphertext_b64 = text.strip()

            if not ciphertext_b64:
                raise ValueError("Ciphertext tidak boleh kosong.")

            # Base64 → Bytes
            encrypted_bytes = base64.b64decode(ciphertext_b64, validate=True)

            # Validasi ukuran blok
            if len(encrypted_bytes) == 0:
                raise ValueError("Ciphertext tidak menghasilkan data.")

            if len(encrypted_bytes) % 8 != 0:
                raise ValueError(
                    "Ukuran ciphertext harus kelipatan "
                    "8 byte karena Blowfish menggunakan "
                    "blok 64-bit."
                )

            num_blocks = len(encrypted_bytes) // 8

            # KEY EXPANSION
            p, s, xor_rows, p_expand_rows, s_summary = _key_expand(key_bytes)

            # LOG / EXPANDER
            logs = [_css()]

            # INFORMASI INPUT
            logs.append(
                _details(
                    "Informasi dekripsi",
                    ("Informasi dasar ciphertext dan kunci yang digunakan."),
                    f"""
                    <b>Ciphertext Base64:</b> <code>{html.escape(ciphertext_b64)}</code> <br>
                    <b>Kunci:</b> <code>{html.escape(key)}</code> <br>
                    <b>Panjang Kunci:</b> {len(key_bytes)} byte <br>
                    <b>Block Size:</b> 64-bit (8 byte) <br>
                    <b>Jumlah Blok:</b> {num_blocks} <br>
                    <b>Mode:</b> ECB
                    """,
                    open_by_default=True,
                )
            )

            # STEP 1 BASE64 → BYTES → BLOK 64-BIT
            block_rows = []

            for block_index in range(0, len(encrypted_bytes), 8):

                block = encrypted_bytes[block_index : block_index + 8]

                left = int.from_bytes(block[:4], "big")

                right = int.from_bytes(block[4:], "big")

                block_rows.append(
                    {
                        "Blok": f"Blok {block_index // 8 + 1}",
                        "Ciphertext Hex": f"0x{block.hex().upper()}",
                        "L0 (32-bit)": f"0x{left:08X}",
                        "R0 (32-bit)": f"0x{right:08X}",
                        "Ukuran": "64-bit",
                    }
                )

            logs.append(
                _details(
                    "📥 STEP 1 — Base64 → Bytes → Blok 64-bit",
                    (
                        "Ciphertext Base64 dikembalikan menjadi "
                        "byte mentah. Kemudian setiap 8 byte "
                        "dipisahkan menjadi L0 dan R0."
                    ),
                    f"""
                    <b>Base64:</b>
                    <code>{html.escape(ciphertext_b64)}</code>
                    <br>

                    <b>Ciphertext Hex:</b>
                    <code>{encrypted_bytes.hex().upper()}</code>

                    <div class="bf-formula">
                        1 blok = 64-bit = 8 byte
                        <br>
                        L0 = 32-bit
                        <br>
                        R0 = 32-bit
                    </div>
                    """,
                    pd.DataFrame(block_rows),
                    open_by_default=True,
                )
            )

            # STEP 2 KEY EXPANSION
            xor_df = pd.DataFrame(xor_rows)

            logs.append(
                _details(
                    "Langkah 2 — Ekspansi kunci",
                    (
                        "Kunci yang sama seperti saat enkripsi "
                        "digunakan untuk membentuk P-Array dan "
                        "S-Box yang identik."
                    ),
                    f"""
                    <div class="bf-formula">
                        P[i] = P[i] XOR KeyWord
                    </div>

                    <p>
                    Blowfish kemudian melakukan ekspansi
                    lebih lanjut menggunakan enkripsi blok
                    nol sehingga terbentuk P-Array final
                    dan empat S-Box.
                    </p>
                    """,
                    xor_df,
                )
            )

            # STEP 2A P-ARRAY FINAL
            p_final_df = pd.DataFrame(
                [
                    {"Subkey": f"P{i + 1}", "Nilai Final": f"0x{p[i]:08X}"}
                    for i in range(18)
                ]
            )

            logs.append(
                _details(
                    "   └─ STEP 2A — P-Array Final",
                    (
                        "P-Array hasil key expansion yang "
                        "digunakan pada proses reverse "
                        "Feistel."
                    ),
                    None,
                    p_final_df,
                )
            )

            # STEP 2B S-BOX
            s_df = pd.DataFrame(s_summary)

            logs.append(
                _details(
                    "   └─ STEP 2B — S-Box",
                    (
                        "Blowfish menggunakan empat S-Box. "
                        "Masing-masing memiliki 256 entry "
                        "32-bit."
                    ),
                    """
                    <div class="bf-formula">
                        S1 = 256 entry
                        <br>
                        S2 = 256 entry
                        <br>
                        S3 = 256 entry
                        <br>
                        S4 = 256 entry
                    </div>
                    """,
                    s_df,
                )
            )

            # STEP 3 REVERSE FEISTEL
            decrypted_blocks = []

            for block_index in range(0, len(encrypted_bytes), 8):

                block = encrypted_bytes[block_index : block_index + 8]

                # DECRYPT BLOCK + COLLECT ROUND
                decrypted_block, round_data = _decrypt_block(block, p, s, collect=True)
                decrypted_blocks.append(decrypted_block)

                # TABLE ROUND
                round_rows = []
                for row in round_data:
                    if row["P"] is None:

                        round_rows.append(
                            {
                                "Round": row["Reverse Round"],
                                "P": "P2 / P1",
                                "L Sebelum": f"0x{row['L Sebelum XOR']:08X}",
                                "L Setelah": f"0x{row['L Setelah XOR P']:08X}",
                                "F(L)": "-",
                                "R": f"0x{row['R Setelah XOR F']:08X}",
                            }
                        )

                    else:

                        round_rows.append(
                            {
                                "Round": row["Reverse Round"],
                                "P": f"P{row['P Index']}",
                                "L Sebelum": f"0x{row['L Sebelum XOR']:08X}",
                                "L Setelah XOR P": f"0x{row['L Setelah XOR P']:08X}",
                                "F(L)": f"0x{row['F(L)']:08X}",
                                "R Setelah XOR F": f"0x{row['R Setelah XOR F']:08X}",
                            }
                        )

                round_df = pd.DataFrame(round_rows)

                logs.append(
                    _details(
                        (
                            f"🔄 STEP 3 — Reverse Feistel "
                            f"Network: Blok "
                            f"{block_index // 8 + 1}"
                        ),
                        (
                            "Dekripsi membalikkan proses "
                            "Feistel dengan menggunakan "
                            "P-Array dari P18 menuju P3."
                        ),
                        (
                            '<div class="bf-formula">'
                            'Untuk setiap reverse round:<br>'
                            'L = L XOR P[i]<br>'
                            'F(L) = ((S1[a] + S2[b]) XOR S3[c]) + S4[d]<br>'
                            'R = R XOR F(L)<br>'
                            'SWAP(L, R)'
                            '</div>'
                            '<div class="bf-note">'
                            'Reverse round menggunakan: P18 → P17 → ... → P3.<br>'
                            'Setelah itu dilakukan final whitening menggunakan P2 dan P1.'
                            '</div>'
                        ),
                        round_df,
                    )
                )

            # GABUNGKAN SEMUA BLOK
            padded_bytes = b"".join(decrypted_blocks)

            # STEP 4 PKCS7 UNPADDING
            unpadded_bytes, pad_len = unpad_pkcs7(padded_bytes, 8)

            logs.append(
                _details(
                    "✂️ STEP 4 — PKCS7 Unpadding",
                    (
                        "Setelah semua blok berhasil "
                        "didekripsi, padding PKCS7 "
                        "dihapus untuk mendapatkan data asli."
                    ),
                    (
                        f'<b>Data sebelum unpadding:</b> '
                        f'<code>{padded_bytes.hex().upper()}</code><br>'
                        f'<div class="bf-formula">'
                        f'Padding Length = {pad_len} byte<br>'
                        f'Padding Value = 0x{pad_len:02X}'
                        f'</div>'
                        f'<b>Data setelah unpadding:</b><br>'
                        f'<code>{unpadded_bytes.hex().upper()}</code>'
                    ),
                )
            )

            # STEP 5 BYTES → UTF-8
            plaintext = unpadded_bytes.decode("utf-8")

            logs.append(
                _details(
                    "Langkah 5 — Byte ke UTF-8 ke plaintext",
                    (
                        "Data hasil dekripsi yang telah "
                        "dihapus padding-nya dikonversi "
                        "kembali menjadi teks UTF-8."
                    ),
                    (
                        f'<b>Plaintext Hex:</b> '
                        f'<code>{unpadded_bytes.hex().upper()}</code><br>'
                        f'<div class="bf-result">'
                        f'<b>Plaintext Hasil Dekripsi:</b><br>'
                        f'<code>{html.escape(plaintext)}</code>'
                        f'</div>'
                    ),
                )
            )

            # HASIL AKHIR
            logs.append(
                _details(
                    "Hasil akhir dekripsi",
                    "Dekripsi Blowfish berhasil.",
                    f"""
                    <b>Ciphertext: <code>{html.escape(ciphertext_b64)}</code> </b>

                    <b>Kunci: <code>{html.escape(key)}</code></b>
                    """,
                    open_by_default=True,
                )
            )

            return plaintext, logs

        except Exception as e:

            return "Gagal Dekripsi!", [
                _css(),
                _details(
                    "Dekripsi gagal",
                    "Terjadi kesalahan saat melakukan dekripsi.",
                    f"""
                    <b>Detail Error:</b>

                    <br>

                    <code>
                    {html.escape(str(e))}
                    </code>

                    <br>
                    <b>Periksa:</b>

                    <ul>
                        <li>
                            Ciphertext merupakan Base64
                            yang valid.
                        </li>

                        <li>
                            Ciphertext memiliki panjang
                            kelipatan 8 byte.
                        </li>

                        <li>
                            Kunci sama dengan kunci
                            saat enkripsi.
                        </li>

                        <li>
                            Ciphertext tidak mengalami
                            perubahan.
                        </li>
                    </ul>
                    """,
                ),
            ]
