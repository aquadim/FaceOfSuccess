<script setup>
// Страница поиска фотографий

import { onMounted } from "vue"
import { useRouter } from "vue-router"

import Heading from "../components/Heading.vue"
import Loader from "../components/Loader.vue"
import config from "../config.js"
import { sendFace } from "../api.js"
import { storage } from '../storage.js'

const router = useRouter();

// Выбор интересного факта
const facts = [
    "Техникум был основан в 1955 году",
    "Техбот - брат Лица успеха",
    "Лицо успеха - дипломный проект студента техникума"
];
const factToDisplay = facts[Math.floor(Math.random() * facts.length)];

onMounted(async function() {
    // Запрос лиц
    const response = await sendFace(storage.photoData);

    if (response.ok) {
        // Лица найдены
        storage.foundFaces = response.photoIds;
        router.push('/Results');
    } else {
        // Произошла ошибка
        storage.errorMessage = response.description;
        router.push('/Failure');
    }
});
</script>

<template>
    <div id="searchingPage" class="page-main">
        <Heading text="Подожди"/>
        <div>
            <p class="w3-center w3-xlarge">
                Выполняется поиск фотографий
            </p>
            <div class="w3-center">
                <Loader/>
            </div>
            <p class="w3-center w3-xlarge">
                Интересный факт: <br/> <span class="w3-text-blue">{{factToDisplay}}</span>
            </p>
        </div>
    </div>
</template>

<style scoped>
#searchingPage
{
    grid-template-rows: auto 1fr;
}
</style>
