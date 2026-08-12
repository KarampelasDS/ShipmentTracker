<script setup>
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { useShipmentStore } from "@/stores/shipments";

const store = useShipmentStore();
const router = useRouter();

onMounted(() => {
  store.fetchShipments();
});

function goToShipment(id) {
  router.push(`/shipments/${id}`);
}
</script>

<template>
  <div>
    <div class="page-head">
      <h1>Shipments</h1>
      <span v-if="store.shipments.length" class="muted"
        >{{ store.shipments.length }} total</span
      >
    </div>

    <p v-if="store.loading" class="state">Loading shipments…</p>
    <p v-else-if="store.error" class="state state--error">{{ store.error }}</p>

    <div v-else-if="store.shipments.length === 0" class="empty">
      No shipments yet. Create your first one to get started.
    </div>

    <div v-else class="table-wrap">
      <table>
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
            role="button"
            tabindex="0"
            @click="goToShipment(shipment.id)"
            @keydown.enter="goToShipment(shipment.id)"
          >
            <td class="mono">{{ shipment.tracking_number }}</td>
            <td>{{ shipment.recipient_name }}</td>
            <td>{{ shipment.destination_country }}</td>
            <td>
              <span class="badge">{{ shipment.status }}</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
