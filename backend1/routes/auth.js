const express = require('express')
const router = express.Router()
const db = require('../db')
const bcrypt = require('bcryptjs')
const jwt = require('jsonwebtoken')

const JWT_SECRET = process.env.JWT_SECRET

// Register
router.post('/register', async (req, res) => {
  const { email, password } = req.body
  if (!email || !password) return res.status(400).json({ message: 'Email and password required' })

  const hashed = await bcrypt.hash(password, 10)

  const stmt = `INSERT INTO users (email, password) VALUES (?, ?)`
  db.run(stmt, [email, hashed], function (err) {
    if (err) return res.status(400).json({ message: 'User already exists' })
    res.status(201).json({ id: this.lastID })
  })
})

// Login
router.post('/login', (req, res) => {
  const { email, password } = req.body
  db.get(`SELECT * FROM users WHERE email = ?`, [email], async (err, user) => {
    if (err || !user) return res.status(401).json({ message: 'Invalid credentials' })

    const match = await bcrypt.compare(password, user.password)
    if (!match) return res.status(401).json({ message: 'Invalid credentials' })

    const token = jwt.sign({ id: user.id, email: user.email }, JWT_SECRET, { expiresIn: '1d' })
    res.json({ token })
  })
})

// Profile (Optional)
router.get('/user-profile', require('../middleware/authMiddleware'), (req, res) => {
  res.json({ user: req.user })
})

module.exports = router
