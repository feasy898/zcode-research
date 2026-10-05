# -*- coding: utf-8 -*-
"""Check: is the oracle docx rerun-vs-backup byte diff only zip timestamps?"""
import zipfile, hashlib
BASE = r"D:\workspace\zcode研究\skillfactory\v3\assets\office-templates"
BAK  = r"D:\workspace\zcode研究\_tmp_ab1_rep2\backup2"
for T in ["周报", "请示函", "会议通知", "工作总结"]:
    za = zipfile.ZipFile(rf"{BAK}\oracle_out\{T}\case1\文书.docx")
    zb = zipfile.ZipFile(rf"{BASE}\oracle\out\{T}\case1\文书.docx")
    na = {i.filename: i.date_time for i in za.infolist()}
    nb = {i.filename: i.date_time for i in zb.infolist()}
    cd = [n for n in sorted(set(na) & set(nb))
          if hashlib.sha256(za.read(n)).hexdigest() != hashlib.sha256(zb.read(n)).hexdigest()]
    to = [n for n in sorted(set(na) & set(nb)) if na[n] != nb[n]]
    print(f"-- {T}: names_equal={set(na) == set(nb)} content_diff={cd} time_only={len(to)}")
