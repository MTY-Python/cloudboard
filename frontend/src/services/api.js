import axios from 'axios'

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:3000/',
    headers: {
        'Content-Type': 'application/json',
    },
})

export const fetchLinks = async () => {
    const res = await api.get('/links')

    return res.data
}

export const createLink = async (url) => {
    const res = await api.post('/links', { url })

    if (res.data.success)
        return {
            success: true,
            errorMessage: null,

            id: res.data.link.id,
            url: res.data.link.url,
            shortUrl: res.data.link.shortUrl,
            created: res.data.link.created,
            expiration: res.data.link.expiration,
        }

    return {
        success: false,
        errorMessage: res.data.error,

        id: null,
        url: url,
        shortUrl: null,
        created: null,
        expiration: null,
    }
}

export const deleteLink = async (id) => {
    const res = await api.delete(`/links/${id}`)

    console.log(res)
    if (res.data.success)
        return { success: true }
    else
        return { success: false, errorMessage: res.data.error }
}

export const getLongUrl = async (shortCode) => {
    const res = await api.get(`/sc/${shortCode}`)

    if (res.data.success)
        return { success: true, longUrl: res.data.url }
    else
        return { success: false, errorMessage: res.data.error }
}

export default {
    fetchLinks,
    createLink,
    deleteLink,
    getLongUrl,
}
