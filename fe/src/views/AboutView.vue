<script setup>
import { ref } from 'vue';
import {useToast} from 'vue-toast-notification'
import 'vue-toast-notification/dist/theme-sugar.css'

const selectedType = ref(1)
const notification = ref(null)

const $toast = useToast();
const showToast = (message) => {
  notification.value = $toast.success(message, {
    position: 'top-right',
    duration: 2500
  });
}
const clearToast = () => {
  $toast.clear()
}

const startCrawl = (async () => {
  await axios.get(`/crawl-data/${selectedType.value}`)
    .then((response) => {
      if (response.status === 200) {
        showToast('Successful')
      }
    })
    .catch((error) => {
      alert(error.message)
      console.log(error)
    })
})
</script>
<template>
  <div class="about">
    <div style="display: grid; gap: 50px; ">
      <div class="cover">
        <input @change="selectedType = 1" :checked="selectedType === 1" type="radio" name="select" id="option-1">
        <input @change="selectedType = 2" :checked="selectedType === 2" type="radio" name="select" id="option-2">
          <label for="option-1" class="option option-1">
            <div class="dot"></div>
              <span>Top 250</span>
              </label>
          <label for="option-2" class="option option-2">
            <div class="dot"></div>
              <span>Popular</span>
          </label>
      </div>

      <div style="display: flex; justify-content: center;">
        <button @click="startCrawl" class='glowing-btn'><span class='glowing-txt'>S<span class='faulty-letter'>T</span>ART</span></button>
      </div>
    </div>
  </div>
</template>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
