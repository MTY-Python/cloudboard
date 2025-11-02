<template>
  <div class="w-full h-screen bg-gray-100 relative overflow-hidden" @click="addPin">
    <div class="absolute top-4 left-4 bg-white p-3 rounded-lg shadow-md z-50">
      <div class="text-lg font-semibold">
        Pinboard for <span :class="`text-${userData.color}-600`">{{ userData.name }}</span>
      </div>
      <div class="text-sm text-gray-500">Click anywhere to create a new pin!</div>
    </div>

    <Pin v-for="pin in pins" :key="pin.id" :id="pin.id" :initial-x="pin.initialX" :initial-y="pin.initialY"
      :username="pin.username" :color="pin.color" :content="pin.content"
      @update:position="updatePinPosition(pin.id, $event)" @delete="deletePin" />
  </div>
</template>

<script setup>
import Pin from '@/components/Pin.vue';
import { db } from '../services/firebaseDB';
import { collection, onSnapshot } from 'firebase/firestore';
import { reactive, onMounted, onUnmounted } from 'vue';
import { addNote } from '@/services/api';

const generateUniqueId = () => Math.random().toString(36).substring(2, 9);

const props = defineProps({
  userData: {
    type: Object,
    required: true,
  }
});

const pins = reactive([]);

const addPin = async (event) => {
  if (event.target === event.currentTarget) {

    const newX = event.clientX - 100;
    const newY = event.clientY - 50;

    const newPinData = {
      initialX: newX > 0 ? newX : 10,
      initialY: newY > 0 ? newY : 10,
      content: '',
      color: userData.color,
      username: userData.username,
    };

    try {
      const noteResult = await addNote(newPinData)

      console.log(noteResult)
    } catch (error) {
      console.error('Failed to add note:', error)
    }

    pins.push({
      id: generateUniqueId(),
      x: newX > 0 ? newX : 10,
      y: newY > 0 ? newY : 10,
    });
  }
};

const updatePinPosition = (id, newPosition) => {
  const index = pins.findIndex(p => p.id === id);
  if (index !== -1) {
    pins[index].initialX = newPosition.x;
    pins[index].y = newPosition.y;
  }
};

const deletePin = (idToDelete) => {
  const index = pins.findIndex(p => p.id === idToDelete);
  if (index !== -1) {
    pins.splice(index, 1);
  }
};


let unsubscribe = null;

onMounted(() => {
  const pinsRef = collection(db, 'notes');

  unsubscribe = onSnapshot(pinsRef, (snapshot) => {

    const fetchedPins = snapshot.docs.map(doc => {
      const data = doc.data();

      const mappedPin = {
        id: doc.id,

        username: data.author,

        content: data.text || '',

        initialX: data.initialX,

        initialY: data.initialY,

        color: data.color,
      };

      return mappedPin;
    });

    pins.splice(0, pins.length, ...fetchedPins);
  });
});

onUnmounted(() => {
  if (unsubscribe) unsubscribe();
});
</script>