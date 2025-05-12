// Связь с backend API, в Javascript функциях
import config from "./config.js";

//////////// API ЛИЦ ////////////
// Посылает запрос на API лиц
function doFaceFetch(path, params = {}) {
    params.headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    };
    return fetch(config.faceApiUrl + path, params);
}

// Отправляет лицо на обработку
export async function sendFace(base64image) {
    const response = await doFaceFetch("/accept-face", {
        method: 'post',
        body: JSON.stringify({base64image: base64image})
    });
    return await response.json();
}

// Посылает запрос на генерацию ZIP на сервере 
export async function getZip(imageIds) {
    const response = await doFaceFetch("/zip", {
        method: 'post',
        body: JSON.stringify({imageIds: imageIds})
    });
    return await response.blob();
}

//////////// API ФАЙЛОВОЙ СИСТЕМЫ ////////////

// Посылает запрос на API лиц
function doFSFetch(path, params = {}) {
    params.headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    };
    return fetch(config.filesystemApiUrl + path, params);
}

// Запрашивает у сервера генерацию имени файла для сохранения
export async function getFilenameToSave() {
    if (config.disableUSBChecks) {
        return {
            ok: true,
            path: "C:\\face_of_success\\result.zip"
        };
    }
    const response = await doFSFetch("/get-name-to-save");
    const jsonData = await response.json();
    return jsonData;
}

// Запрашивает у сервера сохранение фотографий
export async function requestSaving(zipBlob, path) {
    if (config.disableUSBChecks) {
        console.log("Сохранение файлов отключено");
        return;
    }
    const fd = new FormData();
    fd.append("zipfile", zipBlob);
    fd.append("savepath", path);

    await fetch(config.filesystemApiUrl + "/save", {
        method: 'post',
        body: fd
    });
}

// Проверяет, подключено ли внешнее устройство хранения
export async function checkExternalStorage() {
    debugger;
    if (config.disableUSBChecks) {
        return {ok: true};
    }
    const response = await fetch(config.filesystemApiUrl + "/usb-connected");
    const jsonData = await response.json();
    return jsonData;
}