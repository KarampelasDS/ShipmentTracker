<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useShipmentStore } from '@/stores/shipments'

const store = useShipmentStore()
const router = useRouter()

onMounted(() => {
  store.fetchShipments()
})

function goToShipment(id) {
  router.push(`/shipments/${id}`)
}
</script>

<template>
  <div>
    <div style="display: flex; justify-content: space-between; align-items: center;">
      <h1>Shipments</h1>
      <router-link to="/shipments/new">+ New shipment</router-link>
    </div>

    <p v-if="store.loading">Loading...</p>
    <p v-else-if="store.error">{{ store.error }}</p>

    <table v-else>
      <thead>
        <tr>
          <th>Tracking number</th>
          <th>Recipient</th>
          <th>Destination</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="shipment in store.shipments"
          :key="shipment.id"
          @click="goToShipment(shipment.id)"
          style="cursor: pointer;"
        >
          <td>{{ shipment.tracking_number }}</td>
          <td>{{ shipment.recipient_name }}</td>
          <td>{{ shipment.destination_country }}</td>
          <td>{{ shipment.status }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>