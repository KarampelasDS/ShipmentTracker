<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useShipmentStore } from "@/stores/shipments";

const router = useRouter();
const store = useShipmentStore();

const trackingNumber = ref("");
const recipientName = ref("");
const destinationCountry = ref("");
const carrier = ref("");
const submitting = ref(false);
const error = ref(null);

async function handleSubmit() {
  submitting.value = true;
  error.value = null;
  try {
    const newShipment = await store.createShipment({
      tracking_number: trackingNumber.value,
      recipient_name: recipientName.value,
      destination_country: destinationCountry.value,
      carrier: carrier.value,
    });
    router.push(`/shipments/${newShipment.id}`);
  } catch (err) {
    error.value = "Failed to create shipment";
  } finally {
    submitting.value = false;
  }
}
</script>

<template>
  <div class="page--narrow">
    <router-link to="/" class="link"
      ><v-icon name="bi-arrow-left-circle-fill" /> Back to
      shipments</router-link
    >

    <div class="page-head" style="margin-top: 16px">
      <h1>New shipment</h1>
    </div>

    <div class="card">
      <p v-if="error" class="state state--error">{{ error }}</p>

      <form class="form" @submit.prevent="handleSubmit">
        <div class="form-row">
          <label for="tracking">Tracking number</label>
          <input id="tracking" v-model="trackingNumber" required />
        </div>
        <div class="form-row">
          <label for="recipient">Recipient name</label>
          <input id="recipient" v-model="recipientName" required />
        </div>
        <div class="form-row">
          <label for="destination">Destination country</label>
          <input id="destination" v-model="destinationCountry" required />
        </div>
        <div class="form-row">
          <label for="carrier">Carrier</label>
          <input id="carrier" v-model="carrier" required />
        </div>
        <div>
          <button class="btn" type="submit" :disabled="submitting">
            {{ submitting ? "Creating…" : "Create shipment" }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
