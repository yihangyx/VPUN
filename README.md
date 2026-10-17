# JumperVPN 自动注册工具

基于 beeinbox 临时邮箱的 JumperVPN 自动注册网页应用，部署在 Vercel 上。

## 功能

- ✅ 自动创建 beeinbox 临时邮箱
- ✅ 自动提取邮箱地址
- ✅ 自动接收并提取验证码
- ✅ 自动完成 VPN 注册流程
- ✅ 实时显示运行日志

## 部署到 Vercel

### 方法一：直接导入 GitHub

1. 把这个项目推送到 GitHub 仓库
2. 打开 [Vercel](https://vercel.com)，点击 "Add New Project"
3. 选择你的仓库，点击 "Deploy"
4. 等待部署完成，访问你的域名即可

### 方法二：Vercel CLI

```bash
npm i -g vercel
vercel
```

## 项目结构

```
├── api/
│   ├── beeinbox/
│   │   └── [...path].js    # beeinbox 反向代理
│   └── vpn/
│       └── [...path].js    # JumperVPN API 代理
├── index.html               # 主页面
└── vercel.json              # Vercel 配置
```

## 工作原理

1. **反向代理 beeinbox**：通过 `/api/beeinbox/*` 代理 beeinbox.com 的所有请求，解决跨域问题
2. **iframe 嵌入**：在 iframe 中加载代理后的 beeinbox，完整运行所有 JS 和反爬验证
3. **自动提取**：前端 JS 定时从 iframe 中提取邮箱地址和验证码
4. **自动注册**：调用 `/api/vpn/*` 代理完成 JumperVPN 的注册流程

## 注意事项

- beeinbox 有频率限制，短时间内频繁注册会被限制
- 验证码提取是自动的，如果提取失败可以手动从右侧 iframe 中查看
- 所有数据都在浏览器端处理，不会保存任何隐私信息
