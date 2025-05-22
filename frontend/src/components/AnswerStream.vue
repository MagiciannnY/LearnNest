<template>
  <div class="message-block w-full">
    <div class="prose prose-sm prose-slate text-sm text-left leading-loose"
         v-html="answerHtml"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { marked } from 'marked'

const props = defineProps({
  question: String,
  onComplete: Function
})

const emit = defineEmits(['stream-started'])

const answer = ref("")
const answerHtml = ref("")
const streamStarted = ref(false)

onMounted(() => {
  fetchAnswer(props.question)
})

async function fetchAnswer(q) {
  if (!q || q.trim() === "") return

  let started = false

  try {
    const res = await fetch("http://localhost:8002/ask/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: q })
    })

    const reader = res.body.getReader()
    const decoder = new TextDecoder("utf-8")

    while (true) {
      const { value, done } = await reader.read()
      if (done) break
      const chunk = decoder.decode(value)
      if (!started) {
        emit('stream-started')
        started = true
      }
      const lines = chunk.split('\n')
      for (const line of lines) {
        if (line.startsWith("data: ")) {
          const json = line.slice(6).trim()
          if (json === "[DONE]") continue
          try {
            const parsed = JSON.parse(json)
            const content = parsed.choices?.[0]?.delta?.content || ""
            answer.value += content
            answerHtml.value = marked.parse(answer.value)
          } catch (e) {
            console.warn("无法解析 JSON:", json)
          }
        }
      }
    }
    props.onComplete?.(answer.value)
  } catch (err) {
    answer.value = "❌ 出错了：" + err.message
    answerHtml.value = `<pre>${answer.value}</pre>`
  }
}
</script>