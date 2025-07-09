// src/pages/Login.jsx

import React, { useState } from 'react';
import {
  Box,
  Button,
  TextField,
  Typography,
  IconButton,
  Link
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';

// Base API URL dal .env
const API_URL = import.meta.env.VITE_API_URL;

export default function LoginPage({ onLogin, onClose, onSwitchToRegister }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setError('');
    if (!email || !password) {
      setError('Inserisci email e password');
      return;
    }

    setLoading(true);
    try {
      // POST form-encoded a /auth/login
      const form = new URLSearchParams();
      form.append('username', email);
      form.append('password', password);

      const loginRes = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: form.toString(),
      });

      if (!loginRes.ok) {
        setError('Login Fallito');
        setLoading(false);
        return;
      }

      const { access_token: token } = await loginRes.json();
      localStorage.setItem('access_token', token);

      // Recupero profilo utente
      const meRes = await fetch(`${API_URL}/users/me`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!meRes.ok) {
        setError('Impossibile recuperare profilo');
        setLoading(false);
        return;
      }

      const userData = await meRes.json();
      onLogin(userData, token);
    } catch {
      setError('Login Fallito');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      component="form"
      onSubmit={e => {
        e.preventDefault();
        handleSubmit();
      }}
      autoComplete="off"
      sx={{
        position: 'relative',
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        px: 2,
        bgcolor: 'rgba(0, 0, 0, 0.5)',
      }}
    >
      {onClose && (
        <IconButton
          onClick={onClose}
          sx={{ position: 'absolute', top: 16, right: 16, color: '#fff' }}
          size="large"
        >
          <CloseIcon />
        </IconButton>
      )}

      <Typography variant="h4" sx={{ mb: 3, fontWeight: 700, color: '#fff' }}>
        Accedi a DataDash
      </Typography>

      <TextField
        label="Email"
        type="email"
        value={email}
        onChange={e => setEmail(e.target.value)}
        fullWidth
        autoComplete="off"
        sx={{ maxWidth: 360, mb: 2, bgcolor: '#fff', borderRadius: 1 }}
      />
      <TextField
        label="Password"
        type="password"
        value={password}
        onChange={e => setPassword(e.target.value)}
        fullWidth
        autoComplete="new-password"
        sx={{ maxWidth: 360, mb: 2, bgcolor: '#fff', borderRadius: 1 }}
      />

      {error && (
        <Typography color="error" sx={{ mb: 2 }}>
          {error}
        </Typography>
      )}

      <Button
        variant="contained"
        color="primary"
        type="submit"
        disabled={loading}
        sx={{ textTransform: 'none', fontWeight: 700, px: 4, py: 1.5 }}
      >
        {loading ? 'Verifico...' : 'Accedi'}
      </Button>

      <Typography variant="body2" align="center" sx={{ mt: 2, color: '#fff' }}>
        Non sei registrato?{' '}
        <Link
          component="button"
          variant="body2"
          sx={{ color: '#00D084', fontWeight: 700 }}
          onClick={() => {
            onClose();
            onSwitchToRegister?.();
          }}
        >
          Registrati subito.
        </Link>
      </Typography>
    </Box>
  );
}
