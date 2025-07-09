import React, { useState } from 'react';
import { Box, Button, TextField, Typography, IconButton } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';

// Base API URL dal .env
const API_URL = import.meta.env.VITE_API_URL;
const PASSWORD_REGEX = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&]).{8,}$/;

export default function RegisterPage({ onRegister, onClose }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setError('');
    if (!email || !password || !confirmPassword) {
      setError('Compila tutti i campi');
      return;
    }
    if (password !== confirmPassword) {
      setError('Le password non corrispondono');
      return;
    }

    if (!PASSWORD_REGEX.test(password)) {
         setError('La password deve avere almeno 8 caratteri, con maiuscole, minuscole, numeri e simboli');
      return;
    }

    setLoading(true);
    try {
      // POST JSON a /auth/register
      const res = await fetch(`${API_URL}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      if (!res.ok) {
        const data = await res.json();
        setError(data.detail || 'Registrazione fallita');
        setLoading(false);
        return;
      }

      const { access_token: token } = await res.json();
      localStorage.setItem('access_token', token);

      // Recupera profilo utente
      const meRes = await fetch(`${API_URL}/users/me`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!meRes.ok) {
        setError('Impossibile recuperare profilo');
        setLoading(false);
        return;
      }

      const userData = await meRes.json();
      onRegister(userData, token);
    } catch {
      setError('Registrazione fallita');
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
        Registrati a DataDash
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
        helperText="Min 8 caratteri, con maiuscole, minuscole, numeri e simboli"
        sx={{ maxWidth: 360, mb: 2, bgcolor: '#fff', borderRadius: 1 }}
      />
      <TextField
        label="Conferma Password"
        type="password"
        value={confirmPassword}
        onChange={e => setConfirmPassword(e.target.value)}
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
        {loading ? 'Registrando...' : 'Registrati'}
      </Button>
    </Box>
  );
}
