import axios from 'axios';
import store from './store';
import router from './router';

const API_BASE = 'http://localhost:8000/api/auth';
const INACTIVITY_LIMIT_MS = 15 * 60 * 1000;
const LAST_ACTIVITY_KEY = 'user-last-activity';
const SESSION_EXPIRED_MSG_KEY = 'session-expired-message';
let refreshingPromise = null;
let lastActivityRefresh = 0;

function parseJwt(token) {
  try {
    const payload = token.split('.')[1];
    return JSON.parse(atob(payload));
  } catch (e) {
    return null;
  }
}

function tokenExpiresSoon(token, thresholdSeconds = 180) {
  const payload = parseJwt(token);
  if (!payload?.exp) return true;
  const now = Math.floor(Date.now() / 1000);
  return payload.exp - now <= thresholdSeconds;
}

function touchActivity() {
  localStorage.setItem(LAST_ACTIVITY_KEY, String(Date.now()));
}

function isInactiveTooLong() {
  const lastActivity = Number(localStorage.getItem(LAST_ACTIVITY_KEY) || 0);
  if (!lastActivity) return true;
  return Date.now() - lastActivity > INACTIVITY_LIMIT_MS;
}

async function forceLogoutByInactivity() {
  localStorage.setItem(SESSION_EXPIRED_MSG_KEY, 'Tu sesión ha expirado por inactividad. Inicia sesión de nuevo.');
  await store.dispatch('logout');
  if (router.currentRoute.value.path !== '/login') {
    router.push('/login');
  }
}

async function refreshAccessToken() {
  const refreshToken = localStorage.getItem('user-refresh-token');
  if (!refreshToken) throw new Error('No refresh token');

  const response = await axios.post(`${API_BASE}/refresh`, {}, {
    headers: { Authorization: `Bearer ${refreshToken}` }
  });

  const newToken = response.data.access_token;
  store.commit('SET_TOKEN', newToken);
  localStorage.setItem('user-token', newToken);
  return newToken;
}

async function ensureFreshToken() {
  if (isInactiveTooLong()) {
    await forceLogoutByInactivity();
    throw new Error('Sesión expirada por inactividad');
  }

  if (refreshingPromise) return refreshingPromise;

  refreshingPromise = refreshAccessToken()
    .catch(async (error) => {
      await forceLogoutByInactivity();
      throw error;
    })
    .finally(() => {
      refreshingPromise = null;
    });

  return refreshingPromise;
}

function onUserActivity() {
  const token = localStorage.getItem('user-token');
  const refreshToken = localStorage.getItem('user-refresh-token');
  if (!token || !refreshToken) return;

  touchActivity();

  const now = Date.now();
  if (now - lastActivityRefresh < 60_000) return;

  if (tokenExpiresSoon(token, 300)) {
    lastActivityRefresh = now;
    ensureFreshToken().catch(() => {
      // Gestión de logout ya realizada en ensureFreshToken
    });
  }
}

export function initSessionManager() {
  if (localStorage.getItem('user-token')) {
    touchActivity();
  }

  axios.interceptors.request.use(async (config) => {
    // Detectamos automáticamente si estamos en desarrollo local o en producción en Render
    let apiBaseUrl = 'https://coworkflow-backend.onrender.com';
    
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
      apiBaseUrl = 'http://localhost:8000';
    }

    if (config.url && config.url.startsWith('http://localhost:8000')) {
      config.url = config.url.replace('http://localhost:8000', apiBaseUrl);
    }

    const token = localStorage.getItem('user-token');
    const refreshToken = localStorage.getItem('user-refresh-token');

    if (token && !config.headers?.Authorization) {
      if (refreshToken && tokenExpiresSoon(token, 30) && !config.url?.includes('/api/auth/refresh')) {
        const fresh = await ensureFreshToken();
        config.headers.Authorization = `Bearer ${fresh}`;
      } else {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }

    return config;
  });

  axios.interceptors.response.use(
    (response) => response,
    async (error) => {
      const originalRequest = error.config || {};
      if (
        error.response?.status === 401 &&
        !originalRequest._retry &&
        !String(originalRequest.url || '').includes('/api/auth/refresh') &&
        localStorage.getItem('user-refresh-token') &&
        !isInactiveTooLong()
      ) {
        originalRequest._retry = true;
        const fresh = await ensureFreshToken();
        originalRequest.headers = originalRequest.headers || {};
        originalRequest.headers.Authorization = `Bearer ${fresh}`;
        return axios(originalRequest);
      }

      return Promise.reject(error);
    }
  );

  const events = ['click', 'keydown', 'mousemove', 'scroll', 'touchstart'];
  events.forEach((eventName) => {
    window.addEventListener(eventName, onUserActivity, { passive: true });
  });
}
