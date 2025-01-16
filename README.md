# 智能课堂管理系统

## 项目简介
本项目是一个基于Django和Vue.js的智能课堂管理系统，包含学生、教师和管理员三种角色，提供考勤管理、课程管理、数据统计等功能。

## 技术栈
- 前端：Vue 3 + Element Plus + Vite
- 后端：Django 5 + Django REST Framework
- 数据库：SQLite3
- 部署：Nginx + Gunicorn

## 环境要求
- Node.js >= 16.0.0
- Python >= 3.8
- pip >= 21.0.0

## 安装步骤

### 前端
```bash
cd src
npm install
```

### 后端
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
```

## 运行说明

### 开发环境
1. 启动后端服务
```bash
cd backend
python manage.py runserver 0.0.0.0:8000
```

2. 启动前端服务
```bash
cd src
npm run dev
```

3. 访问地址
- 前端：http://localhost:5173
- 后端API：http://localhost:8000/api/

### 生产环境
1. 构建前端
```bash
cd src
npm run build
```

2. 配置Nginx
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        root /path/to/dist;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

3. 启动Gunicorn
```bash
cd backend
gunicorn backend.wsgi:application -w 4 -b 127.0.0.1:8000
```

## API文档
访问 `/api/docs/` 查看Swagger API文档

## 贡献指南
1. Fork 本项目
2. 创建新的分支 (`git checkout -b feature/YourFeature`)
3. 提交修改 (`git commit -m 'Add some feature'`)
4. 推送分支 (`git push origin feature/YourFeature`)
5. 创建Pull Request

## 许可证
[MIT](LICENSE)
