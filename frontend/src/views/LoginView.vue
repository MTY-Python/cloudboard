<script setup>
import { ref } from "vue";
// ⭐ The imported 'colors' array is now the single source of truth
import { colors } from "@/services/colors"; 

const emit = defineEmits(["login"]);

const inputUsername = ref("");
const inputColor = ref("");

// The conflicting local 'const colors = [...]' array has been removed.

const handleLogin = () => {
  if (!inputUsername.value || !inputColor.value) return;

  // Emits the color's name (e.g., 'Red')
  emit("login", inputUsername.value, inputColor.value);
};
</script>

<template>
  <div class="min-h-screen flex items-center justify-center text-black">
    <div class="border-4 border-black bg-white p-8 w-80 shadow-[8px_8px_0_0_#000] text-center">

      <input v-model="inputUsername" placeholder="Enter your username"
        class="w-full border-2 border-black p-2 mb-4 focus:outline-none focus:ring-4 focus:ring-blue-300" />

      <div class="flex space-x-2 mb-6 justify-center">
        <button v-for="color in colors" :key="color.name" @click="inputColor = color.colorKey" :title="color.name"
          class="w-8 h-8 border-2 border-black rounded-full transition-all duration-150" :class="[
            color.buttonClass, //
            { 'ring-4 ring-black ring-offset-2': inputColor === color.colorKey }
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