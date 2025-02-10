// Файл для сохранения глобальных данных
import { reactive } from 'vue'

export const storage = reactive({
    // Данные фотографии, создаваемые в Camera.vue и передаваемые в API
    // Кодировка base64
    imageData: '',

    // Найденные лица после фотографирования
    foundFaces: [1],

    // Описание ошибки (если есть) после фотографирования
    errorMessage: "",

    // Путь сохранения
    savePath: ""
});