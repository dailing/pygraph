<template>
  <svg v-bind:width="width" v-bind:height="height">
    <Box 
      v-for="(b) in boxes"
      :state="b"
      :key="b.uuid"
      @select="box_selection"
    />
    <Wire
      v-for="w in wires"
      :key='w.uuid'
      :wire="w"
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
  methods: {
    box_selection: function(boxid) {
      console.log(boxid);
    }
  }
};
</script>

<style scoped>
</style>