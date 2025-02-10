<script setup>
// Страница завершения
import Button    from "../components/NavButton.vue"
import Heading      from "../components/Heading.vue"
import { ref }      from "vue"
import { useRouter } from "vue-router"

let secondsToMain = ref(10);
const router = useRouter();

const decrementId = setInterval(function() {
    secondsToMain.value--;
    if (secondsToMain.value == 0) {
        returnToMain();
    }
}, 1000);

function returnToMain() {
    // Очищаем интвервал уменьшения
    clearInterval(decrementId);

    // Переходим на главную
    router.push("/");
}

</script>

<template>
    <div id="finalPage" class="page-main">
        <Heading text="Успешно сохранено!"/>
        <p class="w3-center w3-xlarge">
            Возвращаемся на главную страницу через...
        </p>
        <p class="w3-center w3-jumbo">{{secondsToMain}}</p>

        <div class="w3-row">
            <div class="w3-container w3-col s12">
                <Button
                    class="w3-block"
                    text="На главную"
                    icon="house"
                    target="Main"
                    @click="returnToMain"
                    stylename="primary"/>
            </div>
        </div>
    </div>

    <div id="modals"></div>
</template>

<style scoped>
#finalPage {
    grid-template-rows: auto auto 1fr 10vh;
}
</style>
