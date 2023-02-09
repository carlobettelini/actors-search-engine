import Vue from 'vue'
import App from './App.vue'

Vue.config.productionTip = false

const cors = require("cors");
app.use(cors());

new Vue({
    render: h => h(App),
}).$mount('#app')