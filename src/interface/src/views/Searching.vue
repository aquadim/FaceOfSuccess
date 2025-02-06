<script setup>
// Страница поиска фотографий
import Heading from "../components/Heading.vue"
import Loader from "../components/Loader.vue"
import config from "../config.js"
import { onMounted } from "vue"
import { storage } from '../storage.js'
import { useRouter } from "vue-router"

const router = useRouter();

const facts = [
    "Техникум был основан в 1955 году",
    "Техбот - брат Лица успеха",
    "Лицо успеха - дипломный проект студента техникума"
];
const factToDisplay = facts[Math.floor(Math.random() * facts.length)];

onMounted(async function() {
    // Запрос лиц
    const imageData = storage.photoData;
    try {
        const response = await fetch(config.apiUrl+"/accept-face", {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({base64image: imageData})
        });

        const jsonResponse = await response.json();

        if (jsonResponse.ok) {
            storage.foundFaces = jsonResponse.photoIds;
            router.push('/Results');
        } else {
            storage.errorMessage = jsonResponse.description;
            router.push('/Failure');
        }
        
    } catch (err) {
        console.warn("Не удалось отправить данные лица на API");
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
