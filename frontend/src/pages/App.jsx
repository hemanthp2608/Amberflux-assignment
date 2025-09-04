import React, { useState, useEffect } from 'react'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export default function App() {
  const [token, setToken] = useState('')
  const [email, setEmail] = useState('')
  const [name, setName] = useState('')
  const [password, setPassword] = useState('')
  const [assignments, setAssignments] = useState([])
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')

  async function register() {
    const r = await fetch(`${API_BASE}/api/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, name, password }),
    })
    if (!r.ok) alert('Register failed')
    else alert('Registered! Now login.')
  }

  async function login() {
    const body = new URLSearchParams()
    body.append('username', email)
    body.append('password', password)
    const r = await fetch(`${API_BASE}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body
    })
    const data = await r.json()
    if (r.ok) setToken(data.access_token)
    else alert('Login failed')
  }

  async function loadAssignments() {
    const r = await fetch(`${API_BASE}/api/assignments`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    const data = await r.json()
    if (r.ok) setAssignments(data)
  }

  async function createAssignment() {
    const r = await fetch(`${API_BASE}/api/assignments`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify({ title, description })
    })
    if (r.ok) loadAssignments()
  }

  useEffect(() => {
    if (token) loadAssignments()
  }, [token])

  return (
    <div style={{maxWidth: 900, margin: '2rem auto', fontFamily: 'system-ui'}}>
      <h1>Amberflux Assignment</h1>
      <section style={{display: 'grid', gap: 8, gridTemplateColumns: 'repeat(3, 1fr)'}}>
        <input placeholder="email" value={email} onChange={e=>setEmail(e.target.value)} />
        <input placeholder="name" value={name} onChange={e=>setName(e.target.value)} />
        <input placeholder="password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
        <button onClick={register}>Register</button>
        <button onClick={login}>Login</button>
      </section>
      {token && (
        <>
          <h2>Create Assignment</h2>
          <section style={{display:'flex', gap:8}}>
            <input placeholder="title" value={title} onChange={e=>setTitle(e.target.value)} />
            <input placeholder="description" value={description} onChange={e=>setDescription(e.target.value)} />
            <button onClick={createAssignment}>Create</button>
          </section>
          <h2>Assignments</h2>
          <ul>
            {assignments.map(a => (<li key={a.id}>
              <strong>{a.title}</strong> — {a.description}
            </li>))}
          </ul>
        </>
      )}
      <p style={{marginTop: 24}}><em>Set VITE_API_BASE to your backend URL if not localhost:8000.</em></p>
    </div>
  )
}
