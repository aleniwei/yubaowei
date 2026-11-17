# Yubao Wei · Academic Portfolio B2

**Research Stories / Publications / Writing / CV / Contact**

**正式网站目标地址：** https://weiyubao.pages.dev/

这是用于 **GitHub → Cloudflare Pages 自动部署** 的完整网站仓库（repository），并非直接上传到 Cloudflare 的静态 ZIP。网站使用 Python 标准库构建，不依赖 Node.js、数据库、付费主题或第三方 Python 包。

## 1. 从这里开始

请先阅读 **`CLOUDFLARE_部署说明.md`**。它包含 GitHub 新建仓库、上传文件、Cloudflare 连接 GitHub 的逐步操作。

**Cloudflare Pages 构建设置：**

| 字段 | 填写值 |
|---|---|
| Project name | `weiyubao` |
| Production branch | `main` |
| Framework preset | `None` / `无` |
| Build command | `python3 build.py` |
| Build output directory | `site` |
| Root directory | 留空（仓库根目录） |

> `weiyubao.pages.dev` 只有在 Cloudflare 确实分配给你的 Pages 项目时才能访问；写进源代码不等于注册域名。以 Cloudflare 控制台显示的 Production URL 为准。

## 2. 修改网站内容

- `config/site.json`：姓名、单位、简介、联系方式、履历、网址（`domain`）。
- `content/research.json`：3 篇 Research Stories 的正文、摘要、插画。
- `content/publications.json`：真实论文列表，目前留空等待核实。
- `content/writing.json`：真实文章列表，目前留空等待核实。
- `assets/`：图片、SVG、CSS、JS。
- `build.py`：网页生成脚本。
- `site/`：已生成的网页，供预览和部署；每次构建会自动重建。
- `文本草案_EN_ZH.md`：中英文文案草稿。
- `图片素材说明.md`：图片替换与科研插画使用说明。

编辑 JSON 后保存、提交（Commit）到 GitHub `main` 分支，Cloudflare Pages 就会自动运行 `python3 build.py` 并发布 `site/`。

## 3. 本地预览（可选）

在 Windows 上直接打开 `site/index.html` 或双击 `PREVIEW_WINDOWS.bat`。

若安装了 Python 3，可运行：

```bash
python build.py
python verify_site.py
```

Windows 也可双击 `BUILD_WINDOWS.bat` 重新生成。

## 4. 研究诚信说明

网站中的胚胎图片是**概念插画，不是实验显微照片**；研究故事是可修改草案，不应作为已经发表的研究结果引用。论文与文章清单保持空白，避免杜撰文献。公开前请核对姓名、履历、联系信息和科研表述。

## 5. 重要：已经建立了 Direct Upload 项目？

Cloudflare Pages **不支持将现有 Direct Upload 项目直接转换为 Git integration 项目**。如果 `weiyubao` 已经是 Direct Upload 项目，请先阅读部署说明中的“已有项目”一节，不要直接删除已有项目。
