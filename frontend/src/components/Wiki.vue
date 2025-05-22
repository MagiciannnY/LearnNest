<template>
  <div class="px-6 py-4 border-gray-300 space-y-4">
    <div
      v-for="file in uploadedFiles"
      :key="file"
      class="flex items-center justify-between bg-white rounded-xl shadow-sm border border-gray-200 px-5 py-3 hover:shadow-md transition-shadow duration-200"
    >
      <div class="flex items-center gap-3 text-gray-800">
        <span class="text-lg">📄</span>
        <span class="font-medium truncate max-w-lg">{{ file }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"

const uploadedFiles = ref([])

onMounted(async () => {
  try {
    const res = await fetch("http://localhost:8002/wiki/files")
    if (!res.ok) throw new Error(`HTTP错误! 状态码: ${res.status}`)
    const data = await res.json()
    uploadedFiles.value = data.files || []
  } catch (error) {
    console.error("获取文件列表失败:", error)
    uploadedFiles.value = []
  }
})
</script>
