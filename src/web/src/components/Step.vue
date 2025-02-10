<script setup>
const props = defineProps({
    text: String,
    color: String,
    borderColor: String,
    number: String
});

</script>

<template>
    <div class="w3-margin w3-xlarge">
        <div
            class="w3-circle w3-cell w3-center w3-cell-middle number-circle w3-border w3-topbar w3-bottombar w3-leftbar w3-rightbar"
            :class="borderColor,color">
            {{number}}
        </div>
        <p class="w3-cell w3-cell-middle description w3-padding">{{text}}</p>
    </div>
</template>

<style scoped>
.number-circle
{
    width: 128px;
    min-width: 128px;
    height: 128px;
    min-height: 128px;
}

.description
{
    text-align: justify;
}
</style>