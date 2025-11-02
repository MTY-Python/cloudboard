import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:5000",
  headers: {
    "Content-Type": "application/json",
  },
});

export const registerGuest = async (username, color) => {
  const res = await api.post("/register-guest", { username, color });
  return res.data; 
};

export const getNotes = async () => {
  const res = await api.get("/notes");
  return res.data.notes;
};

export const addNote = async (note) => {
  const res = await api.post("/notes", note);
  return res.data;
};

export const deleteNote = async (note_id) => {
  const res = await api.delete("/notes", { data: { note_id } });
  return res.data;
};

export const organiseNotes = async () => {
  const res = await api.get("/organise-firebase");
  return res.data;
};


export default api;
