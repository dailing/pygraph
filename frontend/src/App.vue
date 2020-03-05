<template>
  <div id="app">
    <!-- <img alt="Vue logo" src="./assets/logo.png"> -->
    <!-- <HelloWorld msg="Welcome to Your Vue.js App"/> -->
    asdfasd sdf
    <SvgGraph
     :boxes='boxes'
     :wires='wires'
    /> 

  </div>
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'
// import Box from './components/Box'
import Vue from 'vue' 
import VueResource from 'vue-resource';
import SvgGraph from './components/SvgGraph'
Vue.use(VueResource); 

export default {
  name: 'App',
  data: function(){
    return {
      boxes:{},
      wires:{}
    }
  },
  components: {
    SvgGraph
  },
  methods:{
    get_boxes: function () {
      this.$http.get('/api/box_list').then(response => {
        console.log(response.data);
        this.boxes = response.data
      }, response => {
        console.log(response);
      });
      this.$http.get('/api/wire_list').then(response => {
        console.log(response.data);
        this.wires = response.data;
      }, response => {
        console.log(response);
      })
    }
  },
  mounted: function(){
    console.log("__init__");
    this.get_boxes()
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
