<script setup>
import { ref, onMounted } from "vue";
import LoginView from "./views/LoginView.vue";
import PinboardView from "./views/PinboardView.vue";

const userData = ref(null);

onMounted(() => {
  const saved = localStorage.getItem("userData");
  if (saved) {
    userData.value = JSON.parse(saved);
  }
});

const setUserData = (name, color) => {
  const data = { name, color };
  userData.value = data;
  localStorage.setItem("userData", JSON.stringify(data));
};

const logout = () => {
  userData.value = null;
  localStorage.removeItem("userData");
};
</script>

<template>
  <div id="app">
    <LoginView v-if="!userData" @login="setUserData" />
    <PinboardView v-else :userData="userData" @logout="logout" />
  </div>
</template>
