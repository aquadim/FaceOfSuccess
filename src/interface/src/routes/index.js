import {createRouter,createWebHashHistory} from 'vue-router'
import Main from "../views/Main.vue"
import Camera from "../views/Camera.vue"
import Searching from "../views/Searching.vue"
import Results from "../views/Results.vue"

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
        path: "/Searching",
        name: "Searching",
        component: Searching
    },
    {
        path: "/Results",
        name: "Results",
        component: Results
    }
];

const router = createRouter({
    history: createWebHashHistory(),
    routes,
    scrollBehavior(to, from, savedPosition){return{top:0}}
});
export default router;