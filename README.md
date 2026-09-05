# 群聊日常分析 · 报告模板仓库（暴雨观测档案 Reverse: 1999）

本仓库是 [astrbot_plugin_qq_group_daily_analysis](https://github.com/SXP-Simon/astrbot_plugin_qq_group_daily_analysis) 的报告视觉模板仓库，可以作为自定义模板仓库的起点。

内置模板：**`gda_reverse_1999`（暴雨观测档案 Reverse: 1999）**。这是一个以《重返未来：1999》角色和世界观贯穿的连续场景长图：维尔汀、角色观测员、神秘学家、金句剧场角色与十四行诗依次进入画面。暗夜暴雨、浅金潮汐、米白时代、深绿登记册、猩红结论构成五段不同的游戏场景，而非重复的报告卡片。

> 预览：
> ![暴雨观测档案预览图](assets/gda_reverse_1999-demo-thumb.jpg)
>
> 完整长图见 [assets/gda_reverse_1999-demo.jpg](assets/gda_reverse_1999-demo.jpg)。

> 图片文件说明：
> - `assets/gda_reverse_1999-demo-thumb.jpg`：README 展示缩略图。
> - `assets/gda_reverse_1999-demo.jpg`：完整长图预览。
> - `gda_reverse_1999/preview.jpg`：随模板打包，供 QQ `/查看模板` 与 WebUI 画廊显示。
>
> 三者均由 `generate_preview.py` 一次生成。

## 一键安装

在插件 Web 控制台的配置页，点击模板选择器旁的“安装模板”，在 GitHub 链接页签填写：

```
https://github.com/lingyun14beta/daily-analysis-report-theme-reverse1999
```

插件会自动下载源码、识别 `gda_reverse_1999/` 模板目录并安装，无需重启机器人。也可以下载仓库 ZIP 后，在“安装模板 → 上传 zip”中直接上传。

## 目录结构

```
daily-analysis-report-theme/
├── README.md
└── gda_reverse_1999/
    ├── image_template.html      # 长图报告主骨架
    ├── html_template.html       # 独立网页主骨架
    ├── topic_item.html          # 话题记录
    ├── user_title_item.html     # 神秘学家登记卡
    ├── quote_item.html          # 金句摘录
    ├── activity_chart.html      # 时间裂隙活跃图
    ├── chat_quality_item.html   # 观测结论
    ├── template.json            # 模板展示元信息
    └── preview.jpg              # 随包预览图
```

## 视觉设计

模板的视觉变量位于 `gda_reverse_1999/image_template.html` 顶部：

```css
:root {
    --mist: #e8ece8;       /* 雾灰背景 */
    --paper: #f7f6f0;      /* 档案纸面 */
    --paper-deep: #edede4; /* 摘录与数据底色 */
    --ink: #243936;        /* 深墨绿正文 */
    --muted: #71817d;      /* 次级文字 */
    --gold: #ae8950;       /* 旧金索引和时间线 */
    --red: #ad483e;        /* 暴雨红：峰值与警示 */
    --line: #c9d0c9;       /* 档案分隔线 */
}
```

页面由以下节奏构成：

- 暗夜首屏：维尔汀与雨幕、倒数时刻一起构成主视觉。
- 时间潮汐：角色陪同活跃图，以浅金和雨后灰绿呈现全天节奏。
- 时代回声：角色切入话题区，内容沿场景内的时间线展开。
- 神秘学家群像：深绿场景承载群友画像，像一页被保留下来的登记册。
- 金句剧场与猩红结案：角色分别参与摘录与最终质量判断，结束整段观测。

## 渲染变量契约

主骨架接收 `topics_html`、`titles_html`、`quotes_html`、`hourly_chart_html`、`chat_quality_html` 五个 HTML 片段，以及 `message_count`、`participant_count`、`total_characters`、`emoji_count`、`most_active_period`、`current_date`、`current_datetime`、`total_tokens` 等统计字段。

子模块分别接收 `topics`、`titles`、`quotes`、`chart_data` 与 `title`、`subtitle`、`dimensions`、`summary`。完整变量表见插件仓库的 [REPORT_TEMPLATE_GUIDE](https://github.com/SXP-Simon/astrbot_plugin_qq_group_daily_analysis/blob/main/docs/REPORT_TEMPLATE_GUIDE.md#3-渲染变量契约)。

## 自检与预览

```bash
# 校验 Jinja2 语法与 StrictUndefined 渲染
python verify_demo.py gda_reverse_1999

# 生成完整图、README 缩略图与随包预览图
python generate_preview.py gda_reverse_1999
```

## 图片资源

人物立绘来自《重返未来：1999》官方网站 `https://re.bluepoch.com` 的公开静态资源，模板运行时使用绝对 URL：

- 维尔汀主视觉：`https://re.bluepoch.com/home/img/role/2.png`
- 十四行诗观测结论：`https://re.bluepoch.com/home/img/role/3.png`

资源版权归深蓝互动（Bluepoch）所有，仅供自用与演示；用于商业分发时应更换为已获授权的素材。预览生成脚本会将官网地址替换为 `assets/gda_reverse_1999/art/` 中的本地副本，以保证截图稳定；模板文件本身始终保留官网绝对链接。

## 许可

MIT，可自由复制修改。
