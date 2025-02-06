<script setup>
// Страница результата
import Heading from "../components/Heading.vue"
import { onMounted } from "vue"
import { storage } from '../storage.js'

onMounted(async function() {
    // Смотрим на результат
    const response = await storage.faceCodingResponse.json();

    if (response.ok) {
        // Успешный ответ от сервера
    }
});
</script>

<template>
    <div id="resultsPage" class="page-main">
        <Heading text="Готово!"/>
    </div>
</template>

<style scoped>
</style>
