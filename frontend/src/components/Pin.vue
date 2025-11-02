<template>
  <div
    class="absolute rounded-lg shadow-xl transition-shadow duration-200"
    :class="[
      selectedColorClasses.pinBgClass,
      { 'z-50 shadow-2xl scale-[1.02]': isDragging }
    ]"
    :style="{ top: `${y}px`, left: `${x}px` }"
  >
    <button 
      @click.stop="handleDelete" 
      class="absolute top-2 right-2 p-1 rounded-full text-gray-800 hover:text-red-700 hover:bg-red-100 transition focus:outline-none focus:ring-2 focus:ring-red-500 z-10"
      aria-label="Delete pin"
    >
      <XMarkIcon class="size-5" />
    </button>
    
    <div
      class="p-2 rounded-t-lg font-bold text-sm opacity-90 cursor-grab border-b-2 border-opacity-30 relative"
      :class="selectedColorClasses.headerBgClass"
      @mousedown="startDrag"
      @touchstart="startDrag"
    >
      Pin by: {{ username }}
    </div>

    <div class="p-3">
      <textarea
        class="w-48 h-24 bg-transparent resize-none focus:outline-none placeholder-gray-800 dark:placeholder-gray-200"
        placeholder="Type your note here..."
        :value="content" 
        @input="updateContent($event.target.value)"
      ></textarea>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { XMarkIcon } from '@heroicons/vue/24/outline'; 
import { colors } from '@/services/colors.js';

const props = defineProps({
  id: { type: String, required: true },
  initialX: { type: Number, default: 50 },
  initialY: { type: Number, default: 50 },
  username: { type: String, required: true },
  color: { type: String, default: 'yellow' },
  // NEW: Prop for the pin's text content
  content: { type: String, default: '' }, 
});

const emit = defineEmits(['update:position', 'delete', 'update:content']);

const x = ref(props.initialX);
const y = ref(props.initialY);
const isDragging = ref(false);

// NEW: Emits the updated content back to the parent
const updateContent = (newContent) => {
    emit('update:content', newContent);
};

const handleDelete = () => {
    emit('delete', props.id);
};

// ⭐ STEP 2: Computed property to map the color prop string to the actual classes
const selectedColorClasses = computed(() => {
    // Find the color object that matches the 'color' prop (e.g., 'blue')
    const defaultColor = { 
        pinBgClass: 'bg-yellow-300 text-gray-900', 
        headerBgClass: 'bg-yellow-400 border-yellow-500' 
    };
    
    return colors.find(c => c.colorKey === props.color) || defaultColor;
});

// --- Drag Logic (using local refs x and y) ---
let initialMouseX = 0;
let initialMouseY = 0;
let initialPinX = 0;
let initialPinY = 0;

const startDrag = (e) => {
  if (e.type === 'touchstart') {
    e.preventDefault();
  }
  isDragging.value = true;
  
  const clientX = e.type.startsWith('mouse') ? e.clientX : e.touches[0].clientX;
  const clientY = e.type.startsWith('mouse') ? e.clientY : e.touches[0].clientY;

  initialMouseX = clientX;
  initialMouseY = clientY;
  initialPinX = x.value;
  initialPinY = y.value;

  document.addEventListener('mousemove', onDrag);
  document.addEventListener('mouseup', stopDrag);
  document.addEventListener('touchmove', onDrag);
  document.addEventListener('touchend', stopDrag);
};

const onDrag = (e) => {
  if (!isDragging.value) return;
  
  const clientX = e.type.startsWith('mouse') ? e.clientX : e.touches[0].clientX;
  const clientY = e.type.startsWith('mouse') ? e.clientY : e.touches[0].clientY;

  const dx = clientX - initialMouseX;
  const dy = clientY - initialMouseY;
  
  x.value = initialPinX + dx;
  y.value = initialPinY + dy;
};

const stopDrag = () => {
  isDragging.value = false;
  
  document.removeEventListener('mousemove', onDrag);
  document.removeEventListener('mouseup', stopDrag);
  document.removeEventListener('touchmove', onDrag);
  document.removeEventListener('touchend', stopDrag);
  
  // Emit final position to update parent state
  emit('update:position', { x: x.value, y: y.value });
};
</script>