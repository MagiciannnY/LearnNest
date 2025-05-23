<template>
  <div class="flex flex-col h-full">
    <!-- 对话区（可滚动） -->
    <div ref="chatContainer" class="flex-1 overflow-y-auto px-4 py-6 space-y-6">
      <div v-for="(entry, index) in history" :key="index" class="space-y-4">
        <!-- 用户提问外层块 -->
        <div class="message-block flex justify-end p-3">
          <div class="flex flex-col items-end max-w-[70%]">
            <div class="bg-gray-200 text-gray-800 text-sm py-1 px-3 rounded-xl text-left leading-loose">
              {{ entry.question }}
            </div>
            <div class="text-xs text-gray-500 mt-1">
              <button @click="copyToClipboard(entry.question, false, index, 'question')">
                <svg v-if="copiedIndex === index && copiedType === 'question'" class="w-4 h-4" viewBox="0 0 1024 1024" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                  <path d="M969.6 208c-9.6-9.6-25.6-9.6-35.2 0l-508.8 537.6c-19.2 19.2-48 19.2-70.4 3.2l-265.6-252.8c-9.6-9.6-25.6-9.6-35.2 0-9.6 9.6-9.6 25.6 0 35.2l265.6 252.8c38.4 38.4 102.4 35.2 137.6-3.2l508.8-537.6C979.2 233.6 979.2 217.6 969.6 208z" p-id="9888"></path>
                </svg>
                <svg v-else class="w-4 h-4" viewBox="0 0 1024 1024" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                  <path d="M943.4112 454.7072c-14.1312 0-25.6 11.4688-25.6 25.6v101.3248c0 64.9728-32.6144 124.416-84.6336 159.744 0.8704-8.448 1.3312-16.896 1.3312-25.4464V437.2992c0-134.7072-109.568-244.2752-244.2752-244.2752H311.6032c-8.3456 0-16.6912 0.4096-24.9856 1.28a193.05984 193.05984 0 0 1 159.5392-84.3776h278.6816c106.4448 0 193.0752 86.5792 193.0752 193.0752 0 14.1312 11.4688 25.6 25.6 25.6s25.6-11.4688 25.6-25.6c0-134.656-109.568-244.2752-244.2752-244.2752H446.1056c-89.5488 0-171.776 48.9472-214.6304 127.6928a41.69216 41.69216 0 0 0-5.0688 21.4528c-94.8736 28.5184-164.1984 116.6336-164.1984 220.672v306.3808c0 127.0272 103.3728 230.4 230.4 230.4h306.3808c101.6832 0 188.1088-66.2016 218.624-157.7984 91.0848-37.4272 151.4496-126.5152 151.4496-225.8944V480.3072c-0.0512-14.1312-11.52-25.6-25.6512-25.6z m-344.4224 459.4176H292.608c-98.816 0-179.2-80.384-179.2-179.2V428.544c0-98.816 80.384-179.2 179.2-179.2h306.3808c98.816 0 179.2 80.384 179.2 179.2v306.3808c0 15.3088-1.9456 30.1056-5.5296 44.288l-0.1536 0.4608c-0.4096 1.1264-0.7168 2.2528-0.9216 3.3792-21.1456 75.52-90.4704 131.072-172.5952 131.072z" fill="#44454A"></path>
                  <path d="M943.4112 359.7312c-14.1312 0-25.6 11.4688-25.6 25.6v17.92c0 14.1312 11.4688 25.6 25.6 25.6s25.6-11.4688 25.6-25.6v-17.92c0-14.1824-11.4688-25.6-25.6-25.6z" fill="#44454A"></path>
                </svg>
              </button>
            </div>
          </div>
        </div>
        <!-- AI 回答外层块 -->
        <div class="message-block flex justify-start p-3">
          <div class="flex flex-col items-start max-w-[70%]">
            <div class="prose prose-sm prose-slate text-sm text-left leading-loose" v-html="entry.answerHtml"></div>
            <div class="text-xs text-gray-500 mt-1">
              <button @click="copyToClipboard(entry.answerHtml, true, index, 'answer')">
                <svg v-if="copiedIndex === index && copiedType === 'answer'" class="w-4 h-4" viewBox="0 0 1024 1024" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                  <path d="M969.6 208c-9.6-9.6-25.6-9.6-35.2 0l-508.8 537.6c-19.2 19.2-48 19.2-70.4 3.2l-265.6-252.8c-9.6-9.6-25.6-9.6-35.2 0-9.6 9.6-9.6 25.6 0 35.2l265.6 252.8c38.4 38.4 102.4 35.2 137.6-3.2l508.8-537.6C979.2 233.6 979.2 217.6 969.6 208z" p-id="9888"></path>
                </svg>
                <svg v-else class="w-4 h-4" viewBox="0 0 1024 1024" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                  <path d="M943.4112 454.7072c-14.1312 0-25.6 11.4688-25.6 25.6v101.3248c0 64.9728-32.6144 124.416-84.6336 159.744 0.8704-8.448 1.3312-16.896 1.3312-25.4464V437.2992c0-134.7072-109.568-244.2752-244.2752-244.2752H311.6032c-8.3456 0-16.6912 0.4096-24.9856 1.28a193.05984 193.05984 0 0 1 159.5392-84.3776h278.6816c106.4448 0 193.0752 86.5792 193.0752 193.0752 0 14.1312 11.4688 25.6 25.6 25.6s25.6-11.4688 25.6-25.6c0-134.656-109.568-244.2752-244.2752-244.2752H446.1056c-89.5488 0-171.776 48.9472-214.6304 127.6928a41.69216 41.69216 0 0 0-5.0688 21.4528c-94.8736 28.5184-164.1984 116.6336-164.1984 220.672v306.3808c0 127.0272 103.3728 230.4 230.4 230.4h306.3808c101.6832 0 188.1088-66.2016 218.624-157.7984 91.0848-37.4272 151.4496-126.5152 151.4496-225.8944V480.3072c-0.0512-14.1312-11.52-25.6-25.6512-25.6z m-344.4224 459.4176H292.608c-98.816 0-179.2-80.384-179.2-179.2V428.544c0-98.816 80.384-179.2 179.2-179.2h306.3808c98.816 0 179.2 80.384 179.2 179.2v306.3808c0 15.3088-1.9456 30.1056-5.5296 44.288l-0.1536 0.4608c-0.4096 1.1264-0.7168 2.2528-0.9216 3.3792-21.1456 75.52-90.4704 131.072-172.5952 131.072z" fill="#44454A"></path>
                  <path d="M943.4112 359.7312c-14.1312 0-25.6 11.4688-25.6 25.6v17.92c0 14.1312 11.4688 25.6 25.6 25.6s25.6-11.4688 25.6-25.6v-17.92c0-14.1824-11.4688-25.6-25.6-25.6z" fill="#44454A"></path>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 流式输出占位（同样结构包裹） -->
      <div v-if="streaming" class="message-block w-full p-3">
        <div class="w-full">
          <div class="message-block flex justify-end mb-2">
            <div class="bg-gray-200 text-gray-800 text-sm py-1 px-3 rounded-xl text-left leading-loose max-w-[70%]">
              {{ currentStreamingQuestion }}
            </div>
          </div>
          <div class="message-block flex justify-start">
            <div class="max-w-[70%]">
              <svg
                v-if="!streamStarted"
                class="w-6 h-6 pulse-loader"
                viewBox="0 0 1024 1024"
                xmlns="http://www.w3.org/2000/svg"
                fill="currentColor"
              >
                <path d="M512 512m-512 0a512 512 0 1 0 1024 0 512 512 0 1 0-1024 0Z"></path>
              </svg>
              <AnswerStream
                :question="currentStreamingQuestion"
                :onComplete="onStreamComplete"
                :key="streamKey"
                @stream-started="() => streamStarted = true"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 底部输入区 -->
    <!-- 容器包裹输入框 -->
      <div class="w-full flex justify-center">
        <form
          @submit.prevent="askQuestion"
          class="max-w-[640px] w-full mx-auto bg-white rounded-[24px] m-4 px-4 py-3 flex items-end gap-2 shadow-md border border-gray-300"
        >
        <textarea
          v-model="question"
          class="flex-1 bg-transparent focus:outline-none text-sm resize-none max-h-32 overflow-y-auto py-[6px] leading-[1.5]"
          rows="1"
          placeholder="询问任何问题"
          @input="autoResize"
          @keydown.enter.exact.prevent="askQuestion"
          ref="textareaRef"
        />
        <button
          type="submit"
          class="bg-black text-white rounded-full w-8 h-8 flex items-center justify-center hover:opacity-80 transition self-end"
        >
          <svg class="w-4 h-4" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg" fill="currentColor">
            <path d="M746.026667 197.674667l-296.789334 389.461333a138.154667 138.154667 0 0 0-10.581333-4.181333l-238.634667-82.773334a19.114667 19.114667 0 0 1-2.176-35.413333l548.181334-267.093333z m-249.514667 423.936l292.522667-383.829334-100.352 584.277334c-2.901333 16.810667-24.917333 21.930667-35.2 8.234666l-149.888-200.064a135.04 135.04 0 0 0-7.082667-8.661333z m355.669333-403.584c10.666667-62.08-54.912-109.824-112.426666-81.834667L171.605333 413.013333c-62.165333 30.293333-56.661333 118.954667 8.789334 141.653334l238.592 82.773333c14.848 5.162667 27.776 14.592 37.12 27.008l149.930666 200.106667c41.088 54.826667 129.237333 34.261333 140.757334-32.853334l105.386666-613.674666z" fill="#ffffff"></path>
          </svg>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted, watch } from 'vue'
