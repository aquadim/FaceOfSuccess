<script setup>
// Страница ошибки фотографии
import Heading from "../components/Heading.vue"
import NavButton from "../components/NavButton.vue"
import { onMounted } from "vue"
import { storage } from '../storage.js'
</script>

<template>
    <div id="failurePage" class="page-main">
        <Heading text="Ой-ёй!"/>

        <div class="w3-center w3-xlarge">
            <p class="w3-jumbo w3-center">:(</p>
            <p>Не удалось собрать фотографии. Причина:</p>
            <p class="w3-monospace">{{storage.errorMessage}}</p>
        </div>

        <div class="w3-row">
            <div class="w3-container w3-col s6">
                <NavButton
                    class="w3-block"
                    icon="rotate-right"
                    text="Перефотографироваться"
                    target="Camera"
                    stylename="secondary"/>
            </div>
            <div class="w3-container w3-col s6">
                <NavButton
                    class="w3-block"
                    icon="house"
                    text="На главную"
                    target="Main"
                    stylename="secondary"/>
            </div>
        </div>
    </div>
</template>

<style scoped>
#failurePage {
    grid-template-rows: auto 1fr 10vh;
}
</style>
