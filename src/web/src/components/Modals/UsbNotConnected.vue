<script setup>
import Heading  from "../Heading.vue"
import Button   from "../Button.vue"

const props = defineProps({filename: String});
const emit  = defineEmits(['confirm', 'cancel'])
</script>

<template>
    <div class="w3-modal" style="display: block">
        <div class="w3-modal-content w3-animate-top">
            <div class="w3-container">
                <div id="layout">
                    <Heading text="Хранилище не подключено"/>
                    <p class="w3-center w3-xlarge">
                        Необходимо вставить в киоск флеш-карту или другое USB-хранилище. 
                    </p>
                    <img class="w3-padding" src="/img/usb.png"/>
                    <Button icon="check" text="Хорошо" @click="emit('confirm')" stylename="secondary"/>
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
