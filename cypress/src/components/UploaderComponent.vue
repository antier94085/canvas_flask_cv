<script setup>
defineProps({
  handleFileUpload: Function,
  handleStep: Function,
})
</script>

<template>
  <div class="image-uploader flex items-center justify-center w-full mt-4 mb-8">
    <label
      for="dropzone-file"
      class="flex flex-col items-center justify-center w-full h-60 border-2 border-gray-400 border-dashed rounded-2xl cursor-pointer bg-gray-100"
    >
      <div class="flex flex-col items-center justify-center pt-5 pb-6 text-center">
        <img src="https://sma.stickeryou.com/v1/img/folder.svg" alt="upload-image" />
        <p class="text-base font-semibold text-gray-500 my-2">
          Drag your image, photo or<br />
          PDF document to start uploading
        </p>
        <div class="flex items-center justify-center">
          <hr class="h-[2px] w-20 bg-gray-400 border border-gray-400" />
          <span class="mx-5 text-base">OR</span>
          <hr class="h-[2px] w-20 bg-gray-400 border border-gray-400" />
        </div>
        <label
          class="mt-4 w-56 rounded rounded-s-full rounded-e-full bg-[#047fa1] border border-[#047fa1] py-2 text-base font-medium text-white capitalize hover:bg-transparent hover:text-[#047fa1]"
          for="dropzone-file"
        >
          Click to Upload File
        </label>
        <p class="text-xs mt-4">PNG, JPG, JPEG, GIF, PDF* --- Max. file size 25 MB</p>
      </div>
      <input
        id="dropzone-file"
        accept="image/*"
        type="file"
        class="hidden"
        @change="handleFileUpload"
      />
    </label>
  </div>
</template>
