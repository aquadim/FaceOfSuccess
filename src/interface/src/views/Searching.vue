<script setup>
// Страница поиска фотографий
import Heading from "../components/Heading.vue"
import Loader from "../components/Loader.vue"
import config from "../config.js"
import { onMounted } from "vue"
import { useRoute } from "vue-router"

const facts = [
    "Техникум был основан в 1955 году",
    "Техбот - брат Лица успеха",
    "Лицо успеха - дипломный проект студента техникума"
];
const factToDisplay = facts[Math.floor(Math.random() * facts.length)];

onMounted(async function() {
    // Запрос лиц
    const route = useRoute();
    const imageData = route.params.img;

    const response = await fetch(config.apiUrl+"/accept-face", {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({base64image: imageData})
    });
});
</script>

<template>
    <div id="searchingPage" class="page-main">
        <Heading text="Подожди"/>
        <p>Выполняется поиск фотографий</p>
        <Loader/>
        <p>Интересный факт: {{factToDisplay}}</p>
    </div>
</template>

<style scoped>
#searchingPage
{
    grid-template-rows: auto auto auto auto 1fr;
}
</style>
