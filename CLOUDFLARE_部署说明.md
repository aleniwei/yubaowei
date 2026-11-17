# GitHub → Cloudflare Pages：一步一步部署

目标：**https://weiyubao.pages.dev/**

这是 **GitHub 仓库源代码 ZIP**，不是前一版用于 Cloudflare 拖放上传的网页 ZIP。两种 ZIP 用途不同。

## A. 在 GitHub 创建仓库

1. 确认右上角头像当前切换到你希望使用的 GitHub 账户，例如 `yubaowei`，而不是旧账户 `aleniwei`。
2. 打开 https://github.com/new 。
3. Repository name 填 `weiyubao-portfolio`（GitHub 仓库名称不决定 Cloudflare 域名）。
4. Visibility 选择 Public（也可以 Private）；**不要勾选**自动创建 README、.gitignore 或 License，避免首次上传冲突。
5. 点击 **Create repository**。
6. 下载并解压本 ZIP。进入解压后的目录，确保看到 `build.py`、`README.md`、`config/`、`content/`、`assets/`、`site/` 等。
7. 在 GitHub 新仓库中点击 **uploading an existing file** 或 **Add file → Upload files**，把解压后的**内容**（不是 ZIP 文件，也不是外层目录）上传；确保 `build.py` 和 `site/index.html` 都位于仓库正确路径。点击 **Commit changes**。
8. 默认分支应为 `main`。如果 GitHub 网页无法完整上传文件夹，可以改用 GitHub Desktop：把解压后的文件放进本地仓库目录，Commit 后 Push。

## B. 在 Cloudflare 创建 Git 连接项目

1. 登录 https://dash.cloudflare.com/ 。
2. 打开 **Workers & Pages → Create application → Pages → Connect to Git**（某些界面显示 Import an existing Git repository）。
3. 选择 **GitHub**，授权 Cloudflare Workers & Pages 访问包含 `weiyubao-portfolio` 的 GitHub 账户和仓库。
4. 选择 `yubaowei/weiyubao-portfolio`（如果你使用别的 GitHub 用户名，以实际仓库为准）。
5. **Project name** 填 `weiyubao`。注意：GitHub 仓库名可以是 `weiyubao-portfolio`，但 Cloudflare 项目名必须是 `weiyubao` 才可能得到 `weiyubao.pages.dev`。
6. **Production branch**：`main`。
7. **Framework preset**：`None`（无框架）。
8. **Build command**：`python3 build.py`。
9. **Build output directory**：`site`（不要填 `/site/index.html` 或 `.`）。
10. **Root directory**：留空，使用仓库根目录。
11. 点击 **Save and Deploy**，等待显示成功；从项目主页复制实际 **Production URL** 打开。

### 配置表（照填即可）

| Cloudflare 设置 | 填写 |
|---|---|
| Project name | `weiyubao` |
| Production branch | `main` |
| Framework preset | `None` |
| Build command | `python3 build.py` |
| Build output directory | `site` |
| Root directory | 留空 |

**切记：Cloudflare 项目名与 GitHub 仓库名不必相同。** 只有 Cloudflare 分配了该名称，`https://weiyubao.pages.dev/` 才会生效。

## C. 如果 Cloudflare 中已经存在 `weiyubao` 项目

请先在 Cloudflare 控制台查看项目类型、部署方式、Production URL：

- 如果它**已经连接 GitHub**：可在项目的 Git 设置里检查现有仓库关联与权限；通常不需要再建同名项目。
- 如果它是之前通过 ZIP **Direct Upload** 建立的项目：Cloudflare 不支持直接把它改为 Git integration。**不要立即删除。** 可选择：
  1. 另建一个 Git 集成项目，使用另一个 `*.pages.dev` 名称；或
  2. 确认已有部署可以备份、接受短暂中断后，再考虑删除旧项目、重新创建 `weiyubao` Git 集成项目。删除后能否重新取得相同名称需要以 Cloudflare 实际分配为准；不要假设必然可恢复。

如果你必须**保留原有 `weiyubao.pages.dev` 项目和地址**，还可以走 GitHub Actions + Wrangler 的持续部署路线，但需要额外配置 Cloudflare API Token 和 Account ID；本包默认使用更简单的 Cloudflare 原生 Git 集成。

## D. 上线后如何修改

1. 在 GitHub 打开 `config/site.json`，点击铅笔图标，修改个人简介等信息。
2. 点击 **Commit changes**，提交到 `main`。
3. Cloudflare 会自动重新构建并部署。进入 Cloudflare 项目的 **Deployments** 查看状态。
4. 修改研究故事：`content/research.json`；添加论文：`content/publications.json`；文章：`content/writing.json`。
5. 记得只发布已核实的论文与经过授权的科研图像。

## E. 常见故障

- **打不开网址**：先检查 Cloudflare 控制台实际 Production URL 是否与预期相同，以及 Deployments 是否成功。
- **Cloudflare 找不到 GitHub 仓库**：检查 Cloudflare GitHub App 的安装与授权是否选择了正确的 GitHub 账户及仓库。
- **构建失败**：检查 Build command 是否为 `python3 build.py`，Root directory 是否留空，Build output directory 是否为 `site`；在 Deployments → View details → Build log 查看错误。
- **显示 404**：检查仓库 `site/index.html` 是否存在，以及输出目录是不是 `site`。
- **修改了 JSON 但页面没更新**：确认更改已经 Commit 到生产分支 `main`，并查看 Cloudflare 最新部署是否成功。

## F. 官方参考

- https://developers.cloudflare.com/pages/get-started/git-integration/
- https://developers.cloudflare.com/pages/configuration/build-configuration/
- https://developers.cloudflare.com/pages/get-started/direct-upload/
