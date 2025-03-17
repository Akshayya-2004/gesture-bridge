const API_BASE_URL = "http://127.0.0.1:5000"; // Change if using a deployed backend

export const getGesture = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/detect`);
        return response.json();
    } catch (error) {
        console.error("Error fetching gesture:", error);
    }
};
