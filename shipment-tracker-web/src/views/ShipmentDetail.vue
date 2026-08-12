<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useShipmentStore } from '@/stores/shipments'

const route = useRoute()
const store = useShipmentStore()

const newStatus = ref('')
const newNote = ref('')

onMounted(() => {
  store.fetchShipment(route.params.id)
})

async function handleAddEvent() {
  if (!newStatus.value) return
  await store.addStatusEvent(route.params.id, {
    status: newStatus.value,
    note: newNote.value || null,
  })
  newStatus.value = ''
  newNote.value = ''
}
</script>

<template>
  <div>
    <p v-if="store.loading">Loading...</p>
    <p v-else-if="store.error">{{ store.error }}</p>

    <div v-else-if="store.currentShipment">
      <h1>{{ store.currentShipment.tracking_number }}</h1>
      <p>Recipient: {{ store.currentShipment.recipient_name }}</p>
      <p>Destination: {{ store.currentShipment.destination_country }}</p>
      <p>Carrier: {{ store.currentShipment.carrier }}</p>
      <p>Status: <strong>{{ store.currentShipment.status }}</strong></p>

      <h2>Status history</h2>
      <ul>
        <li v-for="event in store.currentShipment.events" :key="event.id">
          {{ event.status }} — {{ new Date(event.occurred_at).toLocaleString() }}
          <span v-if="event.note">({{ event.note }})</span>
        </li>
      </ul>

      <h2>Add status event</h2>
      <select v-model="newStatus">
        <option value="">Select status</option>
        <option value="created">created</option>
        <option value="picked_up">picked_up</option>
        <option value="in_transit">in_transit</option>
        <option value="out_for_delivery">out_for_delivery</option>
        <option value="delivered">delivered</option>
        <option value="exception">exception</option>
      </select>
      <input v-model="newNote" placeholder="Optional note" />
      <button @click="handleAddEvent">Add event</button>
    </div>
  </div>
</template>