import AnswerStream from './AnswerStream.vue'
import { marked } from 'marked'
import axios from 'axios'

const emit = defineEmits(['new-session'])

const props = defineProps({
  sessionId: String,
  history: {
    type: Array,
    default: () => []
  }
})

const question = ref("")
const streamKey = ref(0)
const streaming = ref(false)
const history = ref([])
const sessionId = ref(props.sessionId || "")
const userId = 'default_user001'

const chatContainer = ref(null)
const textareaRef = ref(null)

const copiedIndex = ref(null)
const copiedType = ref(null)

const currentStreamingQuestion = ref("")

const streamStarted = ref(false)

watch(() => props.history, (newHistory) => {
  if (newHistory.length > 0) {
    history.value = newHistory.map(item => ({
      question: item.question,
      answerHtml: marked.parse(item.answer)
    }))
  }
}, { immediate: true })

function autoResize() {
  const el = textareaRef.value
  if (el) {
    el.style.height = 'auto'
    el.style.height = el.scrollHeight + 'px'
  }
}

onMounted(() => {
  autoResize()
})

function askQuestion() {
  if (!question.value.trim()) return

  const userQuestion = question.value
  question.value = ""
  
  currentStreamingQuestion.value = userQuestion
  streaming.value = true
  streamKey.value += 1
  streamStarted.value = false

  nextTick(() => {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  })
}

