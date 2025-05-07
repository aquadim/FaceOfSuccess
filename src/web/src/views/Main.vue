<script setup>
// Стартовая страница

import { createApp, h, ref }    from "vue"
import { useRouter }            from 'vue-router'
import { createConfirmDialog }  from 'vuejs-confirm-dialog'

import Button           from "../components/Button.vue"
import Heading          from "../components/Heading.vue"
import Step             from "../components/Step.vue"
import UsbNotConnected  from "../components/Modals/UsbNotConnected.vue"

import config                   from "../config.js"
import { checkExternalStorage}  from "../api.js"

const router = useRouter();

function start() {
    checkExternalStorage().then(function(data) {
        const isOk = data.ok;

        if (isOk) {
            router.push('/Camera');
            return;
        }

        // USB не подключен
        const { reveal, onConfirm, onCancel } = createConfirmDialog(
            UsbNotConnected
        );
        reveal();
        onConfirm(() => {
            // pass
        });
        onCancel(() => {
            // pass
        });
    });
}
</script>

<template>
    <div id="mainPage" class="page-main">
        <Heading text="Лицо успеха"/>
        <p class="w3-center w3-xlarge">
            Сфотографируйся, а программа найдёт все фотографии техникума, на которых ты присутствуешь!
        </p>
        <div class="steps">
            <Step
                number="1"
                text="Вставь флешку"
                color="w3-red"
                border-color="w3-border-pink"/>
            <Step
                number="2"
                text="Сфотографируйся"
                color="w3-amber"
                border-color="w3-border-orange"/>
            <Step
                number="3"
                text="Сохрани фотографии"
                color="w3-yellow"
                border-color="w3-border-amber"/>
        </div>

        <div class="w3-row">
            <div class="w3-container w3-col s12">
                <Button
                    class="w3-block"
                    text="Начать"
                    stylename="primary"
                    icon="play"
                    @click="start"/>
            </div>
        </div>
    </div>
</template>

<style scoped>
#mainPage {
    grid-template-rows: auto auto auto 10vh;
}

.steps {
    margin: auto;
}

#modals {
    position: absolute;
    height: 100vh;
    min-height: 100vh;
    max-height: 100vh;
    width: 100vw;
    left: 0;
    top: 0;
    display: none;
}
</style>
