<template>
  <div class="absolute rounded-lg shadow-xl transition-shadow duration-200" :class="[
    selectedColorClasses.pinBgClass,
    { 'z-50 shadow-2xl scale-[1.02]': isDragging }
  ]" :style="{
    top: `${props.y}px`,
    left: `${props.x}px`,

    transform: `translate(${offset.x}px, ${offset.y}px) ${isDragging ? 'translateZ(0)' : 'none'}`
  }">
    <button @click.stop="handleDelete"
      class="absolute top-2 right-2 p-1 rounded-full text-gray-800 hover:text-red-700 hover:bg-red-100 transition focus:outline-none focus:ring-2 focus:ring-red-500 z-10"
      aria-label="Delete pin">
      <XMarkIcon class="size-5" />
    </button>

    <div class="p-2 rounded-t-lg font-bold text-sm opacity-90 cursor-grab border-b-2 border-opacity-30 relative"
      :class="selectedColorClasses.headerBgClass" @mousedown="startDrag" @touchstart="startDrag">
      Pin by: {{ username }}
    </div>

    <div class="p-3">
      <textarea
        class="w-48 h-24 bg-transparent resize-none focus:outline-none placeholder-gray-800 dark:placeholder-gray-200 mb-2"
        placeholder="Type your note here..." :value="localContent"
        @input="localContent = $event.target.value"></textarea>

      <button @click.stop="handleUpdate" :disabled="localContent === content"
        class="p-1 text-sm font-semibold rounded transition duration-150 ease-in-out z-10" :class="{
          'bg-gray-500 text-white cursor-not-allowed opacity-70': localContent === content,
          'bg-blue-600 hover:bg-blue-700 text-white shadow-md': localContent !== content
        }">
        <CheckIcon class="size-5" />
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'; // Added 'watch'
import { CheckIcon, XMarkIcon } from '@heroicons/vue/24/outline';
import { colors } from '@/services/colors.js';

const props = defineProps({
  id: { type: String, required: true },
  x: { type: Number, default: 100 },
  y: { type: Number, default: 100 },
  username: { type: String, required: true },
  color: { type: String, default: 'yellow' },
  content: { type: String, default: '' },
  userData: {
    type: Object,
    required: true,
  }
});

const emit = defineEmits(['update:position', 'delete', 'update:content']);

// 1. New reactive state for local content
const localContent = ref(props.content);

watch(() => props.content, (newContent) => {
  if (props.username !== props.userData.name) {
    localContent.value = newContent;
  }
});

const isDragging = ref(false);
const offset = ref({ x: 0, y: 0 });

const handleUpdate = () => {
  if (localContent.value !== props.content) {
    emit('update:content', props.id, localContent.value);
  }
};

const handleDelete = () => {
  emit('delete', props.id);
};

const selectedColorClasses = computed(() => {
  const defaultColor = {
    pinBgClass: 'bg-yellow-300 text-gray-900',
    headerBgClass: 'bg-yellow-400 border-yellow-500'
  };

  return colors.find(c => c.colorKey === props.color) || defaultColor;
});

let MouseX = 0;
let MouseY = 0;

const startDrag = (e) => {
  if (e.type === 'touchstart') {
    e.preventDefault();
  }
  isDragging.value = true;

  const clientX = e.type.startsWith('mouse') ? e.clientX : e.touches[0].clientX;
  const clientY = e.type.startsWith('mouse') ? e.clientY : e.touches[0].clientY;

  MouseX = clientX;
  MouseY = clientY;


  document.addEventListener('mousemove', onDrag);
  document.addEventListener('mouseup', stopDrag);
  document.addEventListener('touchmove', onDrag);
  document.addEventListener('touchend', stopDrag);
};

const onDrag = (e) => {
  if (!isDragging.value) return;

  const clientX = e.type.startsWith('mouse') ? e.clientX : e.touches[0].clientX;
  const clientY = e.type.startsWith('mouse') ? e.clientY : e.touches[0].clientY;

  const dx = clientX - MouseX;
  const dy = clientY - MouseY;

  offset.value = { x: dx, y: dy };
};

const stopDrag = () => {
  isDragging.value = false;

  document.removeEventListener('mousemove', onDrag);
  document.removeEventListener('mouseup', stopDrag);
  document.removeEventListener('touchmove', onDrag);
  document.removeEventListener('touchend', stopDrag);

  const newX = props.x + offset.value.x;
  const newY = props.y + offset.value.y;

  emit('update:position', { x: newX, y: newY });

  offset.value = { x: 0, y: 0 };
};
</script>