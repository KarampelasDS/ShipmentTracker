<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useShipmentStore } from '@/stores/shipments'

const router = useRouter()
const store = useShipmentStore()

const trackingNumber = ref('')
const recipientName = ref('')
const destinationCountry = ref('')
const carrier = ref('')
const submitting = ref(false)
const error = ref(null)

async function handleSubmit() {
  submitting.value = true
  error.value = null
  try {
    const newShipment = await store.createShipment({
      tracking_number: trackingNumber.value,
      recipient_name: recipientName.value,
      destination_country: destinationCountry.value,
      carrier: carrier.value,
    })
    router.push(`/shipments/${newShipment.id}`)
  } catch (err) {
    error.value = 'Failed to create shipment'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div>
    <h1>New shipment</h1>

    <p v-if="error">{{ error }}</p>

    <form @submit.prevent="handleSubmit">
      <input v-model="trackingNumber" placeholder="Tracking number" required />
      <input v-model="recipientName" placeholder="Recipient name" required />
      <input v-model="destinationCountry" placeholder="Destination country" required />
      <input v-model="carrier" placeholder="Carrier" required />
      <button type="submit" :disabled="submitting">
        {{ submitting ? 'Creating...' : 'Create shipment' }}
      </button>
    </form>
  </div>
</template>