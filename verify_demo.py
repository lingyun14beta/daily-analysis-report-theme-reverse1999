"""验证 demo 模板仓库：Jinja2 语法 + 运行时渲染 + 安装器端到端（打包→安装→卸载）。

用法:
    python verify_demo.py [模板名] [插件仓库路径]

模板名默认为 gda_reverse_1999，也可通过环境变量 TPL_NAME 指定；
插件仓库路径也可通过环境变量 PLUGIN_ROOT 指定。
不指定插件仓库路径时仅执行模板自身的语法与渲染校验，跳过安装器端到端部分。
"""
import io
import json
import os
import sys
import tempfile
import zipfile
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = Path(__file__).resolve().parent

# 位置参数：能被识别为模板目录名的作为模板名，其余作为插件仓库路径
_tpl_name = ""
_plugin_arg = ""
for arg in sys.argv[1:]:
    if not _tpl_name and (ROOT / arg / "image_template.html").is_file():
        _tpl_name = arg
    elif not _plugin_arg:
        _plugin_arg = arg

TPL_NAME = _tpl_name or os.environ.get("TPL_NAME", "gda_reverse_1999")
TPL = ROOT / TPL_NAME
if not TPL.is_dir():
    raise SystemExit(f"模板目录不存在: {TPL}")
PLUGIN_ROOT = _plugin_arg or os.environ.get("PLUGIN_ROOT", "")

# 1) Jinja2 语法检查
env = Environment(
    loader=FileSystemLoader(str(TPL)),
    autoescape=True,
    trim_blocks=True,
    lstrip_blocks=True,
)
for f in sorted(TPL.glob("*.html")):
    env.parse(f.read_text(encoding="utf-8"))
    print(f"[syntax OK] {f.name}")

# 2) 运行时渲染检查（StrictUndefined：任何变量缺失/类型错误立即抛错）
rt_env = Environment(
    loader=FileSystemLoader(str(TPL)),
    autoescape=True,
    trim_blocks=True,
    lstrip_blocks=True,
    undefined=StrictUndefined,
)
common = {
    "hide_user_names": False,
    "t2i_font_source": "Mainland",
    "t2i_google_fonts_mirror": "https://fonts.googleapis.com",
    "t2i_gstatic_mirror": "https://fonts.gstatic.com",
    "t2i_atri_font_mirror": "",
}
sub_ctx = {
    "topics": [
        {
            "index": 1,
            "topic": {"topic": "测试话题"},
            "contributors": "小明、小红",
            "detail": "这是<b>详情</b>（含头像）",
        }
    ],
    "titles": [
        {
            "name": "小明",
            "title": "话题王",
            "mbti": "ENFP",
            "reason": "理由文本",
            "avatar_data": "https://example.com/a.png",
            "profile_display": "ENFP",
        }
    ],
    "quotes": [
        {
            "content": "今天真开心",
            "sender": "小红",
            "reason": "这是<b>锐评</b>",
            "avatar_url": "https://example.com/q.png",
        }
    ],
    "chart_data": [{"hour": i, "count": i, "percentage": i * 4} for i in range(24)],
    "title": "群聊质量",
    "subtitle": "锐评",
    "summary": "质量总结文本",
    "dimensions": [{"name": "活跃度", "percentage": 80, "comment": "很好"}],
}
topics_html = rt_env.get_template("topic_item.html").render(**common, **sub_ctx)
titles_html = rt_env.get_template("user_title_item.html").render(**common, **sub_ctx)
quotes_html = rt_env.get_template("quote_item.html").render(**common, **sub_ctx)
hourly_chart_html = rt_env.get_template("activity_chart.html").render(
    **common, **sub_ctx
)
chat_quality_html = rt_env.get_template("chat_quality_item.html").render(
    **common, **sub_ctx
)
main_ctx = {
    **common,
    "topics_html": topics_html,
    "titles_html": titles_html,
    "quotes_html": quotes_html,
    "hourly_chart_html": hourly_chart_html,
    "chat_quality_html": chat_quality_html,
    "message_count": 100,
    "participant_count": 20,
    "total_characters": 3000,
    "emoji_count": 10,
    "most_active_period": "20:00-22:00",
    "current_date": "2026年08月01日",
    "current_datetime": "2026-08-01 20:00:00",
    "total_tokens": 1000,
    "prompt_tokens": 500,
    "completion_tokens": 500,
}
for name, out in {
    "image_template.html": None,
    "html_template.html": None,
}.items():
    html = rt_env.get_template(name).render(**main_ctx)
    assert "暴雨观测档案" in html and "时代回声" in html and "时间回响" in html
    assert "20:00-22:00" in html and "ARCHIVE SEALED" in html
    print(f"[render OK] {name} ({len(html)} bytes)")

