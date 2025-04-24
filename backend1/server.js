require('dotenv').config()
const express = require('express')
const cors = require('cors')
const app = express()
const authRoutes = require('./routes/auth')

app.use(cors())
app.use(express.json())

app.use('/api', authRoutes)

app.listen(3000, () => {
  console.log('Auth API running on http://localhost:3000')
})
