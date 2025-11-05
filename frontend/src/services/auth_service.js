import { auth } from './firebase.js';
import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
  getIdToken,
  GoogleAuthProvider,
  signInWithPopup
} from 'firebase/auth';

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || '';
const SKIP_BACKEND = (import.meta.env.VITE_SKIP_BACKEND === 'true');

export const registerWithEmail = async (email, password) => {
  return createUserWithEmailAndPassword(auth, email, password);
};

export const loginWithEmail = async (email, password) => {
  return signInWithEmailAndPassword(auth, email, password);
};

export const loginWithGoogle = async () => {
  const provider = new GoogleAuthProvider();
  return signInWithPopup(auth, provider);
};

export const logout = async () => {
  return signOut(auth);
};

export const onAuthChange = (callback) => {
  return onAuthStateChanged(auth, callback);
};

export const getCurrentIdToken = async () => {
  const user = auth.currentUser;
  if (!user) return null;
  return getIdToken(user, false);
};

export const sendIdTokenToBackend = async (idToken) => {
    /*developmnet */
  if (SKIP_BACKEND) {
    try {
      const short = idToken ? `${idToken.slice(0, 40)}...` : null;
      console.log('skip backend send; ID token truncated:', short);
      return { skipped: true };
    } catch (err) {
      throw new Error(`Failed to log ID token: ${err.message}`);
    }
  }
  /* real backend send*/
  if (!BACKEND_URL) throw new Error('VITE_BACKEND_URL not set');
  try {
    const resp = await fetch(`${BACKEND_URL.replace(/\/+$/,'')}/auth/session`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ idToken }),
    });
    if (!resp.ok) throw new Error(`Backend responded with ${resp.status}`);
    return resp.json();
  } catch (err) {
    throw new Error(`Failed to send ID token to backend: ${err.message}`);
  }
};

export default {
  registerWithEmail,
  loginWithEmail,
  loginWithGoogle,
  logout,
  onAuthChange,
  getCurrentIdToken,
  sendIdTokenToBackend,
};

/* Stubbing Backend During Development to test frontend wihtout running backend */