const API_URL = 'https://financey.onrender.com/api';

export async function fetchAPI(endpoint: string, options: RequestInit = {}) {
    let token = null;
    if (typeof window !== 'undefined') {
        token = localStorage.getItem('access_token');
    }

    const headers = {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
        ...options.headers,
    };

    const response = await fetch(`${API_URL}${endpoint}`, { ...options, headers });
    
    if (response.status === 401 && typeof window !== 'undefined') {
        // Attempt token refresh or redirect to login
        localStorage.removeItem('access_token');
        window.location.href = '/login';
    }

    if (!response.ok) {
        let errorData = {};
        try {
            errorData = await response.json();
        } catch(e) {}
        throw { status: response.status, data: errorData };
    }

    if (response.status === 204) return null;
    return response.json();
}
