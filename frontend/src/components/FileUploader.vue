<template>
  <div
    class="border-2 border-dashed border-gray-300 rounded-2xl p-8 text-center bg-white hover:border-blue-400 transition-colors duration-200 cursor-pointer"
    @dragover.prevent
    @drop.prevent="handleDrop"
    @click="triggerFileInput"
  >
    <input ref="fileInput" type="file" class="hidden" @change="onFileChange" multiple />
    <p class="text-lg text-gray-700 font-medium mb-2">拖拽文件到此处或点击上传</p>
    <p class="text-sm text-gray-500 mb-4">支持 PDF, DOC, DOCX, PPT, PPTX, MD, TXT 格式</p>
    <button class="px-4 py-2 bg-gray-600 hover:bg-blue-500 text-white text-sm font-semibold rounded-md">
      选择文件
    </button>
    <div class="mt-3 text-sm">
      <p v-if="isLoading" class="text-blue-500 animate-pulse">正在处理，请稍候...</p>
      <p v-else-if="message" class="text-green-600 whitespace-pre-line">{{ message }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const files = ref([])
const message = ref("")
const fileInput = ref(null)
const isLoading = ref(false)

function onFileChange(e) {
  for (const f of e.target.files) {
    files.value.push(f)
  }
  uploadFiles()
}

function triggerFileInput() {
  fileInput.value.click()
}

function handleDrop(event) {
  file.value = event.dataTransfer.files[0]
  uploadFile()
}

async function uploadFiles() {
  if (!files.value.length) return alert("请选择文件")
  isLoading.value = true
  const formData = new FormData()
  for (const f of files.value) {
    formData.append("files", f)
  }

  const res = await fetch("http://localhost:8002/upload/", {
    method: "POST",
    body: formData
  })
  const data = await res.json()
  message.value = data.message.map(entry => `${entry.file}：${entry.status}`).join("\n")
  isLoading.value = false
}
</script>