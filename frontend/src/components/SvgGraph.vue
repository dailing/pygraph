<template>
  <svg v-bind:width="width" v-bind:height="height">
    <Box 
      v-for="(b) in boxes"
      :state="b"
      :key="b.uuid"
      @select="box_selection"
      @box_port_change='box_port_change'
    />
    <Wire
      v-for="w in wires"
      :key='w.uuid'
      :wire='w'
      :ports='ports'
    />
  </svg>
</template>

<script>
import Box from "./Box.vue";
import Wire from './Wire.vue'

export default {
  name: "SvgGraph",
  props: {
    width: {
      type: [String, Number],
      default: "100%"
    },
    height: {
      type: [String, Number],
      default: 600
    },
    boxes: {
      type: Object,
      required: true
    },
    wires: {
      type: Object,
      required: true
    }
  },
  components: {
    Box, Wire
  },
  data: function(){
    return {
      ports:{},
    }
  },
  methods: {
    box_selection: function(boxid) {
      // console.log(boxid);
    },
    box_port_change: function(uuid, ports){
      let tmp = {};
      for(let ii of ports){
        tmp[ii.id] = ii;
      }
      this.$set(this.ports, uuid, tmp);
      // this.ports[uuid] = tmp;
    }
  }
};
</script>

<style scoped>
</style>