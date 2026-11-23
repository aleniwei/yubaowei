# Yubao WEI — Hugo 网站源代码

目标域名：**https://yubaowei.pages.dev/**

本项目按你上传的 `Yubao.pptx` 制作，**六个网页正文均来自 PPT**；没有添加个人经历、论文或其他正文内容。顶部仅保留六个网页的导航，不显示顶部“Yubao WEI”；没有底部署名或页码。第六页横幅直接使用你 PPT 中的五国名胜拼贴图。

## 文件结构

- `hugo.toml`：网站域名、导航设置
- `content/_index.md`：Home（首页）正文
- `content/researches.md`：Researches 正文
- `content/publications.md`：Publications，**单栏长网页**
- `content/writings.md`：Writings 正文
- `content/humanities.md`：Humanities 正文
- `content/avocations.md`：Avocations 正文
- `static/images/`：从你 PPT 提取的六张横幅，WebP 格式
- `static/css/site.css`：统一字体、颜色、字号和排版
- `static/js/site.js`：长网页右侧的阅读进度条
- `layouts/`：Hugo 网站骨架，无须安装主题或 npm 包

## 首次发布到 GitHub / Cloudflare Pages

**重要：先备份当前 GitHub 仓库。** 如果它仍包含旧的 Python 建站程序，不要将新代码与旧代码混合使用。

1. 下载本源码 ZIP 并解压。
2. 将解压后的**全部文件及目录**上传到对应 GitHub 仓库的 **main** 分支，确保根目录有 `hugo.toml`；若仓库中是旧版网站，请替换旧版网站文件，而不是只新增 ZIP。
3. 进入 Cloudflare → Workers & Pages → 现有 Pages 项目 **yubaowei** → Settings → Build，将设置改为：
   - Framework preset：**Hugo**（或 None，只要下面两个参数正确）
   - Build command：**`hugo --gc --minify`**
   - Build output directory：**`public`**
   - Root directory：**留空**
   - Production branch：**main**
   - Environment variable：**`HUGO_VERSION` = `0.170.1`**（分别在 Production / Preview 配置，如使用预览）
4. 在 Cloudflare 的 Deployments 中重试/重新部署，确认 Production 部署成功。
5. 打开 **https://yubaowei.pages.dev/** 检查六个导航链接。

**注意：你之前使用的是 `python3 build.py`、输出 `site`。改成 Hugo 后，必须将它们改为 `hugo --gc --minify` 和 `public`。否则新网站不会正确发布。**

如果 Cloudflare 项目已连接到 GitHub，更新 main 分支后会自动开始构建；无需每次在 Cloudflare 中手动上传文件。

## 今后如何修改正文（最简单）

登录 GitHub → 进入 `content` → 选择某个 `.md` 文件 → 点击铅笔图标 → 修改段落或列表 → Commit changes。随后 Cloudflare 会自动重建。

Markdown 规则：

- `## 标题`：次级标题
- `### 标题`：小标题
- `- 内容`：列表条目
- 两个段落之间保留空行

如需修改全部页面的颜色、字体或正文大小，只改 `static/css/site.css` 开头的 `:root`：

- `--font`：统一字体，目前优先使用 Segoe UI / Microsoft YaHei / PingFang SC / Noto Sans 等系统字体
- `--body-size`：所有网页的正文字号
- `--body-line`：所有网页的正文行高
- `--purple`、`--purple-deep`、`--paper`：主色与背景

若要更换顶部配图，把新图片放进 `static/images`，更新对应 `.md` 文件开头的 `banner` 路径即可。

## 本地预览（可选）

安装 Hugo 后，在项目根目录执行：

```sh
hugo server -D
```

浏览器访问 `http://localhost:1313`。要生成静态文件，运行：

```sh
hugo --gc --minify
```

Hugo 会将网站放在 `public/` 文件夹；它是构建产物，不需要上传到 GitHub。

## 关于文字与页面

- 网页的六个标签、原稿中的条目、正文、重复出现的“Professional Memberships”等均按 PPT 保留。
- 原 PPT 中 Writings 的小标题写作“P Memberships”，此处**原样保留**，避免擅自改动；如这是打字错误，可日后在 `content/writings.md` 中自行改为 `Memberships`。
- Publications 中的 `Presentations (continued)` 也按 PPT 原样保留，但已改成纵向单栏。
- 页面的高度由文字量自动决定，不再固定与 PPT 相同。
- 第六页五国名胜图为你 PPT 中的概念拼贴图，而不是实际个人旅行照片。
