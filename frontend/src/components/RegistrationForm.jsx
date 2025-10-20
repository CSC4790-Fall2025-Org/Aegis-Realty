import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { registerWithEmail, loginWithEmail, getCurrentIdToken, sendIdTokenToBackend } from '../services/auth_service.js';

// Sign-up form
const RegistrationForm = () => {
  const [form, setForm] = useState({
    name: '',
    email: '',
    password: ''
  });
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      // Create user in Firebase
      await registerWithEmail(form.email, form.password);
    } catch (err) {
      // If the email is already in use, try to sign the user in instead (makes testing easier)
      if (err?.code === 'auth/email-already-in-use' || err?.message?.includes('email-already-in-use')) {
        try {
          await loginWithEmail(form.email, form.password);
        } catch (loginErr) {
          console.error('Login fallback failed', loginErr);
          setError(loginErr.message || 'Login fallback failed');
          setLoading(false);
          return;
        }
      } else {
        console.error(err);
        setError(err.message || 'Registration failed');
        setLoading(false);
        return;
      }
    }

    try {
      // Get id token
      const idToken = await getCurrentIdToken();

      // Optionally send token to backend to create a server session
      if (idToken) {
        await sendIdTokenToBackend(idToken);
      }

      setSubmitted(true);
      // short delay so user sees message then redirect
      setTimeout(() => navigate('/home'), 1000);
    } catch (err) {
      console.error(err);
      setError(err.message || 'Failed to complete registration flow');
    } finally {
      setLoading(false);
    }
  };

  if (submitted) {
    return <div>Registration successful! Redirecting to home...</div>;
  }

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: 400, margin: '2rem auto', padding: '2rem', border: '1px solid #ccc', borderRadius: '8px' }}>
      <h2>Sign Up</h2>
      <div>
        <label>Name:</label>
        <input type="text" name="name" value={form.name} onChange={handleChange} required />
      </div>
      <div>
        <label>Email:</label>
        <input type="email" name="email" value={form.email} onChange={handleChange} required />
      </div>
      <div>
        <label>Password:</label>
        <input type="password" name="password" value={form.password} onChange={handleChange} required />
      </div>
      <button type="submit" disabled={loading}>{loading ? 'Registering...' : 'Register'}</button>
      {error && <div style={{ color: 'red', marginTop: '0.5rem' }}>{error}</div>}
    </form>
  );
};

export default RegistrationForm;
