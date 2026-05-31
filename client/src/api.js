import axios from 'axios'

const API_BASE_URL = 'http://localhost:8001/api'

// Build URLSearchParams from a filters object, including only the allowed keys
// and skipping unset or 'all' values.
const buildParams = (filters = {}, allowedKeys = []) => {
  const params = new URLSearchParams()
  for (const key of allowedKeys) {
    const value = filters[key]
    if (value && value !== 'all') params.append(key, value)
  }
  return params
}

export const api = {
  async getInventory(filters = {}) {
    const params = buildParams(filters, ['warehouse', 'category'])

    const response = await axios.get(`${API_BASE_URL}/inventory?${params.toString()}`)
    return response.data
  },

  async getInventoryItem(id) {
    const response = await axios.get(`${API_BASE_URL}/inventory/${id}`)
    return response.data
  },

  async getOrders(filters = {}) {
    const params = buildParams(filters, ['warehouse', 'category', 'status', 'month'])

    const response = await axios.get(`${API_BASE_URL}/orders?${params.toString()}`)
    return response.data
  },

  async getOrder(id) {
    const response = await axios.get(`${API_BASE_URL}/orders/${id}`)
    return response.data
  },

  async getDemandForecasts() {
    const response = await axios.get(`${API_BASE_URL}/demand`)
    return response.data
  },

  async getBacklog() {
    const response = await axios.get(`${API_BASE_URL}/backlog`)
    return response.data
  },

  async getDashboardSummary(filters = {}) {
    const params = buildParams(filters, ['warehouse', 'category', 'status', 'month'])

    const response = await axios.get(`${API_BASE_URL}/dashboard/summary?${params.toString()}`)
    return response.data
  },

  async getSpendingSummary() {
    const response = await axios.get(`${API_BASE_URL}/spending/summary`)
    return response.data
  },

  async getMonthlySpending() {
    const response = await axios.get(`${API_BASE_URL}/spending/monthly`)
    return response.data
  },

  async getCategorySpending() {
    const response = await axios.get(`${API_BASE_URL}/spending/categories`)
    return response.data
  },

  async getTransactions() {
    const response = await axios.get(`${API_BASE_URL}/spending/transactions`)
    return response.data
  },

  async getQuarterlyReports() {
    const response = await axios.get(`${API_BASE_URL}/reports/quarterly`)
    return response.data
  },

  async getMonthlyTrends() {
    const response = await axios.get(`${API_BASE_URL}/reports/monthly-trends`)
    return response.data
  },

  async getTasks() {
    const response = await axios.get(`${API_BASE_URL}/tasks`)
    return response.data
  },

  async createTask(taskData) {
    const response = await axios.post(`${API_BASE_URL}/tasks`, taskData)
    return response.data
  },

  async deleteTask(taskId) {
    const response = await axios.delete(`${API_BASE_URL}/tasks/${taskId}`)
    return response.data
  },

  async toggleTask(taskId) {
    const response = await axios.patch(`${API_BASE_URL}/tasks/${taskId}`)
    return response.data
  }
}
