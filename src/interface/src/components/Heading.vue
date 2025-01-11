<script setup>
defineProps({
    text: String
})
</script>

<template>
    <h1 class="heading">{{text}}</h1>
</template>

<style scoped>
.heading
{
    text-align: center;
    font-weight: bold;
}
</style>
