<script setup>
import config   from "../config.js";
const props = defineProps({
    imageId: Number
});
const imageUrl = config.apiUrl + "/photo?id=" + props.imageId;
</script>

<template>
    <img class="w3-round-xlarge w3-col l4 w3-border resultImage" :src="imageUrl" loading="lazy"/>
</template>

<style scoped>
.resultImage {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
</style>