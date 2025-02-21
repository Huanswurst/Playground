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
    // 添加stream参数处理
    const stream = req.body.stream === true
    
    const response = await axios({
      method: 'post',
      url: 'https://ark.cn-beijing.volces.com/api/v3/chat/completions',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.ARK_API_KEY}`
      },
      data: {
        model: process.env.MODEL_ID,
        messages: req.body.messages,
        temperature: 0.7,
        stream: stream // 透传stream参数
      },
      responseType: stream ? 'stream' : 'json' // 动态设置响应类型
    })

    // 流式响应处理（保持原有逻辑）
    if (stream) {
      res.setHeader('Content-Type', 'text/event-stream')
      response.data.pipe(res)
      return
    }

    // 标准响应处理
    res.json({
      id: response.data.id,
      content: response.data.choices[0].message.content,
      usage: response.data.usage
    })
    
  } catch (error) {
    // 错误处理（保持原有逻辑）
  }
})

// 启动服务
app.listen(PORT, () => {
  console.log(`Proxy server running on port ${PORT}`)
})
