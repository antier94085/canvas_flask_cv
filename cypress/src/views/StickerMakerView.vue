<script setup>
import { onMounted, reactive, ref } from 'vue'
import { fabric } from 'fabric'
import { FirstStepPanelComponent, SecondStepPanelComponent } from '@/components/stepPanel'
import axios from 'axios'

let apiUrl = 'http://localhost:5050/'
const canvasSize = reactive({ width: 760, height: 590 })
const canvasPadding = ref(20)
const step = ref(1)
const outLine = ref(3)
const inLine = ref(3)
const imageUrl = ref('')

let canvas

const handleStep = (val) => {
  step.value = val
}

const handleLine = (val, type) => {
  if (type) {
    inLine.value = +val
  } else {
    outLine.value = +val
  }
}

const loadImage = (image_url) => {
  fabric.Image.fromURL(image_url, (img) => {
    const displayWidth = canvas.width - canvasPadding.value
    const displayHeight = canvas.height - canvasPadding.value
    if (img.width > displayWidth || img.height > displayHeight) {
      const widthRatio = displayWidth / img.width
      const heightRatio = displayHeight / img.height
      const scaleVal = Math.min(widthRatio, heightRatio)
      img.scale(scaleVal).set('flipX', false)
      img.top = (canvas.height - img.height * scaleVal) / 2
      img.left = (canvas.width - img.width * scaleVal) / 2
    } else {
      img.top = (canvas.height - img.height) / 2
      img.left = (canvas.width - img.width) / 2
    }
    canvas.add(img)
    canvas.setActiveObject(img)
  })
}

const handleFileUpload = async (event) => {
  const file = event.target.files[0]
  const imageOriginUrl = URL.createObjectURL(file)
  loadImage(imageOriginUrl)
  imageUrl.value = window.location.origin + '/pngs/' + file.name
  handleStep(2)
}

const addText = (text_content) => {
  console.log(text_content)
  const text = new fabric.Text(text_content, {
    left: 300,
    top: 300,
    fontFamily: 'Arial',
    fontSize: 24,
    fill: 'black'
  })
  canvas.add(text)
  canvas.setActiveObject(text)
}

const handleProcess = async () => {
  const reqData = {
    image_url: imageUrl.value,
    outLine: outLine.value,
    inLine: inLine.value,
    contours_type: 'path'
  }

  const res = await axios.post(apiUrl + 'edge', reqData)
  canvas.remove(canvas.getActiveObject())
  if (res.status === 200) {
    loadImage(apiUrl + 'image')
    loadImage(apiUrl + 'origin')
  }
}

const removeObject = (str) => {
  if (str === 'one')
    canvas.remove(canvas.getActiveObject())
  else if (str === 'all') {
    var objects = canvas.getObjects();
    objects.forEach(function (object) {
      canvas.remove(object);
    });
  }
}

onMounted(() => {
  canvas = new fabric.Canvas('canvasPanel', {
    width: canvasSize.width,
    height: canvasSize.height,
    backgroundColor: 'rgb(200, 200, 200)'
  })


  // Render canvas
  canvas.renderAll()
})
</script>

<template>
  <main class="main-container py-4 flex">
    <canvas id="canvasPanel" />
    <div class="ms-5 flex-1">
      <FirstStepPanelComponent :handleStep="handleStep" :handleFileUpload="handleFileUpload" v-if="step === 1" />
      <SecondStepPanelComponent :handleStep="handleStep" v-else-if="step === 2" :handleProcess="handleProcess"
        :inLine="inLine" :outLine="outLine" :handleLine="handleLine" :addText="addText" :removeObject="removeObject" />
    </div>
  </main>
</template>
