import { createRouter, createWebHistory } from 'vue-router'
import ShipmentList from '@/views/ShipmentList.vue'
import ShipmentDetail from '@/views/ShipmentDetail.vue'
import NewShipment from '@/views/NewShipment.vue'

const routes = [
  { path: '/', component: ShipmentList },
  { path: '/shipments/new', component: NewShipment },
  { path: '/shipments/:id', component: ShipmentDetail },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router