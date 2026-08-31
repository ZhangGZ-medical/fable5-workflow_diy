#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
inventory_skills.py — 本地技能全量盘点（fable5-workflow_diy v3.0 阶段2 专用）

背景：本地技能规模大（数百个顶层目录 + 嵌套子技能，如 LabClaw/skills/literature/...），
逐个读 SKILL.md 会爆上下文。本脚本只解析每个 SKILL.md 的 YAML frontmatter，
生成轻量索引（skill_id / name / description / version / source），供按需精准加载。

用法：
  python inventory_skills.py                        # 全量 Markdown 索引（按命名空间分组）
  python inventory_skills.py --query "pdf ocr"      # 关键词过滤（AND，匹配 id+name+desc）
  python inventory_skills.py --query "docx" --compact
  python inventory_skills.py --json                 # JSON 输出（供程序消费）
  python inventory_skills.py --top-level-only       # 只看顶层技能（跳过嵌套子技能）
  python inventory_skills.py --limit 50             # 限制条数
  python inventory_skills.py --save <path.md>       # 落盘

依赖：无（纯标准库，不依赖 PyYAML）
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

# ---------- 路径解析 ----------

def default_roots():
    roots = []
    home = Path.home()
    user_skills = home / ".workbuddy" / "skills"
    if user_skills.is_dir():
        roots.append(("user", user_skills))
    # 项目级技能（当前工作目录）
    proj = Path.cwd() / ".workbuddy" / "skills"
    if proj.is_dir():
        roots.append(("project", proj))
    # 本地技能市场
    market = home / ".workbuddy" / "skills-marketplace" / "skills"
    if market.is_dir():
        roots.append(("marketplace", market))
    return roots


# ---------- frontmatter 解析（极简 YAML 子集） ----------

def parse_frontmatter(text):
    """解析 SKILL.md 头部 --- ... --- 的 YAML frontmatter（子集：key: value / > / | / [a,b]）"""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end].strip("\n")
    data = {}
    key = None
    buf = []
    for line in block.split("\n"):
        m = re.match(r"^([A-Za-z_][\w\-]*):\s*(.*)$", line)
        if m:
            if key is not None:
                data[key] = _finalize(buf)
            key = m.group(1).strip()
            val = m.group(2).strip()
            buf = [val] if val not in (">", "|", ">-", "|-", "") else []
        elif key is not None:
            buf.append(line.strip())
    if key is not None:
        data[key] = _finalize(buf)
    return data


def _finalize(buf):
    if not buf:
        return ""
    if len(buf) == 1:
        return buf[0].strip().strip('"').strip("'")
    # 多行（folded > 或 literal |）：折叠为单行
    return " ".join(x for x in buf if x).strip()


# ---------- 扫描 ----------

def body_abstract(text):
    """frontmatter 缺失 description 时：从正文抽取 H1 + 首段 / 触发词 作为摘要"""
    # 去掉 frontmatter
    body = text
    if body.startswith("---"):
        end = body.find("\n---", 3)
        if end != -1:
            body = body[end + 4:]
    h1 = ""
    para = ""
    trigger = ""
    for line in body.split("\n"):
        s = line.strip()
        if not s:
            continue
        if s.startswith("# ") and not h1:
            h1 = s[2:].strip()
            continue
        if s.startswith("#") or s.startswith("---") or s.startswith("```") or s.startswith("|"):
            continue
        if not para:
            para = s.lstrip("-").strip()
        if "触发词" in s and not trigger:
            trigger = s
    parts = [p for p in (h1, para) if p]
    if trigger and len(trigger) < 120:
        parts.append(trigger)
    return " / ".join(parts)


def scan(roots, max_depth=6, top_level_only=False):
    items = []
    seen = set()
    for source, root in roots:
        for md in root.rglob("SKILL.md"):
            rel = md.parent.relative_to(root)
            depth = len(rel.parts)
            if depth == 0:
                continue
            if top_level_only and depth > 1:
                continue
            if depth > max_depth:
                continue
            try:
                text = md.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            fm = parse_frontmatter(text)
            # skill_id 沿用平台约定：路径分隔符转冒号
            skill_id = ":".join(rel.parts)
            if skill_id in seen:
                continue
            seen.add(skill_id)
            # 描述回退链：description → summary → (title + read_when) → 正文摘要
            desc = (fm.get("description") or "").replace("\n", " ")
            if not desc.strip():
                # 注意：join 两个空串会得到 " "（truthy），必须先过滤再拼接
                extra = " ".join(x for x in (fm.get("summary"), fm.get("title")) if x).strip()
                desc = extra or body_abstract(text)
            desc = re.sub(r"\s+", " ", desc).strip()
            # disable-model-invocation: true → 只能用户手动触发，不可自动调度
            auto = str(fm.get("disable-model-invocation", "false")).lower() != "true"
            items.append({
                "skill_id": skill_id,
                "name": fm.get("name") or rel.parts[-1],
                "description": desc,
                "version": fm.get("version") or "",
                "source": source,
                "path": str(md),
                "nested": depth > 1,
                "auto_invocable": auto,
            })
    return items


