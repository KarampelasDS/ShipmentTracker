import { defineStore } from 'pinia'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

export const useShipmentStore = defineStore('shipments', {
  state: () => ({
    shipments: [],
    currentShipment: null,
    loading: false,
    error: null,
  }),

  getters: {
    inTransit: (state) => state.shipments.filter(s => s.status === 'in_transit'),
  },

  actions: {
    async fetchShipments(statusFilter = null) {
      this.loading = true
      this.error = null
      try {
        const params = statusFilter ? { status: statusFilter } : {}
        const res = await axios.get(`${API_URL}/shipments`, { params })
        this.shipments = res.data
      } catch (err) {
        this.error = 'Failed to load shipments'
      } finally {
        this.loading = false
      }
    },

    async fetchShipment(id) {
      this.loading = true
      this.error = null
      try {
        const res = await axios.get(`${API_URL}/shipments/${id}`)
        this.currentShipment = res.data
      } catch (err) {
        this.error = 'Failed to load shipment'
      } finally {
        this.loading = false
      }
    },

    async createShipment(payload) {
      const res = await axios.post(`${API_URL}/shipments`, payload)
      return res.data
    },

    async addStatusEvent(shipmentId, payload) {
      const res = await axios.post(`${API_URL}/shipments/${shipmentId}/events`, payload)
      await this.fetchShipment(shipmentId) // refresh detail after adding event
      return res.data
    },
  },
})