# 隐私回归：模板负责的标题名和金句发送者应使用脱敏文案。
private_ctx = {**main_ctx, "hide_user_names": True}
private_titles = rt_env.get_template("user_title_item.html").render(**private_ctx, **sub_ctx)
private_quotes = rt_env.get_template("quote_item.html").render(**private_ctx, **sub_ctx)
assert "神秘群友" in private_titles and "小明" not in private_titles
assert "神秘群友" in private_quotes and "小红" not in private_quotes and "阿伟" not in private_quotes
print("[privacy OK] title and quote names are hidden")

if not PLUGIN_ROOT or not (Path(PLUGIN_ROOT) / "src").is_dir():
    print(
        "[skip] 未指定插件仓库路径，跳过安装器端到端检查。\n"
        "       用法: python verify_demo.py <插件仓库路径>  （或设置环境变量 PLUGIN_ROOT）",
        file=sys.stderr,
    )
    sys.exit(0)

sys.path.insert(0, PLUGIN_ROOT)

# 与插件 tests/conftest.py 一致的 astrbot mock（本机未安装 astrbot 包）
import logging  # noqa: E402
import types  # noqa: E402

if "astrbot.api" not in sys.modules:
    astrbot_module = types.ModuleType("astrbot")
    astrbot_api_module = types.ModuleType("astrbot.api")
    astrbot_star_module = types.ModuleType("astrbot.api.star")

    class StarTools:  # noqa: D101
        pass

    astrbot_api_module.logger = logging.getLogger("astrbot-demo")
    astrbot_api_module.AstrBotConfig = dict
    astrbot_star_module.StarTools = StarTools
    astrbot_module.api = astrbot_api_module
    sys.modules.setdefault("astrbot", astrbot_module)
    sys.modules.setdefault("astrbot.api", astrbot_api_module)
    sys.modules.setdefault("astrbot.api.star", astrbot_star_module)

from src.infrastructure.reporting.template_installer import (  # noqa: E402
    install_template_from_zip,
    uninstall_template,
)

# 2) 打包 zip（模拟仓库下载后的结构：外层 <模板名>/）
buf = io.BytesIO()
with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
    for f in sorted(TPL.rglob("*")):
        if f.is_file():
            zf.write(f, f.relative_to(ROOT).as_posix())

# 3) 安装
with tempfile.TemporaryDirectory() as tmp:
    store = Path(tmp) / "store"
    res = install_template_from_zip(
        buf.getvalue(),
        store_dir=store,
        source="url",
        source_url="https://github.com/lingyun14beta/daily-analysis-report-theme-reverse1999",
    )
    print(f"[install] {json.dumps(res, ensure_ascii=False)}")
    assert res["name"] == TPL_NAME, res["name"]
    assert res["has_image"] and res["has_html"]
    tpl_meta = TPL / "template.json"
    if tpl_meta.is_file():
        expected_label = json.loads(tpl_meta.read_text(encoding="utf-8"))["name"]
        assert res["label"] == expected_label, (res["label"], expected_label)
    installed_dir = store / TPL_NAME
    assert (installed_dir / ".tpl_installed.json").is_file()
    assert {f.name for f in installed_dir.glob("*.html")} == {
        "image_template.html", "html_template.html", "topic_item.html",
        "user_title_item.html", "quote_item.html", "activity_chart.html",
        "chat_quality_item.html",
    }

    # 4) 卸载
    res2 = uninstall_template(TPL_NAME, store_dir=store)
    print(f"[uninstall] {res2}")
    assert res2["removed"] is True
    assert not installed_dir.exists()

print("ALL OK")
