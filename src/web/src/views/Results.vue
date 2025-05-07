<script setup>
// Страница результата
import Button           from "../components/Button.vue"
import NavButton        from "../components/NavButton.vue"
import Heading          from "../components/Heading.vue"
import ResultImage      from "../components/ResultImage.vue"
import ShowFilename     from "../components/Modals/ShowFilename.vue"

import { onMounted, createApp, h }  from "vue"
import { createConfirmDialog }      from 'vuejs-confirm-dialog'
import { useRouter }                from 'vue-router'
import { storage }                  from '../storage.js'
import { getFilenameToSave }        from '../api.js'

const router = useRouter();

async function start() {
    const response = await getFilenameToSave();

    const { reveal, onConfirm, onCancel } = createConfirmDialog(
        ShowFilename,
        {filename: response.path}
    );
    reveal();
    onConfirm(() => {
        storage.savePath = response.path;
        router.push("/Saving"); 
    });
    onCancel(() => {
        console.log('pass');
    });
}
</script>

<template>
    <div id="resultsPage" class="page-main">
        <Heading text="Готово!"/>
        <p class="no-margin w3-center w3-xlarge">Найдено {{storage.foundFaces.length}} фотографий!<br/>Вот некоторые из них:</p>

        <div class="images">
            <ResultImage
                v-for="imageId in storage.foundFaces.slice(0,6)"
                :imageId="imageId"
                :key="imageId"/>
        </div>

        <div class="w3-row">
            <div class="w3-container w3-col s6">
                <NavButton
                    class="w3-block"
                    icon="house"
                    text="На главную"
                    target="Main"
                    stylename="secondary"/>
            </div>
            <div class="w3-container w3-col s6">
                <Button
                    class="w3-block"
                    icon="save"
                    text="Сохранить результат"
                    stylename="primary"
                    @click="start"/>
            </div>
        </div>
    </div>
    <div id="modals"></div>
</template>

<style scoped>
#resultsPage {
    grid-template-rows: auto auto minmax(0, 1fr) 10vh;
}

.images {
    width: 80%;
    margin-left: auto;
    margin-right: auto;
    margin-top: 1rem;
    margin-bottom: 1rem;
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    grid-template-rows: 1fr 1fr 1em;
    grid-gap: 1rem;
}

.no-margin {
    margin: 0;
}
</style>
