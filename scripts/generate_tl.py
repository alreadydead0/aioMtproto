"""
Deterministic Telegram TL Schema Parser and Code Generator for Layer 229.
Fetches official api.tl and mtproto.tl, parses constructors and functions,
and generates aiogram/raw/types/__init__.py, aiogram/raw/functions/__init__.py,
and aiogram/raw/all.py.
"""

from __future__ import annotations

import os
import re
import urllib.request
import zlib
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

SCHEME_DIR = Path(__file__).parent / "scheme"
API_TL_URL = "https://raw.githubusercontent.com/telegramdesktop/tdesktop/dev/Telegram/SourceFiles/mtproto/scheme/api.tl"
MTPROTO_TL_URL = "https://raw.githubusercontent.com/telegramdesktop/tdesktop/dev/Telegram/SourceFiles/mtproto/scheme/mtproto.tl"

RAW_DIR = Path(__file__).parent.parent / "aiogram" / "raw"


def fetch_and_cache_schema() -> Tuple[str, str]:
    SCHEME_DIR.mkdir(parents=True, exist_ok=True)
    api_path = SCHEME_DIR / "api.tl"
    mtproto_path = SCHEME_DIR / "mtproto.tl"

    if not api_path.exists():
        req = urllib.request.Request(API_TL_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            api_content = response.read().decode("utf-8")
        api_path.write_text(api_content, encoding="utf-8")
    else:
        api_content = api_path.read_text(encoding="utf-8")

    if not mtproto_path.exists():
        req = urllib.request.Request(MTPROTO_TL_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            mtproto_content = response.read().decode("utf-8")
        mtproto_path.write_text(mtproto_content, encoding="utf-8")
    else:
        mtproto_content = mtproto_path.read_text(encoding="utf-8")

    return api_content, mtproto_content


def crc32_tl(string: str) -> int:
    string = re.sub(r" \w+:\bTYPE\b", "", string)
    string = string.replace(":", " ").replace(";", "")
    string = re.sub(r"\s+", " ", string).strip()
    return zlib.crc32(string.encode("ascii"))


def pascal_case(fullname: str) -> str:
    parts = fullname.split(".")
    res = []
    for part in parts:
        sub = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", part)
        words = sub.split("_")
        res.append("".join(w.capitalize() for w in words if w))
    return "".join(res)


def safe_param_name(name: str) -> str:
    if name == "self":
        return "is_self"
    if name in ("from", "in", "import", "def", "class", "global", "lambda", "return", "pass"):
        return f"{name}_"
    return name


class TLArg:
    def __init__(self, name: str, arg_type: str) -> None:
        self.raw_name = name
        self.name = safe_param_name(name)
        self.raw_type = arg_type
        self.flag_name: Optional[str] = None
        self.flag_bit: Optional[int] = None
        self.is_flag_num: bool = False
        self.is_optional: bool = False
        self.type_name: str = arg_type

        flag_match = re.match(r"^([a-zA-Z0-9_]+)\.(\d+)\?(.*)$", arg_type)
        if flag_match:
            self.flag_name = flag_match.group(1)
            self.flag_bit = int(flag_match.group(2))
            self.is_optional = True
            self.type_name = flag_match.group(3)

        if arg_type in ("#", "flags:#", "flags2:#"):
            self.is_flag_num = True


class TLEntry:
    def __init__(
        self, fullname: str, hex_id: Optional[str], args: List[TLArg], result_type: str, section: str
    ) -> None:
        self.fullname = fullname
        self.args = args
        self.result_type = result_type
        self.section = section

        if "." in fullname:
            self.namespace, self.name = fullname.split(".", 1)
        else:
            self.namespace = ""
            self.name = fullname

        if hex_id:
            self.id = int(hex_id, 16)
        else:
            args_str = " ".join([f"{a.raw_name}:{a.raw_type}" for a in args])
            tl_str = f"{fullname} {args_str} = {result_type};"
            self.id = crc32_tl(tl_str)

        self.class_name = pascal_case(fullname)
        reserved_types = {"int", "long", "string", "bytes", "bool", "Bool", "X", "!X", "true", "True"}
        self.base_class_name = pascal_case(result_type) if result_type and not result_type.startswith("Vector") and result_type not in reserved_types else "TLObject"


def parse_tl_schema(api_content: str, mtproto_content: str) -> List[TLEntry]:
    entries: List[TLEntry] = []
    combined = api_content + "\n" + mtproto_content

    current_section = "types"
    for line in combined.splitlines():
        line = line.strip()
        if not line or line.startswith("//"):
            continue
        if line == "---types---":
            current_section = "types"
            continue
        if line == "---functions---":
            current_section = "functions"
            continue

        m = re.match(r"^([a-zA-Z0-9_.]+)(?:#([0-9a-fA-F]+))?\s*(.*?)=\s*([a-zA-Z0-9_.<>!]+);", line)
        if not m:
            continue

        fullname, hex_id, args_str, res_type = m.groups()
        args = []
        if args_str.strip():
            tokens = args_str.strip().split()
            for token in tokens:
                if token.startswith("{") and token.endswith("}"):
                    continue
                if ":" in token:
                    p_name, p_type = token.split(":", 1)
                    args.append(TLArg(p_name, p_type))

        entries.append(TLEntry(fullname, hex_id, args, res_type, current_section))

    return entries


def generate_writer_expr(arg: TLArg, var_name: Optional[str] = None) -> str:
    t = arg.type_name
    var = var_name or f"self.{arg.name}"
    if t == "int":
        return f"write_int({var})"
    elif t == "long":
        return f"write_long({var})"
    elif t == "int128":
        return f"write_int128({var})"
    elif t == "int256":
        return f"write_int256({var})"
    elif t == "double":
        return f"write_double({var})"
    elif t == "string":
        return f"write_string({var})"
    elif t == "bytes":
        return f"write_bytes({var})"
    elif t in ("bool", "Bool"):
        return f"write_bool({var})"
    elif t == "true":
        return "b''"
    elif t.startswith("Vector<") or t.startswith("vector<"):
        inner = t[t.find("<") + 1 : t.rfind(">")]
        if inner == "int":
            return f"write_vector({var}, write_int)"
        elif inner == "long":
            return f"write_vector({var}, write_long)"
        elif inner == "string":
            return f"write_vector({var}, write_string)"
        elif inner == "bytes":
            return f"write_vector({var}, write_bytes)"
        else:
            return f"write_vector({var}, lambda x: x.write() if hasattr(x, 'write') else write_bytes(x))"
    else:
        return f"({var}.write() if hasattr({var}, 'write') else write_bytes({var}))"


def generate_reader_expr(arg: TLArg) -> str:
    t = arg.type_name
    if t == "int":
        return "read_int(b)"
    elif t == "long":
        return "read_long(b)"
    elif t == "int128":
        return "read_int128(b)"
    elif t == "int256":
        return "read_int256(b)"
    elif t == "double":
        return "read_double(b)"
    elif t == "string":
        return "read_string(b)"
    elif t == "bytes":
        return "read_bytes(b)"
    elif t in ("bool", "Bool"):
        return "read_bool(b)"
    elif t == "true":
        return "True"
    elif t.startswith("Vector<") or t.startswith("vector<"):
        inner = t[t.find("<") + 1 : t.rfind(">")]
        if inner == "int":
            return "read_vector(b, read_int)"
        elif inner == "long":
            return "read_vector(b, read_long)"
        elif inner == "string":
            return "read_vector(b, read_string)"
        elif inner == "bytes":
            return "read_vector(b, read_bytes)"
        else:
            return "read_vector(b, read_tl_object)"
    else:
        return "read_tl_object(b)"


def generate_type_class(entry: TLEntry) -> str:
    lines = []
    base_cls = entry.base_class_name if entry.base_class_name != entry.class_name else "TLObject"
    lines.append(f"class {entry.class_name}({base_cls}):")
    lines.append(f"    ID = {hex(entry.id).upper()}")
    lines.append(f'    QUALNAME = "{entry.section}.{entry.fullname}"')
    lines.append("")

    init_args = []
    has_bytes_arg = False
    for a in entry.args:
        if a.is_flag_num:
            continue
        if a.name == "bytes":
            has_bytes_arg = True
        init_args.append(f"{a.name}: Any = None")

    if has_bytes_arg:
        init_args.append("bytes_data: Any = None")

    if init_args:
        lines.append(f"    def __init__(self, {', '.join(init_args)}) -> None:")
        for a in entry.args:
            if not a.is_flag_num:
                if a.name == "bytes":
                    lines.append("        b_val = bytes if bytes is not None else bytes_data")
                    lines.append("        self.bytes = b_val")
                    lines.append("        self.bytes_data = b_val")
                else:
                    lines.append(f"        self.{a.name} = {a.name}")
    else:
        lines.append("    def __init__(self) -> None:")
        lines.append("        pass")

    lines.append("")

    # Write
    lines.append("    def write(self) -> bytes:")
    flag_vars = set(a.name for a in entry.args if a.is_flag_num)
    if "flags" in flag_vars:
        lines.append("        flags = 0")
        for a in entry.args:
            if a.flag_name == "flags" and a.flag_bit is not None:
                if a.type_name == "true":
                    lines.append(f"        if getattr(self, '{a.name}', None):")
                else:
                    lines.append(f"        if getattr(self, '{a.name}', None) is not None and getattr(self, '{a.name}', None) is not False:")
                lines.append(f"            flags |= (1 << {a.flag_bit})")

    if "flags2" in flag_vars:
        lines.append("        flags2 = 0")
        for a in entry.args:
            if a.flag_name == "flags2" and a.flag_bit is not None:
                if a.type_name == "true":
                    lines.append(f"        if getattr(self, '{a.name}', None):")
                else:
                    lines.append(f"        if getattr(self, '{a.name}', None) is not None and getattr(self, '{a.name}', None) is not False:")
                lines.append(f"            flags2 |= (1 << {a.flag_bit})")

    lines.append("        res = struct.pack('<I', self.ID)")
    for a in entry.args:
        if a.is_flag_num:
            lines.append(f"        res += write_int({a.name})")
        elif a.is_optional:
            if a.type_name == "true":
                continue
            flag_var = a.flag_name
            lines.append(f"        if bool({flag_var} & (1 << {a.flag_bit})):")
            if a.type_name in ("int", "long", "double"):
                val_expr = f"getattr(self, '{a.name}', None) or 0"
            elif a.type_name == "string":
                val_expr = f"getattr(self, '{a.name}', None) or ''"
            elif a.type_name == "bytes":
                val_expr = f"getattr(self, '{a.name}', None) or b''"
            elif a.type_name.startswith("Vector") or a.type_name.startswith("vector"):
                val_expr = f"getattr(self, '{a.name}', None) or []"
            else:
                val_expr = f"getattr(self, '{a.name}', None)"
            lines.append(f"            v = {val_expr}")
            lines.append(f"            if v is not None:")
            lines.append(f"                res += {generate_writer_expr(a, 'v')}")
        else:
            lines.append(f"        res += {generate_writer_expr(a)}")
    lines.append("        return res")
    lines.append("")

    # Read
    lines.append("    @classmethod")
    lines.append(f"    def read(cls, b: BinaryIO) -> {entry.class_name}:")
    lines.append("        from aiogram.raw.all import read_tl_object")
    for a in entry.args:
        if a.is_flag_num:
            lines.append(f"        {a.name} = read_int(b)")
        elif a.is_optional:
            flag_check = f"bool({a.flag_name} & (1 << {a.flag_bit}))"
            if a.type_name == "true":
                lines.append(f"        {a.name} = {flag_check}")
            else:
                lines.append(f"        {a.name} = {generate_reader_expr(a)} if {flag_check} else None")
        else:
            lines.append(f"        {a.name} = {generate_reader_expr(a)}")

    kwargs_str = ", ".join(f"{a.name}={a.name}" for a in entry.args if not a.is_flag_num)
    lines.append(f"        return {entry.class_name}({kwargs_str})")
    lines.append("")

    return "\n".join(lines)


def generate_func_class(entry: TLEntry) -> str:
    lines = []
    lines.append(f"class {entry.class_name}(TLRequest[Any]):")
    lines.append(f"    ID = {hex(entry.id).upper()}")
    lines.append(f'    QUALNAME = "{entry.section}.{entry.fullname}"')
    lines.append("")

    init_args = []
    has_bytes_arg = False
    for a in entry.args:
        if a.is_flag_num:
            continue
        if a.name == "bytes":
            has_bytes_arg = True
        init_args.append(f"{a.name}: Any = None")

    if has_bytes_arg:
        init_args.append("bytes_data: Any = None")

    if init_args:
        lines.append(f"    def __init__(self, {', '.join(init_args)}) -> None:")
        for a in entry.args:
            if not a.is_flag_num:
                if a.name == "bytes":
                    lines.append("        b_val = bytes if bytes is not None else bytes_data")
                    lines.append("        self.bytes = b_val")
                    lines.append("        self.bytes_data = b_val")
                else:
                    lines.append(f"        self.{a.name} = {a.name}")
    else:
        lines.append("    def __init__(self) -> None:")
        lines.append("        pass")

    lines.append("")

    # Write
    lines.append("    def write(self) -> bytes:")
    flag_vars = set(a.name for a in entry.args if a.is_flag_num)
    if "flags" in flag_vars:
        lines.append("        flags = 0")
        for a in entry.args:
            if a.flag_name == "flags" and a.flag_bit is not None:
                if a.type_name == "true":
                    lines.append(f"        if getattr(self, '{a.name}', None):")
                else:
                    lines.append(f"        if getattr(self, '{a.name}', None) is not None and getattr(self, '{a.name}', None) is not False:")
                lines.append(f"            flags |= (1 << {a.flag_bit})")

    if "flags2" in flag_vars:
        lines.append("        flags2 = 0")
        for a in entry.args:
            if a.flag_name == "flags2" and a.flag_bit is not None:
                if a.type_name == "true":
                    lines.append(f"        if getattr(self, '{a.name}', None):")
                else:
                    lines.append(f"        if getattr(self, '{a.name}', None) is not None and getattr(self, '{a.name}', None) is not False:")
                lines.append(f"            flags2 |= (1 << {a.flag_bit})")

    lines.append("        res = struct.pack('<I', self.ID)")
    for a in entry.args:
        if a.is_flag_num:
            lines.append(f"        res += write_int({a.name})")
        elif a.is_optional:
            if a.type_name == "true":
                continue
            flag_var = a.flag_name
            lines.append(f"        if bool({flag_var} & (1 << {a.flag_bit})):")
            if a.type_name in ("int", "long", "double"):
                val_expr = f"getattr(self, '{a.name}', None) or 0"
            elif a.type_name == "string":
                val_expr = f"getattr(self, '{a.name}', None) or ''"
            elif a.type_name == "bytes":
                val_expr = f"getattr(self, '{a.name}', None) or b''"
            elif a.type_name.startswith("Vector") or a.type_name.startswith("vector"):
                val_expr = f"getattr(self, '{a.name}', None) or []"
            else:
                val_expr = f"getattr(self, '{a.name}', None)"
            lines.append(f"            v = {val_expr}")
            lines.append(f"            if v is not None:")
            lines.append(f"                res += {generate_writer_expr(a, 'v')}")
        else:
            lines.append(f"        res += {generate_writer_expr(a)}")
    lines.append("        return res")
    lines.append("")

    # read_result
    lines.append("    def read_result(self, b: BinaryIO) -> Any:")
    lines.append("        from aiogram.raw.all import read_tl_object")
    res_t = entry.result_type
    if res_t in ("Vector<int>", "vector<int>"):
        lines.append("        c_id = read_uint(b)")
        lines.append("        b.seek(b.tell() - 4)")
        lines.append("        if c_id == 0x1CB5C415:")
        lines.append("            return read_vector(b, read_int)")
        lines.append("        return read_tl_object(b)")
    elif res_t in ("Vector<long>", "vector<long>"):
        lines.append("        c_id = read_uint(b)")
        lines.append("        b.seek(b.tell() - 4)")
        lines.append("        if c_id == 0x1CB5C415:")
        lines.append("            return read_vector(b, read_long)")
        lines.append("        return read_tl_object(b)")
    elif res_t in ("Vector<string>", "vector<string>"):
        lines.append("        c_id = read_uint(b)")
        lines.append("        b.seek(b.tell() - 4)")
        lines.append("        if c_id == 0x1CB5C415:")
        lines.append("            return read_vector(b, read_string)")
        lines.append("        return read_tl_object(b)")
    elif res_t in ("Vector<bytes>", "vector<bytes>"):
        lines.append("        c_id = read_uint(b)")
        lines.append("        b.seek(b.tell() - 4)")
        lines.append("        if c_id == 0x1CB5C415:")
        lines.append("            return read_vector(b, read_bytes)")
        lines.append("        return read_tl_object(b)")
    elif res_t in ("bool", "Bool"):
        lines.append("        c_id = read_uint(b)")
        lines.append("        b.seek(b.tell() - 4)")
        lines.append("        if c_id == 0x997275B5:")
        lines.append("            read_uint(b)")
        lines.append("            return True")
        lines.append("        if c_id == 0xBC799737:")
        lines.append("            read_uint(b)")
        lines.append("            return False")
        lines.append("        return read_tl_object(b)")
    else:
        lines.append("        return read_tl_object(b)")
    lines.append("")

    return "\n".join(lines)


def write_generated_files(entries: List[TLEntry]):
    reserved_types = {"True", "Bool", "Int", "Long", "String", "Bytes", "Double", "Vector", "VectorInt", "VectorLong", "VectorString"}

    type_entries: Dict[str, TLEntry] = {}
    func_entries: Dict[str, TLEntry] = {}

    for e in entries:
        if e.section == "types" and e.class_name not in reserved_types:
            type_entries[e.class_name] = e
        elif e.section == "functions" and e.class_name not in reserved_types:
            func_entries[e.class_name] = e

    base_types = set()
    for e in type_entries.values():
        if e.base_class_name != "TLObject" and e.base_class_name != e.class_name and e.base_class_name not in reserved_types:
            base_types.add(e.base_class_name)

    # Write types/__init__.py
    types_file = RAW_DIR / "types" / "__init__.py"
    type_lines = [
        '"""',
        'Official Telegram TL Types for MTProto (Layer 229).',
        '"""',
        '',
        'from __future__ import annotations',
        '',
        'import io',
        'import struct',
        'from typing import Any, BinaryIO, Optional',
        '',
        'from aiogram.raw.core.primitives import (',
        '    TLObject,',
        '    read_bool,',
        '    read_bytes,',
        '    read_double,',
        '    read_int,',
        '    read_int128,',
        '    read_int256,',
        '    read_long,',
        '    read_string,',
        '    read_uint,',
        '    read_vector,',
        '    write_bool,',
        '    write_bytes,',
        '    write_double,',
        '    write_int,',
        '    write_int128,',
        '    write_int256,',
        '    write_long,',
        '    write_string,',
        '    write_uint,',
        '    write_vector,',
        ')',
        '',
    ]

    for base in sorted(base_types):
        type_lines.append(f"class {base}(TLObject):")
        type_lines.append("    pass")
        type_lines.append("")

    for c_name in sorted(type_entries.keys()):
        type_lines.append(generate_type_class(type_entries[c_name]))

    aliases = [
        "SentCode = AuthSentCode",
        "Authorization = AuthAuthorization",
        "ExportedAuthorization = AuthExportedAuthorization",
        "ExportedAuthorizationLegacy = AuthExportedAuthorization",
        "ResolvedPeer = ContactsResolvedPeer",
        "InputCheckPasswordSRP = InputCheckPasswordSrp",
        "PasswordKdfAlgoSHA256SHA256PBKDF2HMACSHA512 = PasswordKdfAlgoSha256Sha256Pbkdf2Hmacsha512iter100000Sha256ModPow",
        "SecurePasswordKdfAlgoPBKDF2HMACSHA512 = SecurePasswordKdfAlgoPbkdf2Hmacsha512iter100000",
        "SecurePasswordKdfAlgoSHA512 = SecurePasswordKdfAlgoSha512",
    ]
    type_lines.extend(aliases)
    type_lines.append("")

    types_file.write_text("\n".join(type_lines), encoding="utf-8")

    # Write functions/__init__.py
    funcs_file = RAW_DIR / "functions" / "__init__.py"
    func_lines = [
        '"""',
        'Official Telegram TL RPC Functions for MTProto (Layer 229).',
        '"""',
        '',
        'from __future__ import annotations',
        '',
        'import struct',
        'from typing import Any, BinaryIO, Optional',
        '',
        'from aiogram.raw.core.primitives import (',
        '    TLObject,',
        '    TLRequest,',
        '    read_bool,',
        '    read_bytes,',
        '    read_double,',
        '    read_int,',
        '    read_int128,',
        '    read_int256,',
        '    read_long,',
        '    read_string,',
        '    read_uint,',
        '    read_vector,',
        '    write_bool,',
        '    write_bytes,',
        '    write_double,',
        '    write_int,',
        '    write_int128,',
        '    write_int256,',
        '    write_long,',
        '    write_string,',
        '    write_uint,',
        '    write_vector,',
        ')',
        'from aiogram.raw.types import *',
        '',
    ]

    for c_name in sorted(func_entries.keys()):
        func_lines.append(generate_func_class(func_entries[c_name]))

    func_aliases = [
        "SendMessage = MessagesSendMessage",
        "SendMedia = MessagesSendMedia",
        "GetHistory = MessagesGetHistory",
        "GetFile = UploadGetFile",
        "SaveFilePart = UploadSaveFilePart",
        "SaveBigFilePart = UploadSaveBigFilePart",
        "ResolveUsername = ContactsResolveUsername",
        "GetNearestDc = HelpGetNearestDc",
        "SendCode = AuthSendCode",
        "ResendCode = AuthResendCode",
        "CancelCode = AuthCancelCode",
        "SignIn = AuthSignIn",
        "SignUp = AuthSignUp",
        "CheckPassword = AuthCheckPassword",
        "ImportBotAuthorization = AuthImportBotAuthorization",
        "ExportAuthorization = AuthExportAuthorization",
        "ImportAuthorization = AuthImportAuthorization",
        "LogOut = AuthLogOut",
        "GetPassword = AccountGetPassword",
        "GetUsers = UsersGetUsers",
        "GetFullUser = UsersGetFullUser",
        "EditMessage = MessagesEditMessage",
        "DeleteMessages = MessagesDeleteMessages",
        "ForwardMessages = MessagesForwardMessages",
    ]
    func_lines.extend(func_aliases)
    func_lines.append("")

    namespaces: Dict[str, Dict[str, str]] = {}
    for e in func_entries.values():
        if e.namespace:
            ns = e.namespace
            method = pascal_case(e.name)
            if ns not in namespaces:
                namespaces[ns] = {}
            namespaces[ns][method] = e.class_name

    for ns, methods_dict in sorted(namespaces.items()):
        func_lines.append(f"class {ns}:")
        for m_name, full_cls in sorted(methods_dict.items()):
            func_lines.append(f"    {m_name} = {full_cls}")
        func_lines.append("")

    funcs_file.write_text("\n".join(func_lines), encoding="utf-8")

    # Write all.py (registry)
    all_file = RAW_DIR / "all.py"
    all_lines = [
        '"""',
        'Central TL constructor registry and polymorphic reader (Layer 229).',
        '"""',
        '',
        'from __future__ import annotations',
        '',
        'import io',
        'import struct',
        'from typing import Any, BinaryIO',
        '',
        'from aiogram.raw.core.primitives import TLObject, read_uint',
        'from aiogram.raw.types import *',
        'import aiogram.raw.core.tl_core_types as core_types',
        '',
        'TL_REGISTRY: dict[int, type[TLObject]] = {',
        '    core_types.GzipPacked.ID: core_types.GzipPacked,',
        '    core_types.RpcResult.ID: core_types.RpcResult,',
        '    core_types.RpcError.ID: core_types.RpcError,',
        '    core_types.MsgsAck.ID: core_types.MsgsAck,',
        '    core_types.BadServerSalt.ID: core_types.BadServerSalt,',
        '    core_types.BadMsgNotification.ID: core_types.BadMsgNotification,',
        '    core_types.NewSessionCreated.ID: core_types.NewSessionCreated,',
        '    core_types.Pong.ID: core_types.Pong,',
        '    core_types.Ping.ID: core_types.Ping,',
        '    core_types.PingDelayDisconnect.ID: core_types.PingDelayDisconnect,',
        '    core_types.ResPQ.ID: core_types.ResPQ,',
        '    core_types.ServerDHParamsOk.ID: core_types.ServerDHParamsOk,',
        '    core_types.DhGenOk.ID: core_types.DhGenOk,',
    ]

    core_override_names = {
        "NewSessionCreated", "Pong", "Ping", "PingDelayDisconnect",
        "BadMsgNotification", "BadServerSalt", "MsgsAck", "ResPQ",
        "ServerDHParamsOk", "DhGenOk", "GzipPacked", "RpcResult", "RpcError"
    }

    for c_name in sorted(type_entries.keys()):
        if c_name not in core_override_names:
            all_lines.append(f'    {c_name}.ID: {c_name},')

    legacy_ids = {
        0x83314F16: "User",
        0xD3BC4B7A: "User",
        0x761453C7: "Message",
        0x2390FC44: "AuthSentCode",
        0x2EA2C0D4: "AuthAuthorization",
        0xCD0509A6: "AuthAuthorization",
        0xB9BC2B17: "AuthAuthorization",
        0x44747E9A: "AuthAuthorization",
        0x185B184F: "AuthPasswordRecovery",
        0xBBF2DDA0: "SecurePasswordKdfAlgoPbkdf2Hmacsha512iter100000",
    }
    for leg_id, leg_cls in legacy_ids.items():
        all_lines.append(f'    {hex(leg_id).upper()}: {leg_cls},')

    all_lines.extend([
        '}',
        '',
        '',
        'def read_tl_object(b: BinaryIO) -> Any:',
        '    """',
        '    Read constructor ID and instantiate corresponding TL object.',
        '    Handles GzipPacked, boxed vectors, booleans, and known TL types automatically.',
        '    """',
        '    c_id_bytes = b.read(4)',
        '    if not c_id_bytes or len(c_id_bytes) < 4:',
        '        return None',
        '    c_id = struct.unpack("<I", c_id_bytes)[0]',
        '',
        '    # Vector',
        '    if c_id == 0x1CB5C415:',
        '        count_bytes = b.read(4)',
        '        if len(count_bytes) < 4:',
        '            raise ValueError("Truncated vector length in read_tl_object")',
        '        count = struct.unpack("<I", count_bytes)[0]',
        '        if count > 100000:',
        '            raise ValueError(f"Vector count {count} exceeds sanity limit in read_tl_object")',
        '        return [read_tl_object(b) for _ in range(count)]',
        '',
        '    # boolTrue / boolFalse',
        '    if c_id == 0x997275B5:',
        '        return True',
        '    if c_id == 0xBC799737:',
        '        return False',
        '',
        '    if c_id == core_types.GzipPacked.ID:',
        '        decompressed = core_types.GzipPacked.read(b)',
        '        return read_tl_object(io.BytesIO(decompressed))',
        '',
        '    cls = TL_REGISTRY.get(c_id)',
        '    if cls is not None:',
        '        return cls.read(b)',
        '',
        '    offset = b.tell() - 4 if hasattr(b, "tell") else -1',
        '    remaining = -1',
        '    if isinstance(b, io.BytesIO):',
        '        remaining = len(b.getvalue()) - b.tell()',
        '',
        '    msg = (',
        '        f"Unknown TL constructor ID: {c_id:#010x} "',
        '        f"at stream offset {offset} (remaining payload: {remaining} bytes)"',
        '    )',
        '    raise ValueError(msg)',
        '',
    ])

    all_file.write_text("\n".join(all_lines), encoding="utf-8")
    print("Successfully generated aiogram/raw/types/__init__.py, aiogram/raw/functions/__init__.py, and aiogram/raw/all.py!")


def main():
    api_content, mtproto_content = fetch_and_cache_schema()
    entries = parse_tl_schema(api_content, mtproto_content)
    write_generated_files(entries)


if __name__ == "__main__":
    main()
