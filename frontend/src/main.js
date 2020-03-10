import Vue from 'vue'
import App from './App.vue'

Vue.config.productionTip = false

import VueSocketIO from 'vue-socket.io'
import SocketIO from "socket.io-client";

// const options = { path: '/socket.io' }; //Options object to pass into SocketIO

Vue.use(new VueSocketIO({
    debug: true,
    connection: SocketIO(''), //options object is Optional
    // vuex: {
    //   store,
    //   actionPrefix: "SOCKET_",
    //   mutationPrefix: "SOCKET_"
    // } 
  })
);

new Vue({
  render: h => h(App),
}).$mount('#app')
