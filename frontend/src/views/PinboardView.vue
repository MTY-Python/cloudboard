<template>
  <div
    class="w-full h-screen bg-gray-100 relative overflow-hidden"
    @click="addPin"
  >
    <div class="absolute top-4 left-4 bg-white p-3 rounded-lg shadow-md z-50">
      <div class="text-lg font-semibold">
        Pinboard for <span :class="`text-${userData.color}-600`">{{ userData.name }}</span>
      </div>
      <div class="text-sm text-gray-500">Click anywhere to create a new pin!</div>
    </div>

    <Pin
      v-for="pin in pins"
      :key="pin.id"
      :id="pin.id"
      :initial-x="pin.x"
      :initial-y="pin.y"
      :username="userData.username"
      :color="userData.color"
      @update:position="updatePinPosition(pin.id, $event)"
      @delete="deletePin"
    />
  </div>
</template>

<script setup>
import Pin from '@/components/Pin.vue';
import { reactive } from 'vue';

// Helper function for generating a unique ID (simple UUID-like string)
const generateUniqueId = () => Math.random().toString(36).substring(2, 9);

// Define Props to receive userData
const props = defineProps({
  userData: {
    type: Object,
    required: true, // ⭐ Removed the default property
    // We can also add a validator to ensure structure, but 'required: true' is sufficient here
  }
});

// --- Pin Management ---
const pins = reactive([]);

// Function to add a new pin at the clicked coordinates
const addPin = (event) => {
  if (event.target === event.currentTarget) {
    
    const newX = event.clientX - 100;
    const newY = event.clientY - 50; 

    pins.push({
      id: generateUniqueId(), // Assign a unique ID
      x: newX > 0 ? newX : 10,
      y: newY > 0 ? newY : 10,
    });
  }
};

// Function to update a pin's position after a drag
const updatePinPosition = (id, newPosition) => {
  const index = pins.findIndex(p => p.id === id);
  if (index !== -1) {
    pins[index].x = newPosition.x;
    pins[index].y = newPosition.y;
  }
};

// Function to delete a pin
const deletePin = (idToDelete) => {
  const index = pins.findIndex(p => p.id === idToDelete);
  if (index !== -1) {
    pins.splice(index, 1); // Remove the pin from the reactive array
  }
};
</script>