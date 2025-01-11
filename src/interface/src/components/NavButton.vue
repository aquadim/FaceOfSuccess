<script setup>
const props = defineProps({
    text: String,
    target: String,
    stylename: String
});
const targetObj = {name: props.target};

let constructedClass = "";
if (props.stylename == "primary") {
    constructedClass = "w3-blue";
} else if (props.stylename == "secondary") {
    constructedClass = "w3-border w3-light-grey";
} else {
    console.warn("Неизвестный стиль кнопки " + props.stylename);
}
</script>

<template>
    <RouterLink
        :to="targetObj"
        :class="constructedClass"
        class="w3-round-large w3-xlarge w3-btn">
        {{text}}
    </RouterLink>
</template>

<style scoped>
</style>