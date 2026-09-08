const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

export async function fetchHealth(){
    const response = await fetch(`${API_BASE_URL}/health/`);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();

}