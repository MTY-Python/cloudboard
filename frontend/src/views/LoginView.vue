<script setup>
import { ref } from "vue";

const emit = defineEmits(["login"]);

const inputUsername = ref("");
const inputColor = ref("");

const colors = [
  { name: 'Red', colorClass: 'bg-red-500' },
  { name: 'Blue', colorClass: 'bg-blue-500' },
  { name: 'Green', colorClass: 'bg-green-500' },
  { name: 'Yellow', colorClass: 'bg-yellow-500' },
  { name: 'Purple', colorClass: 'bg-purple-500' },
];

const handleLogin = () => {
  if (!inputUsername.value || !inputColor.value) return;

  emit("login", inputUsername.value, inputColor.value);
};
</script>

<template>
  <div class="min-h-screen flex items-center justify-center text-black">
    <div class="border-4 border-black bg-white p-8 w-80 shadow-[8px_8px_0_0_#000] text-center">

      <input v-model="inputUsername" placeholder="Enter your username"
        class="w-full border-2 border-black p-2 mb-4 focus:outline-none focus:ring-4 focus:ring-blue-300" />

      <div class="flex space-x-2 mb-6 justify-center">
        <button v-for="color in colors" :key="color.name" @click="inputColor = color.name" :title="color.name"
          class="w-8 h-8 border-2 border-black rounded-full transition-all duration-150" :class="[
            color.colorClass,
            { 'ring-4 ring-black ring-offset-2': inputColor === color.name }
          ]"></button>
      </div>

      <button @click="handleLogin" :disabled="!inputUsername || !inputColor"
        class="w-full bg-primary text-white font-bold py-2 border-2 border-black transition-all duration-150" :class="{
          'bg-gray-400 cursor-not-allowed': !inputUsername || !inputColor,
          'bg-primary hover:bg-primary-hov active:translate-x-1 active:translate-y-1 active:shadow-none shadow-[4px_4px_0_0_#000]': inputUsername && inputColor
        }">
        Enter
      </button>
    </div>
  </div>
</template>
