import axios from "axios"
const API_URL = process.env.REACT_APP_API_URL

console.log('API_URL', API_URL)
const shopurl = axios.create({
  baseURL: API_URL,
})

// get search result
export const searchItems = async (text) => {
  
  const params = new URLSearchParams({
    keyword:text
  })
  const response = await shopurl.get(`SearchItems?${params}`)
  return response.data.Result
}

export const getItems = async (itemid) => {
  console.log('actions', itemid)

  const body = { itemid: itemid }
  const response = await shopurl.post(`/ContentItems`, body)
  
  return response.data.Result

}