<script setup>
const props = defineProps({
    text: String,
    stylename: String,
    icon: String
});

let constructedClass = "";
if (props.stylename == "primary") {
    constructedClass = "w3-blue";
} else if (props.stylename == "secondary") {
    constructedClass = "w3-border w3-light-grey";
} else {
    console.warn("Неизвестный стиль кнопки " + props.stylename);
}

const faIcon = "fa-" + props.icon;
</script>

<template>
    <button
        :class="constructedClass"
        class="w3-round-large w3-xlarge w3-btn">
        <i class="fa-solid" :class="faIcon"></i>
        {{text}}
    </button>
</template>

<style scoped>
</style>