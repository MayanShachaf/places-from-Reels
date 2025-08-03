import axios from "axios";

const API_BASE_URL = "https://rapidly-uncommon-kiwi.ngrok-free.app";

export const getUserPlaces = async (userId: string) => {
  const res = await axios.get(`${API_BASE_URL}/places/get_all_places_for_user`, {params: { user_id: userId }});
  return res.data;
};
export const addPlace = async (userId: string, text: string) => {
  const res = await axios.post(`${API_BASE_URL}/places/add_place`, { user_id: userId, text });
  return res.data;
};
export const addUser = async (userName: string, userEmail: string) => {
    const res = await axios.post(`${API_BASE_URL}/users/create_user`, { name: userName, email: userEmail });
    return res.data;
    }

export const get_favorite_places_ids = async (userId: string) => {
    const res = await axios.get(`${API_BASE_URL}/users/get_favorite_places`);
    return res.data;
}
export const addFavoritePlace = async (placeId: string, userId: string) => {
    const res = await axios.post(`${API_BASE_URL}/users/add_favorite_place`, { place_id: placeId, user_id: userId });
    return res.data;
}