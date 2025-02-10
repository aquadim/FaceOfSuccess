<script setup>
// Страница снятия фотографии
// Помощь и немного кода:
// https://developer.mozilla.org/ru/docs/Web/API/Media_Capture_and_Streams_API/Taking_still_photos
    
import Button from "../components/Button.vue"
import NavButton from "../components/NavButton.vue"
import Heading from "../components/Heading.vue"
import config from "../config.js"
import { onMounted, ref } from "vue"
import { useRouter } from 'vue-router'
import { storage } from '../storage.js'

const video = ref(null);
const canvas = ref(null);
const streaming = false;
const router = useRouter();

function takePhoto() {
    const ctx = canvas.value.getContext("2d");
    canvas.value.width = video.value.videoWidth;
    canvas.value.height = video.value.videoHeight;
    ctx.drawImage(video.value, 0, 0);

    storage.photoData = canvas.value.toDataURL("image/png").split(',')[1];

    router.push('/Searching');
}

onMounted(() => {
    navigator.mediaDevices
        .getUserMedia({ video: true, audio: false })
        .then((stream) => {
            video.value.srcObject = stream;
            video.value.play();
        })
        .catch((err) => {
            console.error(`An error occurred: ${err}`);
        });
})
</script>

<template>
    <div id="cameraPage" class="page-main">
        <Heading text="Улыбнись!"/>

        <div id="videoWrapper" class="w3-center w3-margin-bottom">
            <video ref="video">Видеопоток недоступен</video>
        </div>

        <div class="w3-row">
            <div class="w3-container w3-col s6">
                <NavButton
                    class="w3-block"
                    text="Отмена"
                    icon="xmark"
                    target="Main"
                    stylename="secondary"/>
            </div>
            <div class="w3-container  w3-col s6">
                <Button
                    class="w3-block"
                    icon="camera"
                    text="Сфотографироваться"
                    stylename="primary"
                    @click="takePhoto"/>
            </div>
        </div>
    </div>

    <canvas ref="canvas" class="w3-hide"></canvas>
</template>

<style scoped>
#cameraPage
{
    grid-template-rows: auto 1fr 10vh;
}

#videoWrapper
{
    background-color: black;
}

#videoWrapper > video
{
    height: 100%;
    margin: auto;
}
</style>
