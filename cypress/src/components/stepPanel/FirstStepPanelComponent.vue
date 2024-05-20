<script setup>
import { ref, reactive } from 'vue'
import UploaderImage from '@/components/UploaderComponent.vue'

defineProps({
  step: Number,
  handleStep: Function,
  handleFileUpload: Function,
})

const active = ref(0)
const buttonData = reactive([{ btn_name: 'Upload Image' }, { btn_name: 'Add Art' }])
</script>

<template>
  <div class="step-panel font-sans">
    <div class="text-panel pb-1">
      <h3 class="text-xl font-semibold mb-1">Step 1</h3>
      <p class="text-base">Upload or Add an Image</p>
    </div>
    <div class="tab-content p-4 flex flex-col items-center">
      <div class="switch-box p-1 border rounded-s-full rounded-e-full flex">
        <button
          v-for="(btnItem, index) in buttonData"
          :key="index"
          :class="
            'h-12 w-40 rounded-s-full rounded-e-full ' + (active === index ? 'bg-[#cceef8]' : '')
          "
          @click="active = index"
        >
          {{ btnItem.btn_name }}
        </button>
      </div>
      <UploaderImage :handleStep="handleStep" :handleFileUpload="handleFileUpload" />
      <button class="mb-4 text-base font-medium text-[#01acdc] capitalize">
        Skip & Go to the Editor
      </button>
      <p class="text-xs text-wrap">
        * For PDF files, you can create your own custom die-cut.
        <br />
        See PDF requirements
      </p>
    </div>
  </div>
</template>
