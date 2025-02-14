// server.js
import express from 'express'
import cors from 'cors'
import axios from 'axios'

const app = express()
const PORT = 3001

// 配置中间件
app.use(express.json())
app.use(cors({
  origin: 'https://www.huanswurst.top' // 替换为你的前端域名
}))

// 代理端点
app.post('/api/chat', async (req, res) => {
  try {
    const response = await axios({
      method: 'post',
      url: 'https://ark.cn-beijing.volces.com/api/v3/chat/completions',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.ARK_API_KEY}`
      },
      data: {
        ...req.body,
        model: "ep-20250214164658-m9cgv" // 你的模型ID
      }
    })
    
    res.json(response.data)
  } catch (error) {
    res.status(500).json({
      error: 'API请求失败',
      details: error.message
    })
  }
})

// 启动服务
app.listen(PORT, () => {
  console.log(`Proxy server running on port ${PORT}`)
})