def match(items, query, limit=None):
    if not query:
        return items[:limit] if limit else items
    toks = [t.lower() for t in query.split() if t]
    hits = []
    for it in items:
        hay = f"{it['skill_id']} {it['name']} {it['description']} {it['path']}".lower()
        if all(t in hay for t in toks):
            hits.append(it)
    # 命中词越多越靠前；顶层优先
    def score(it):
        hay = f"{it['skill_id']} {it['name']} {it['description']}".lower()
        s = sum(hay.count(t) for t in toks)
        if it["skill_id"].lower().startswith(toks[0]):
            s += 5
        if not it["nested"]:
            s += 2
        return -s
    hits.sort(key=score)
    return hits[:limit] if limit else hits


# ---------- 输出 ----------

def render_md(items, query=None):
    total = len(items)
    out = []
    out.append(f"# 本地技能索引（{total} 个）")
    if query:
        out.append(f"> 过滤条件：`{query}`")
    out.append("")
    by_src = {}
    for it in items:
        by_src.setdefault(it["source"], []).append(it)
    tag = {"user": "已安装(用户级)", "project": "已安装(项目级)", "marketplace": "本地市场(可复制安装)"}
    for src in ("user", "project", "marketplace"):
        group = by_src.get(src, [])
        if not group:
            continue
        out.append(f"## {tag.get(src, src)} — {len(group)} 个")
        out.append("")
        out.append("| skill_id | 说明 | 版本 |")
        out.append("|---|---|---|")
        for it in group:
            desc = it["description"] or "—"
            if len(desc) > 160:
                desc = desc[:160] + "…"
            desc = desc.replace("|", "\\|")
            ver = it["version"] or "—"
            sid = f"`{it['skill_id']}`"
            if not it.get("auto_invocable", True):
                sid += " ⚠仅手动"
            out.append(f"| {sid} | {desc} | {ver} |")
        out.append("")
    return "\n".join(out)


def render_compact(items, query=None):
    out = [f"# 本地技能索引（{len(items)} 个）" + (f" — 过滤：`{query}`" if query else ""), ""]
    for it in items:
        d = re.sub(r"\s+", " ", it["description"])[:110]
        mark = "  [嵌套]" if it["nested"] else ""
        if not it.get("auto_invocable", True):
            mark += "  [仅手动触发]"
        out.append(f"- `{it['skill_id']}` ({it['source']}){mark}: {d}")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="本地技能全量盘点")
    ap.add_argument("--query", "-q", help="关键词过滤（空格分隔，AND）")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    ap.add_argument("--compact", action="store_true", help="紧凑列表输出")
    ap.add_argument("--top-level-only", action="store_true", help="只列顶层技能")
    ap.add_argument("--limit", type=int, default=None, help="限制条数")
    ap.add_argument("--save", help="输出到文件（默认 stdout）")
    ap.add_argument("--roots", nargs="*", help="自定义扫描根目录（覆盖默认）")
    args = ap.parse_args()

    if args.roots:
        roots = [("custom", Path(r)) for r in args.roots if Path(r).is_dir()]
    else:
        roots = default_roots()

    if not roots:
        print("未找到任何技能根目录", file=sys.stderr)
        sys.exit(1)

    items = scan(roots, top_level_only=args.top_level_only)
    items = match(items, args.query, args.limit)
    items.sort(key=lambda x: (x["source"] != "user", x["skill_id"].lower()))

    if args.json:
        text = json.dumps(items, ensure_ascii=False, indent=2)
    elif args.compact:
        text = render_compact(items, args.query)
    else:
        text = render_md(items, args.query)

    if args.save:
        Path(args.save).write_text(text, encoding="utf-8")
        print(f"已写入 {args.save}（{len(items)} 条）")
    else:
        print(text)


if __name__ == "__main__":
    main()
