import {createRouter,createWebHashHistory} from 'vue-router'
import Main from "../views/Main.vue"
import Camera from "../views/Camera.vue"
import Searching from "../views/Searching.vue"

const routes = [
    {
        path: "/",
        name: "Main",
        component: Main
    },
    {
        path: "/Camera",
        name: "Camera",
        component: Camera
    },
    {
        path: "/Searching/:img",
        name: "Searching",
        component: Searching
    }
];

const router = createRouter({
    history: createWebHashHistory(),
    routes,
    scrollBehavior(to, from, savedPosition){return{top:0}}
});
export default router;