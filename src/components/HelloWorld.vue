<script setup>
defineProps({
  msg: {
    type: String,
    required: true,
  },
})
</script>

<template>
  <div class="greetings">
    <h1 class="green">{{ msg }}</h1>
    <h3>
      You’ve successfully created a project with
      <a href="https://vite.dev/" target="_blank" rel="noopener">Vite</a> +
      <a href="https://vuejs.org/" target="_blank" rel="noopener">Vue 3</a>.
    </h3>
  </div>

  <div class="nav-buttons">
    <a href="https://vitejs.dev/guide/" target="_blank" rel="noopener">
      <button>Vite Docs</button>
    </a>
    <a href="https://vuejs.org/guide/" target="_blank" rel="noopener">
      <button>Vue Docs</button>
    </a>
  </div>
</template>

<style scoped>
h1 {
  font-weight: 500;
  font-size: 2.6rem;
  position: relative;
  top: -10px;
}

h3 {
  font-size: 1.2rem;
}

.greetings h1,
.greetings h3 {
  text-align: center;
}

.nav-buttons {
  margin-top: 2rem;
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.nav-buttons button {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  border: 1px solid #42b983;
  background-color: transparent;
  color: #42b983;
  cursor: pointer;
  transition: all 0.2s ease;
}

.nav-buttons button:hover {
  background-color: #42b983;
  color: white;
}

@media (min-width: 1024px) {
  .greetings h1,
  .greetings h3 {
    text-align: left;
  }
}
</style>
