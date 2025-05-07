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
                <div class="w3-padding">
                    <Heading text="Сохранение фотографий"/>
                    <p class="w3-center w3-xlarge">
                        Файлы будут сохранены в <br/> <span class="w3-monospace">{{props.filename}}</span>
                    </p>

                    <div class="w3-row-padding">
                        <div class="w3-col l6">
                            <Button
                                class="buttonControl"
                                icon="xmark"
                                text="Отмена"
                                @click="emit('cancel')"
                                stylename="secondary"/>
                        </div>
                        
                        <div class="w3-col l6">
                            <Button
                                class="buttonControl"
                                icon="check"
                                text="Хорошо"
                                @click="emit('confirm')"
                                stylename="primary"/>
                        </div>
                    </div>
                    
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.buttonsRow {
    height: 10vh;
}
.buttonControl {
    width: 100%;
}
</style>
