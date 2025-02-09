<script setup>
// Страница сохранения фотографий в ZIP
import Heading                  from "../components/Heading.vue"
import Loader                   from "../components/Loader.vue"
import { onMounted }            from "vue"
import { storage }              from '../storage.js'
import { useRouter }            from "vue-router"
import { requestSaving }        from '../api.js'

const router = useRouter();

onMounted(async function() {
    await requestSaving(storage.foundFaces, storage.savePath);
    router.push("/Final");
});
</script>

<template>
    <div>
        <Heading text="Подожди"/>
        <p class="w3-center w3-xlarge">
            Фотографии сохраняются
        </p>
        <div class="w3-center">
            <Loader/>
        </div>
    </div>
</template>

<style scoped>
</style>
