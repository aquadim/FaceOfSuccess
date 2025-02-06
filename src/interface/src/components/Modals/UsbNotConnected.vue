<script setup>
import Heading from "../Heading.vue"
import Button from "../Button.vue"

const props = defineProps({
    id: String
});

function hide() {
    document.getElementById(props.id).style.display = 'none';
    document.getElementById("modals").style.display = "none";
}
</script>

<template>
    <div :id="id" class="w3-modal">
        <div class="w3-modal-content w3-animate-top">
            <div class="w3-container">
                <div id="layout">
                    <Heading text="Хранилище не подключено"/>
                    <p class="w3-center w3-xlarge">
                        Необходимо вставить в терминал флеш-карту или другое USB-хранилище. 
                    </p>
                    <img src="/img/usb.png"/>
                    <Button icon="check" text="Хорошо" @click="hide" stylename="secondary"/>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
#layout
{
    display: grid;
    grid-template-rows: auto auto 256px 10vh;
}

img
{
    width: auto;
    margin: auto;
    height: 100%;
}
</style>