async function onStreamComplete(answerText) {
  const questionText = currentStreamingQuestion.value
  const answerHtml = marked.parse(answerText)

  history.value.push({
    question: questionText,
    answerHtml
  })
  streaming.value = false
  currentStreamingQuestion.value = ""
  streamStarted.value = false

  try {
    if (!sessionId.value && questionText && answerText) {
      const res = await axios.post('http://localhost:8002/history/start', {
        user_id: userId,
        title: questionText,
        content: `<question>${questionText}</question>\n<answer>${answerText}</answer>`
      })
      sessionId.value = res.data.session_id

      // 向父组件主动触发历史记录刷新
      emit('new-session', {
        session_id: sessionId.value,
        title: questionText,
        created_at: new Date().toISOString()
      })
    } else if (questionText && answerText) {
      await axios.post('http://localhost:8002/history/save', {
        session_id: sessionId.value,
        user_id: userId,
        content: `<question>${questionText}</question>\n<answer>${answerText}</answer>`
      })
    }
  } catch (error) {
    console.error('保存聊天记录失败', error)
  }

  nextTick(() => {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  })
}

function copyToClipboard(content, isHtml = false, index, type) {
  const text = isHtml ? new DOMParser().parseFromString(content, 'text/html').body.innerText : content
  navigator.clipboard.writeText(text)
  copiedIndex.value = index
  copiedType.value = type
  setTimeout(() => {
    copiedIndex.value = null
    copiedType.value = null
  }, 3000)
}
</script>

<style scoped>
.prose :where(pre, code) {
  white-space: pre-wrap;
  word-break: break-word;
}

.pulse-loader {
  animation: pulseGrowFade 1.2s infinite ease-in-out;
  transform-origin: center;
  fill: #888;
}

@keyframes pulseGrowFade {
  0% {
    transform: scale(0.4);
    fill: #bbb;
  }
  50% {
    transform: scale(0.8);
    fill: #444;
  }
  100% {
    transform: scale(0.4);
    fill: #bbb;
  }
}
</style>
