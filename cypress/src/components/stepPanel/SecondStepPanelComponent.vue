<script setup>
import { ref, defineProps } from 'vue'
import { shapeData } from '@/utils/shapeData.js'
import { lineData } from '@/utils/lineData'


const text = ref('')
const activeShape = ref(null)

const props = defineProps({
  handleProcess: Function,
  handleLine: Function,
  outLine: Number,
  inLine: Number,
  addText: Function,
  removeObject: Function
})

const handleText = (e) => {
  text.value = e.target.value;
}

const handleShape = (index) => {
  activeShape.value = index
  if (!index) {
    props.handleProcess()
  }
}
const deleteObject = (str) => {
  props.removeObject(str)
}
</script>

<template>
  <div class="step-panel">
    <div class="text-panel pb-1">
      <div class="top-panel flex justify-between">
        <h3 class="text-xl font-semibold mb-1">Step 2</h3>
        <button class="px-4 py-2 leading-none bg-[#047fa1] text-white rounded-[4px]">
          Continue Editing
        </button>
      </div>
      <p class="text-base">Select Shape</p>
      <div class="shape-search-panel w-full rounded-2xl bg-[#f2f2f2] p-3">
        <input class="w-full h-12 p-3 rounded-xl border mb-2" placeholder="Search for Template" />
        <p class="text-base font-semibold mb-3">Popular Shapes</p>
        <div class="flex flex-wrap justify-between">
          <button
            v-for="(shapeItem, index) in shapeData"
            :key="index"
            :class="
              'bg-white w-[70px] h-[68px] rounded-md p-1 border-[2px] ' +
              (activeShape === index ? 'border-[#0099c4]' : '')
            "
            @click="handleShape(index)"
          >
            <img :src="shapeItem.img" :alt="shapeItem.name" />
          </button>
        </div>
        
      </div>
      <div class="w-full flex items-center justify-between my-5">
        <div class="relative h-10 flex-1 mr-2" v-for="(lineItem, index) in lineData" :key="index">
          <select
            class="peer h-full w-full rounded-[7px] border border-blue-gray-200 outline-none bg-transparent px-3 py-2.5 font-sans text-sm font-normal text-blue-gray-700 transition-all empty:!bg-gray-900"
            :value="index === 0 ? outLine : inLine"
            @change="(e) => handleLine(e.target.value, index)"
          >
            <option
              v-for="(lineValue, lineIndex) in lineItem.value"
              :value="lineValue"
              :key="lineIndex"
            >
              {{ lineValue }}
            </option>
          </select>
          <label
            class="before:content[' '] after:content[' '] pointer-events-none absolute left-0 -top-1.5 flex h-full w-full select-none text-[11px] font-normal leading-tight text-blue-gray-400 transition-all before:pointer-events-none before:mt-[6.5px] before:mr-1 before:box-border before:block before:h-1.5 before:w-2.5 before:rounded-tl-md before:border-l before:border-blue-gray-200 before:transition-all after:pointer-events-none after:mt-[6.5px] after:ml-1 after:box-border after:block after:h-1.5 after:w-2.5 after:flex-grow after:rounded-tr-md after:transition-all peer-placeholder-shown:text-sm peer-placeholder-shown:leading-[3.75] peer-placeholder-shown:text-blue-gray-500 peer-placeholder-shown:before:border-transparent peer-placeholder-shown:after:border-transparent peer-focus:text-[11px] peer-focus:leading-tight peer-focus:text-gray-900 peer-disabled:text-transparent peer-disabled:before:border-transparent peer-disabled:after:border-transparent peer-disabled:peer-placeholder-shown:text-blue-gray-500"
          >
            {{ lineItem.label }}
          </label>
        </div>
      </div>
      <div class="w-full flex items-center justify-between my-5">
        <div class="flex flex-wrap justify-between">
          <button @click="deleteObject('one')" class="px-4 py-2 leading-none bg-[#047fa1] text-white rounded-[4px] mr-1">
            Delete Selected Object
          </button>
          <button @click="deleteObject('all')" class="px-4 py-2 leading-none bg-[#047fa1] text-white rounded-[4px] p-2 ml-1">
            Delete All Object
          </button>
        </div>
      </div>
      
      <div class="text-panel w-full rounded-2xl bg-[#f2f2f2] p-3">
        <p class="text-base font-semibold mb-3">Add Text</p>
        <textarea
          id="message"
          rows="4"
          class="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          placeholder="Write your thoughts here..."
          @change="handleText"
        />
        <button
          class="bg-transparent w-full mt-4 hover:bg-gray-500 text-gray-700 font-semibold hover:text-white py-2 px-4 border border-gray-500 hover:border-transparent rounded"
          @click="addText(text)"
        >
          Add Text
        </button>
      </div>
    </div>
  </div>
</template>
