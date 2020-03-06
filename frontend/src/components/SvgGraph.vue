<template>
<div class="columns">
  <div class="column"></div>
  <div class="column is-three-quarters">
    <svg v-bind:width="width" v-bind:height="height">
      <Wire
        v-for="w in wires"
        :key='w.uuid'
        :wire='w'
        :ports='ports'
      />
      <Box 
        v-for="(b) in render_list"
        :state="boxes[b]"
        :key="boxes[b].uuid"
        @box_mouse_down="box_mouse_done"
        @box_port_change='box_port_change'
        @box_select='box_select'
      />
    </svg>
  </div>

</div>
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
      current_box:null,
    }
  },
  methods: {
    box_mouse_done: function(boxid) {
      console.log(boxid);
      this.current_box = boxid;
      this.$set(this, 'current_box', boxid);
    },
    box_port_change: function(uuid, ports){
      let tmp = {};
      for(let ii of ports){
        tmp[ii.id] = ii;
      }
      this.$set(this.ports, uuid, tmp);
      // this.ports[uuid] = tmp;
    }
  },
  created(){
  },
  computed: {
    render_list: function(){
      var l = [];
      if(this.current_box != null){
        l.push(this.current_box);
      }
      for(var x in this.boxes){
        if(x!=this.current_box){
          l.push(x);
        }
      }
      return l.reverse();
    }
  }
};
</script>

<style scoped>
svg {
  background-color: thistle;
}
</style>