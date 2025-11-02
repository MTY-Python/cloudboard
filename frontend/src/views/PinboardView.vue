<template>
  <div class="w-full h-screen bg-gray-100 relative overflow-hidden" @click="addPin">
    <div class="absolute top-4 left-4 bg-white p-3 rounded-lg shadow-md z-50">
      <div class="text-lg font-semibold">
        Pinboard for <span :class="`text-${userData.color}-600`">{{ userData.name }}</span>
      </div>
      <div class="text-sm text-gray-500">Click anywhere to create a new pin!</div>
      <a href="#" @click.prevent="logout">Logout</a>
    
    </div>

    <Pin v-for="pin in pins" :key="pin.id" :id="pin.id" :x="pin.x" :y="pin.y" :username="pin.username"
      :color="pin.color" :content="pin.content" :user-data="userData" @update:position="updatePinPosition(pin.id, $event)"
      @delete="deletePin" @update:content="updatePin" />


    <button 
      @click.stop="handleOrganise" 
      class="absolute top-10 right-10 p-5 bg-blue-100 rounded-4xl text-gray-800 hover:text-indigo-700 hover:bg-indigo-100 transition focus:outline-none focus:ring-2 focus:ring-indigo-500 z-10"
      aria-label="Organise notes"
    >
      <SparklesIcon class="size-25" />
    </button>
  </div>
</template>

<script setup>
import Pin from '@/components/Pin.vue';
import { db } from '../services/firebaseDB';
import { collection, onSnapshot } from 'firebase/firestore';
import { reactive, onMounted, onUnmounted } from 'vue';
import { addNote, deleteNote, updateNote, organiseNotes } from '@/services/api';
import { SparklesIcon } from '@heroicons/vue/24/outline';

const generateUniqueId = () => Math.random().toString(36).substring(2, 9);

const props = defineProps({
  userData: {
    type: Object,
    required: true,
  }
});

const pins = reactive([]);

const emit = defineEmits(["logout"]);

const logout = () => {

  emit("logout");
};

const addPin = async (event) => {
  if (event.target === event.currentTarget) {
const rect = event.currentTarget.getBoundingClientRect();

    const rawX = event.clientX - rect.left;
    const rawY = event.clientY - rect.top;
    
    const newX = rawX - 100; 
    const newY = rawY - 50;  

    const newPinData = {
      x: newX > 0 ? newX : 10,
      y: newY > 0 ? newY : 10,
      text: '',
      guest_id: generateUniqueId(),
      color: props.userData.color,
      author: props.userData.name,
    };

    try {
      const noteResult = await addNote(newPinData)

      console.log(noteResult)
    } catch (error) {
      console.error('Failed to add note:', error)
    }

    // pins.push({
    //   id: generateUniqueId(),
    //   x: newX > 0 ? newX : 10,
    //   y: newY > 0 ? newY : 10,
    // });
  }
};

const updatePinPosition = (id, newPosition) => {
  const index = pins.findIndex(p => p.id === id);
  if (index !== -1) {
    pins[index].x = newPosition.x;
    pins[index].y = newPosition.y;
  }
};

const deletePin = async (idToDelete) => {


  try {
    const noteResult = await deleteNote(idToDelete)

    const index = pins.findIndex(p => p.id === idToDelete);
    if (index !== -1) {
      pins.splice(index, 1);
    }

    console.log(noteResult)
  } catch (error) {
    console.error('Failed to delete note:', error)
  }

};

const updatePin = async (id, text) => {


  try {
    const noteResult = await updateNote(id, text)


    console.log(noteResult)
  } catch (error) {
    console.error('Failed to update note:', error)
  }

};

const handleOrganise = async () => {
    const result = await organiseNotes(); 
    
    console.log("Organise Notes Result:", result);
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

        x: data.x,

        y: data.y,

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