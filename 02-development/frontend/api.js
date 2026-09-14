/* The single frontend/backend seam. Set window.FAIRSHARE_API_URL for another backend host. */
const FairShareAPI = (() => {
  const API_URL = window.FAIRSHARE_API_URL || 'http://127.0.0.1:8000/api';
  let csrfToken = '';

  const readError = async response => {
    let body = {};
    try { body = await response.json(); } catch (_) { /* non-JSON response */ }
    const detail = body.detail || Object.values(body.errors || {}).flat()[0] || `Request failed (${response.status}).`;
    const error = new Error(detail);
    error.status = response.status;
    error.errors = body.errors || {};
    return error;
  };

  const request = async (path, options = {}) => {
    const method = options.method || 'GET';
    const headers = { ...(options.body ? { 'Content-Type': 'application/json' } : {}), ...(options.headers || {}) };
    if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(method)) {
      if (!csrfToken) {
        const csrfResponse = await fetch(`${API_URL}/auth/csrf/`, { credentials: 'include' });
        const csrfBody = await csrfResponse.json();
        csrfToken = csrfBody.csrfToken;
      }
      headers['X-CSRFToken'] = csrfToken;
    }
    const response = await fetch(`${API_URL}${path}`, { ...options, method, headers, credentials: 'include' });
    if (!response.ok) throw await readError(response);
    if (response.status === 204) return true;
    return response.json();
  };

  return {
    async register({ username, password, name }) { return request('/auth/register/', { method: 'POST', body: JSON.stringify({ username, password, name }) }); },
    async login({ username, password }) { return request('/auth/login/', { method: 'POST', body: JSON.stringify({ username, password }) }); },
    async logout() { const result = await request('/auth/logout/', { method: 'POST' }); csrfToken = ''; return result; },
    async currentUser() { try { return await request('/auth/me/'); } catch (error) { if (error.status === 401) return null; throw error; } },
    async listExpenses() { return request('/expenses/'); },
    async getExpense(id) { return request(`/expenses/${encodeURIComponent(id)}/`); },
    async createExpense(expense) { return request('/expenses/', { method: 'POST', body: JSON.stringify(expense) }); },
    async deleteExpense(id) { return request(`/expenses/${encodeURIComponent(id)}/`, { method: 'DELETE' }); }
  };
})();
