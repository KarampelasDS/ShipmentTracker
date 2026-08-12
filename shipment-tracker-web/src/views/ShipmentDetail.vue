<script setup>
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { useShipmentStore } from "@/stores/shipments";

const route = useRoute();
const store = useShipmentStore();

const newStatus = ref("");
const newNote = ref("");

onMounted(() => {
  store.fetchShipment(route.params.id);
});

function formatTime(value) {
  return new Date(value).toLocaleString();
}

async function handleAddEvent() {
  if (!newStatus.value) return;
  await store.addStatusEvent(route.params.id, {
    status: newStatus.value,
    note: newNote.value || null,
  });
  newStatus.value = "";
  newNote.value = "";
}
</script>

<template>
  <div>
    <router-link to="/" class="link"
      ><v-icon name="bi-arrow-left-circle-fill" /> Back to
      shipments</router-link
    >

    <p v-if="store.loading" class="state">Loading shipment…</p>
    <p v-else-if="store.error" class="state state--error">{{ store.error }}</p>

    <div v-else-if="store.currentShipment">
      <div class="page-head" style="margin-top: 16px">
        <h1 class="mono">{{ store.currentShipment.tracking_number }}</h1>
        <span class="badge" :data-status="store.currentShipment.status">{{
          store.currentShipment.status
        }}</span>
      </div>

      <div class="card">
        <div class="detail-grid">
          <span class="field-label">Recipient</span>
          <span>{{ store.currentShipment.recipient_name }}</span>
          <span class="field-label">Destination</span>
          <span>{{ store.currentShipment.destination_country }}</span>
          <span class="field-label">Carrier</span>
          <span>{{ store.currentShipment.carrier }}</span>
        </div>
      </div>

      <div class="section">
        <h2>Status history</h2>
        <ul v-if="store.currentShipment.events.length" class="timeline">
          <li v-for="event in store.currentShipment.events" :key="event.id">
            <span class="badge" :data-status="event.status">{{
              event.status
            }}</span>
            <span class="timeline__time">{{
              formatTime(event.occurred_at)
            }}</span>
            <span v-if="event.note" class="timeline__note"
              >— {{ event.note }}</span
            >
          </li>
        </ul>
        <p v-else class="state">No status events recorded yet.</p>
      </div>

      <div class="section">
        <h2>Add status event</h2>
        <div class="inline-form">
          <select v-model="newStatus" aria-label="Status">
            <option value="">Select status</option>
            <option value="created">created</option>
            <option value="picked_up">picked_up</option>
            <option value="in_transit">in_transit</option>
            <option value="out_for_delivery">out_for_delivery</option>
            <option value="delivered">delivered</option>
            <option value="exception">exception</option>
          </select>
          <input
            v-model="newNote"
            placeholder="Optional note"
            aria-label="Note"
          />
          <button class="btn" :disabled="!newStatus" @click="handleAddEvent">
            Add event
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
