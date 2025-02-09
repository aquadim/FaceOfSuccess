// Связь с backend API, в Javascript функциях
import config from "./config.js";

function doFetch(path, params = {}) {
    params.headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    };
    return fetch(config.apiUrl + path, params);
}

// Запрашивает у сервера генерацию имени файла для сохранения
export async function getFilenameToSave() {
    const response = await doFetch("/get-name-to-save");
    const jsonData = await response.json();
    return jsonData;
}

// Запрашивает у сервера сохранение фотографий
export async function requestSaving(photoIds, path) {
    const response = await doFetch("/save", {
        method: 'post',
        body: JSON.stringify({images: photoIds, savepath: path})
    });
}