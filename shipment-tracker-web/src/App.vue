<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
</script>

<template>
  <header class="app-header">
    <div class="app-header__inner">
      <RouterLink to="/" class="app-header__title">Shipment Tracker</RouterLink>
      <nav class="app-nav">
        <RouterLink to="/" class="app-nav__link">Shipments</RouterLink>
        <RouterLink to="/shipments/new" class="btn btn--sm"
          >New shipment</RouterLink
        >
      </nav>
    </div>
  </header>

  <main class="app-main">
    <RouterView />
  </main>
</template>
